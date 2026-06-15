import os
import sys
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

# Add project root to PYTHONPATH so we can import app modules
import cloudinary
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from app.database import SessionLocal, engine, Base
from app import models

# Configure Cloudinary – expects env vars to be set
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True,
)

def fetch_product_image(slug: str) -> str | None:
    """Scrape the main product image URL from cocayhoala.vn.
    Returns the absolute image URL or None if not found.
    """
    product_url = f"https://cocayhoala.vn/products/{slug}"
    try:
        resp = requests.get(product_url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"[WARN] Failed to GET {product_url}: {e}")
        return None
    soup = BeautifulSoup(resp.text, "html.parser")
    # Heuristic: the first <img> inside a container with class "product-gallery" or similar
    img_tag = soup.select_one('.product-gallery img')
    if not img_tag:
        img_tag = soup.select_one('img')  # fallback to first img on page
    if img_tag and img_tag.get('src'):
        src = img_tag['src']
        # Some src may be relative – make absolute
        if src.startswith('http'):
            return src
        else:
            return f"https://cocayhoala.vn{src}"
    return None

def upload_image_to_cloudinary(image_url: str, public_id: str) -> str | None:
    """Upload image by URL to Cloudinary and return the secure URL."""
    try:
        result = cloudinary.uploader.upload(image_url, public_id=public_id, folder='products')
        return result.get('secure_url')
    except Exception as e:
        print(f"[ERROR] Cloudinary upload failed for {image_url}: {e}")
        return None

def main():
    # Ensure tables exist (they already should)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        products = session.query(models.Product).all()
        for product in products:
            # Check if we already have a primary image for this product
            existing_image = (
                session.query(models.ProductImage)
                .filter_by(product_id=product.id, is_primary=True)
                .first()
            )
            if existing_image:
                print(f"[SKIP] Product {product.slug} already has image – {existing_image.image_url}")
                continue
            img_url = fetch_product_image(product.slug)
            if not img_url:
                print(f"[WARN] No image found for {product.slug}")
                continue
            cloud_url = upload_image_to_cloudinary(img_url, public_id=product.slug)
            if not cloud_url:
                continue
            # Save to DB
            new_img = models.ProductImage(
                product_id=product.id,
                image_url=cloud_url,
                is_primary=True,
            )
            session.add(new_img)
            session.commit()
            print(f"[OK] Uploaded image for {product.slug}: {cloud_url}")

if __name__ == "__main__":
    main()
