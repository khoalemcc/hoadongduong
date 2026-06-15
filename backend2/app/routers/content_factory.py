from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional

from app import auth, models
from app.database import get_db
from app.models import BlogPost, PostStatus
from app.services import content_factory


router = APIRouter(
    prefix="/admin/content-factory",
    tags=["Content Factory"],
    dependencies=[Depends(auth.check_admin)],
)


class SourcePreviewRequest(BaseModel):
    source_urls: List[str] = Field(default_factory=lambda: list(content_factory.DEFAULT_SOURCE_URLS))
    limit: int = Field(default=10, ge=1, le=50)
    full_owned_content: bool = False


class SourceImportRequest(SourcePreviewRequest):
    status: PostStatus = PostStatus.draft
    allow_duplicates: bool = False


class DraftRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=255)
    keyword: Optional[str] = Field(default=None, max_length=255)
    audience: Optional[str] = Field(default=None, max_length=255)
    status: PostStatus = PostStatus.draft


def next_available_slug(db: Session, base_slug: str) -> str:
    slug = base_slug
    suffix = 2
    while db.query(BlogPost).filter(BlogPost.slug == slug).first():
        slug = f"{base_slug}-{suffix}"
        suffix += 1
    return slug


def article_to_payload(article: content_factory.SourceArticle) -> dict:
    return {
        "title": article.title,
        "slug": article.slug,
        "content": article.content,
        "seo_keyword": article.seo_keyword,
        "source_url": article.source_url,
        "image_url": article.image_url,
    }


@router.post("/preview")
def preview_sources(payload: SourcePreviewRequest):
    urls, warnings = content_factory.collect_article_urls(payload.source_urls, payload.limit)
    articles = []
    for url in urls:
        try:
            article = content_factory.extract_article(url, payload.full_owned_content)
        except Exception as exc:
            warnings.append(f"Skipped article {url}: {exc.__class__.__name__}")
            continue
        articles.append(article_to_payload(article))
    return {"items": articles, "warnings": warnings}


@router.post("/import")
def import_sources(
    payload: SourceImportRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_admin),
):
    urls, warnings = content_factory.collect_article_urls(payload.source_urls, payload.limit)
    created = []
    duplicates = []
    skipped = 0
    for url in urls:
        existing = db.query(BlogPost).filter(BlogPost.content.contains(url)).first()
        if existing and not payload.allow_duplicates:
            duplicates.append({"id": existing.id, "title": existing.title, "slug": existing.slug, "source_url": url})
            skipped += 1
            continue
        try:
            article = content_factory.extract_article(url, payload.full_owned_content)
        except Exception as exc:
            warnings.append(f"Skipped article {url}: {exc.__class__.__name__}")
            skipped += 1
            continue

        post = BlogPost(
            title=article.title,
            slug=next_available_slug(db, article.slug),
            content=article.content,
            image_url=article.image_url,
            seo_keyword=article.seo_keyword,
            status=payload.status,
            created_by=current_user.id,
            updated_by=current_user.id,
        )
        db.add(post)
        created.append(post)

    db.commit()
    for post in created:
        db.refresh(post)

    return {
        "created": [{"id": post.id, "title": post.title, "slug": post.slug, "status": post.status} for post in created],
        "duplicates": duplicates,
        "skipped": skipped,
        "warnings": warnings,
    }


@router.post("/draft")
def create_original_draft(
    payload: DraftRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_admin),
):
    article = content_factory.build_original_draft(payload.topic, payload.keyword, payload.audience)
    post = BlogPost(
        title=article.title,
        slug=next_available_slug(db, article.slug),
        content=article.content,
        image_url=article.image_url,
        seo_keyword=article.seo_keyword,
        status=payload.status,
        created_by=current_user.id,
        updated_by=current_user.id,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"id": post.id, "title": post.title, "slug": post.slug, "status": post.status}
