import os
import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from app.database import SessionLocal, engine, Base
from app import models

# Ensure tables exist (should already)
Base.metadata.create_all(bind=engine)

# Default placeholder image URL (Cloudinary demo image)
PLACEHOLDER_URL = "https://res.cloudinary.com/demo/image/upload/sample.jpg"

with SessionLocal() as session:
    # Find products without any primary image
    products_without_image = (
        session.query(models.Product)
        .outerjoin(models.ProductImage, models.Product.id == models.ProductImage.product_id)
        .filter(models.ProductImage.id.is_(None))
        .all()
    )
    for product in products_without_image:
        img = models.ProductImage(
            product_id=product.id,
            image_url=PLACEHOLDER_URL,
            is_primary=True,
        )
        session.add(img)
    session.commit()
    print(f"Added placeholder images for {len(products_without_image)} products.")
