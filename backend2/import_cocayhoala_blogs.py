import argparse
import html
import os
import re
import sys
from html.parser import HTMLParser
from typing import Iterable
from urllib.parse import urljoin, urlparse

import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import BlogPost, PostStatus


DEFAULT_SOURCES = [
    "https://cocayhoala.vn/blogs/news-cocayhoala?view=en",
    "https://cocayhoala.vn/blogs/cham-soc-toc",
    "https://cocayhoala.vn/blogs/cham-soc-co-the",
    "https://cocayhoala.vn/blogs/cham-soc-da",
    "https://cocayhoala.vn/blogs/tin-tuc-co-cay-hoa-la",
    "https://cocayhoala.vn/blogs/cau-chuyen-thuong-hieu",
    "https://cocayhoala.vn/blogs/kien-thuc-chuyen-sau",
]
DEFAULT_TIMEOUT = 20
MAX_EXCERPT_CHARS = 700


class BlogHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
        self.meta: dict[str, str] = {}
        self.text_parts: list[str] = []
        self.title_parts: list[str] = []
        self._capture_tag: str | None = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"])
            return

        if tag == "meta":
            key = attrs_dict.get("property") or attrs_dict.get("name")
            value = attrs_dict.get("content")
            if key and value:
                self.meta[key.lower()] = html.unescape(value).strip()
            return

        if tag in {"p", "li", "h2", "h3"}:
            self._capture_tag = "body"
        elif tag == "h1":
            self._capture_tag = "title"

    def handle_endtag(self, tag):
        if tag in {"p", "li", "h1", "h2", "h3"}:
            self._capture_tag = None

    def handle_data(self, data):
        text = normalize_space(data)
        if not text:
            return
        if self._capture_tag == "title":
            self.title_parts.append(text)
        elif self._capture_tag == "body":
            self.text_parts.append(text)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def slugify(value: str) -> str:
    value = value.lower()
    replacements = {
        "đ": "d",
        "à": "a",
        "á": "a",
        "ả": "a",
        "ã": "a",
        "ạ": "a",
        "ă": "a",
        "ằ": "a",
        "ắ": "a",
        "ẳ": "a",
        "ẵ": "a",
        "ặ": "a",
        "â": "a",
        "ầ": "a",
        "ấ": "a",
        "ẩ": "a",
        "ẫ": "a",
        "ậ": "a",
        "è": "e",
        "é": "e",
        "ẻ": "e",
        "ẽ": "e",
        "ẹ": "e",
        "ê": "e",
        "ề": "e",
        "ế": "e",
        "ể": "e",
        "ễ": "e",
        "ệ": "e",
        "ì": "i",
        "í": "i",
        "ỉ": "i",
        "ĩ": "i",
        "ị": "i",
        "ò": "o",
        "ó": "o",
        "ỏ": "o",
        "õ": "o",
        "ọ": "o",
        "ô": "o",
        "ồ": "o",
        "ố": "o",
        "ổ": "o",
        "ỗ": "o",
        "ộ": "o",
        "ơ": "o",
        "ờ": "o",
        "ớ": "o",
        "ở": "o",
        "ỡ": "o",
        "ợ": "o",
        "ù": "u",
        "ú": "u",
        "ủ": "u",
        "ũ": "u",
        "ụ": "u",
        "ư": "u",
        "ừ": "u",
        "ứ": "u",
        "ử": "u",
        "ữ": "u",
        "ự": "u",
        "ỳ": "y",
        "ý": "y",
        "ỷ": "y",
        "ỹ": "y",
        "ỵ": "y",
    }
    for src, dest in replacements.items():
        value = value.replace(src, dest)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:180] or "blog-post"


def parse_html(raw_html: str) -> BlogHTMLParser:
    parser = BlogHTMLParser()
    parser.feed(raw_html)
    return parser


def is_article_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != "cocayhoala.vn":
        return False
    parts = [part for part in parsed.path.split("/") if part]
    return len(parts) >= 3 and parts[0] == "blogs"


