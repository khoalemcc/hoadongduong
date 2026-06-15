import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Ensure project root is in PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from app.database import SessionLocal, engine, Base
from app import models


def fetch_blog(url: str) -> dict:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Title
    title_tag = soup.select_one('h1') or soup.select_one('.blog-title')
    title = title_tag.get_text(strip=True) if title_tag else ''
    # Slug from URL
    slug = url.rstrip('/').split('/')[-1]
    # Content: combine article body paragraphs
    content_parts = []
    article = soup.select_one('.article-content') or soup.select_one('.blog-content')
    if article:
        for p in article.find_all(['p', 'h2', 'h3', 'ul', 'ol']):
            content_parts.append(str(p))
    content = '\n'.join(content_parts)
    # Image: first img in article
    img_tag = soup.select_one('.article-content img') or soup.select_one('.blog-content img')
    image_url = ''
    if img_tag and img_tag.get('src'):
        src = img_tag['src']
        image_url = src if src.startswith('http') else urljoin(url, src)
    return {
        'title': title,
        'slug': slug,
        'content': content,
        'image_url': image_url,
    }


def main():
    blog_url = 'https://cocayhoala.vn/blogs/cau-chuyen-phu-nu-viet-binh-thuong-ma-phi-thuong'
    data = fetch_blog(blog_url)
    # Insert into DB
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        # Check duplicate by slug
        existing = session.query(models.BlogPost).filter_by(slug=data['slug']).first()
        if existing:
            print(f"[SKIP] Blog post with slug {data['slug']} already exists.")
            return
        post = models.BlogPost(
            title=data['title'],
            slug=data['slug'],
            content=data['content'],
            image_url=data['image_url'],
            status=models.PostStatus.published,
            created_by=1,  # assuming admin user id 1 exists
        )
        session.add(post)
        session.commit()
        # Ensure stdout uses UTF-8 and report success
        import sys
        sys.stdout.reconfigure(encoding='utf-8')
        print(f"[DONE] Inserted blog post: {data['title']}")

if __name__ == '__main__':
    main()
