from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import auth, crud, models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/blog",
    tags=["blog"],
)

@router.get("/", response_model=List[schemas.BlogPost])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_blog_posts(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.BlogPost)
def create_post(
    post: schemas.BlogPostCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.check_admin),
):
    return crud.create_blog_post(db=db, post=post)

@router.get("/{slug}", response_model=schemas.BlogPost)
def read_post_by_slug(slug: str, db: Session = Depends(get_db)):
    db_post = db.query(models.BlogPost).filter(models.BlogPost.slug == slug, models.BlogPost.is_deleted == False).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_post

@router.put("/{post_id}", response_model=schemas.BlogPost)
def update_post(
    post_id: int,
    post_update: schemas.BlogPostUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.check_admin),
):
    db_post = crud.update_blog_post(
        db,
        post_id=post_id,
        title=post_update.title,
        content=post_update.content,
        image_url=post_update.image_url,
        seo_keyword=post_update.seo_keyword,
        status=post_update.status.value if post_update.status else None
    )
    if not db_post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_post

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.check_admin),
):
    db_post = crud.delete_blog_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"status": "success", "message": "Blog post deleted"}