def unique_article_urls(source_url: str, links: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    article_urls: list[str] = []
    for href in links:
        absolute = urljoin(source_url, href).split("#", 1)[0]
        if is_article_url(absolute) and absolute not in seen:
            seen.add(absolute)
            article_urls.append(absolute)
    return article_urls


def fetch(client: httpx.Client, url: str) -> str:
    response = client.get(url)
    response.raise_for_status()
    return response.text


def extract_post(client: httpx.Client, url: str, import_full_content: bool) -> dict[str, str]:
    parser = parse_html(fetch(client, url))
    title = (
        parser.meta.get("og:title")
        or parser.meta.get("twitter:title")
        or " ".join(parser.title_parts)
        or url.rstrip("/").rsplit("/", 1)[-1].replace("-", " ").title()
    )
    title = normalize_space(title.replace("– Cỏ Cây Hoa Lá", "").replace("- Cỏ Cây Hoa Lá", ""))

    description = parser.meta.get("description") or parser.meta.get("og:description") or ""
    body_text = "\n\n".join(dict.fromkeys(parser.text_parts))
    excerpt = normalize_space(description or body_text)
    if len(excerpt) > MAX_EXCERPT_CHARS:
        excerpt = excerpt[:MAX_EXCERPT_CHARS].rsplit(" ", 1)[0] + "..."

    if import_full_content:
        imported_body = body_text
    else:
        imported_body = excerpt

    source_line = f"Nguồn tham khảo: {url}"
    content = f"{imported_body}\n\n{source_line}".strip()

    return {
        "title": title,
        "slug": slugify(title),
        "content": content,
        "seo_keyword": title[:255],
        "source_url": url,
    }


def next_available_slug(db, base_slug: str) -> str:
    slug = base_slug
    suffix = 2
    while db.query(BlogPost).filter(BlogPost.slug == slug).first():
        slug = f"{base_slug}-{suffix}"
        suffix += 1
    return slug


def import_posts(args) -> int:
    headers = {
        "User-Agent": "HoaDongDuongBlogImporter/1.0 (+https://hoadongduong.local)"
    }
    with httpx.Client(headers=headers, timeout=DEFAULT_TIMEOUT, follow_redirects=True) as client:
        urls: list[str] = []
        for source_url in args.source_url:
            try:
                listing_parser = parse_html(fetch(client, source_url))
            except httpx.HTTPStatusError as exc:
                print(f"Skipping {source_url}: HTTP {exc.response.status_code}")
                continue
            for url in unique_article_urls(source_url, listing_parser.links):
                if url not in urls:
                    urls.append(url)

        if args.limit:
            urls = urls[: args.limit]

        if args.dry_run:
            for url in urls:
                try:
                    post_data = extract_post(client, url, args.full_owned_content)
                except httpx.HTTPStatusError as exc:
                    print(f"Skipping article {url}: HTTP {exc.response.status_code}")
                    continue
                print(f"- {post_data['title']} ({url})")
            print(f"Found {len(urls)} posts from {len(args.source_url)} source pages")
            return len(urls)

        database_url = args.database_url or os.getenv("DATABASE_URL")
        if not database_url:
            raise RuntimeError("DATABASE_URL is required. Pass --database-url or set DATABASE_URL.")

        engine = create_engine(database_url)
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = session_local()
        try:
            added = 0
            skipped = 0
            for url in urls:
                try:
                    post_data = extract_post(client, url, args.full_owned_content)
                except httpx.HTTPStatusError as exc:
                    print(f"Skipping article {url}: HTTP {exc.response.status_code}")
                    skipped += 1
                    continue
                existing = db.query(BlogPost).filter(BlogPost.content.contains(url)).first()
                if existing:
                    skipped += 1
                    continue

                post = BlogPost(
                    title=post_data["title"],
                    slug=next_available_slug(db, post_data["slug"]),
                    content=post_data["content"],
                    seo_keyword=post_data["seo_keyword"],
                    status=PostStatus.published,
                    created_by=args.author_id,
                    updated_by=args.author_id,
                )
                db.add(post)
                added += 1

            db.commit()
            print(f"Imported {added} posts, skipped {skipped} duplicates from {len(args.source_url)} source pages")
            return added
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import Cocayhoala blog posts into BlogPost.")
    parser.add_argument(
        "--source-url",
        action="append",
        default=None,
        help="Blog listing/category URL. Can be passed multiple times.",
    )
    parser.add_argument("--database-url", default=None)
    parser.add_argument("--author-id", type=int, default=1)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--full-owned-content",
        action="store_true",
        help="Import full article text. Use only if you own or are licensed to reuse the source content.",
    )
    parsed_defaults = parser
    return parsed_defaults


if __name__ == "__main__":
    try:
        args = build_parser().parse_args()
        if not args.source_url:
            args.source_url = DEFAULT_SOURCES
        sys.exit(0 if import_posts(args) >= 0 else 1)
    except Exception as exc:
        print(f"Import failed: {exc}", file=sys.stderr)
        sys.exit(1)
