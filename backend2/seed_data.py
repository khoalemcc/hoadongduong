import os
from app.database import SessionLocal, engine, Base
from app import crud, models, schemas
import csv
from pathlib import Path
from sqlalchemy.orm import Session

# Ensure tables exist
Base.metadata.create_all(bind=engine)

session: Session = SessionLocal()

# Clear existing data to prevent duplicate constraints
session.query(models.ProductImage).delete()
session.query(models.Product).delete()
session.query(models.BlogPost).delete()
session.commit()

# Helper to create product with images
def create_product_with_images(session: Session, product_data: schemas.ProductCreate, image_urls: list[str]):
    product = crud.create_product(db=session, product=product_data)
    # Add images, first image as primary
    for idx, url in enumerate(image_urls):
        img = models.ProductImage(
            product_id=product.id,
            image_url=url,
            is_primary=(idx == 0)  # first image primary
        )
        session.add(img)
    session.commit()
    session.refresh(product)
    return product

# Sample products
products = [
    {
        "sku": "HD001",
        "name": "Verde Shampoo",
        "slug": "verde-shampoo",
        "description": "Gentle botanical shampoo for daily use.",
        "price": 120000,
        "stock": 50,
        "brand_id": None,
        "is_active": True,
        "images": [
            "https://picsum.photos/seed/verde1/400/400",
            "https://picsum.photos/seed/verde2/400/400",
        ],
    },
    {
        "sku": "HD002",
        "name": "Aurum Conditioner",
        "slug": "aurum-conditioner",
        "description": "Rich conditioner with gold‑derived nutrients.",
        "price": 150000,
        "stock": 30,
        "brand_id": None,
        "is_active": True,
        "images": ["https://picsum.photos/seed/aurum/400/400"],
    },
    {
        "sku": "HD003",
        "name": "Terra Hair Oil",
        "slug": "terra-hair-oil",
        "description": "Nourishing oil infused with rare earth botanicals.",
        "price": 200000,
        "stock": 20,
        "brand_id": None,
        "is_active": True,
        "images": ["https://picsum.photos/seed/terra/400/400"],
    },
    {
        "sku": "HD004",
        "name": "Flora Curl Cream",
        "slug": "flora-curl-cream",
        "description": "Curl defining cream with natural extracts.",
        "price": 130000,
        "stock": 40,
        "brand_id": None,
        "is_active": True,
        "images": ["https://picsum.photos/seed/flora/400/400"]
    },
    {
        "sku": "HD005",
        "name": "Luna Hair Mask",
        "slug": "luna-hair-mask",
        "description": "Deep moisturizing hair mask for strength.",
        "price": 180000,
        "stock": 25,
        "brand_id": None,
        "is_active": True,
        "images": ["https://picsum.photos/seed/luna/400/400"]
    },
    {
        "sku": "HD006",
        "name": "Solar Spray",
        "slug": "solar-spray",
        "description": "Lightweight spray for shine and protection.",
        "price": 110000,
        "stock": 60,
        "brand_id": None,
        "is_active": True,
        "images": ["https://picsum.photos/seed/solar/400/400"]
    },
    {
        "sku": "HD007",
        "name": "Aura Scalp Serum",
        "slug": "aura-scalp-serum",
        "description": "Serum to stimulate scalp health.",
        "price": 140000,
        "stock": 35,
        "brand_id": None,
        "is_active": True,
        "images": ["https://picsum.photos/seed/aura/400/400"]
    },
    {
        "sku": "HD008",
        "name": "Nimbus Volume Powder",
        "slug": "nimbus-volume-powder",
        "description": "Powder for instant volume boost.",
        "price": 90000,
        "stock": 45,
        "brand_id": None,
        "is_active": True,
        "images": ["https://picsum.photos/seed/nimbus/400/400"]
    },
    {
        "sku": "HD009",
        "name": "Zen Hair Detox",
        "slug": "zen-hair-detox",
        "description": "Detoxifying treatment for clean scalp.",
        "price": 160000,
        "stock": 28,
        "brand_id": None,
        "is_active": True,
        "images": ["https://picsum.photos/seed/zen/400/400"]
    },
    {
        "sku": "HD010",
        "name": "Eclipse Night Oil",
        "slug": "eclipse-night-oil",
        "description": "Night oil for overnight regeneration.",
        "price": 210000,
        "stock": 22,
        "brand_id": None,
        "is_active": True,
        "images": ["https://picsum.photos/seed/eclipse/400/400"]
    }
]


for p in products:
    prod_create = schemas.ProductCreate(
        sku=p["sku"],
        name=p["name"],
        slug=p["slug"],
        description=p["description"],
        price=p["price"],
        stock=p["stock"],
        brand_id=p["brand_id"],
        is_active=p["is_active"],
    )
    create_product_with_images(session, prod_create, p["images"]) 

# Sample blog posts
blog_posts = [
    {
        "title": "Cây cỏ và mái tóc bạn",
        "slug": "cay-co-va-mai-toc-cua-ban",
        "content": "<p>Khám phá cách các loại thảo dược tự nhiên giúp nuôi dưỡng tóc từ gốc tới ngọn.</p>",
        "image_url": "https://picsum.photos/seed/blog1/800/400",
        "seo_keyword": "cây cỏ, tóc, chăm sóc",
        "status": "published",
        "created_by": 1,
    },
    {
        "title": "Câu chuyện thương hiệu Hoạ Đông Dương",
        "slug": "cau-chuyen-thuong-hieu-hoa-dong-duong",
        "content": "<p>Hành trình từ một vườn cây thuốc hữu cơ tới thương hiệu tóc cao cấp.</p>",
        "image_url": "https://picsum.photos/seed/blog2/800/400",
        "seo_keyword": "thương hiệu, hoa dong duong, câu chuyện",
        "status": "published",
        "created_by": 1,
    },
]

for b in blog_posts:
    post_create = schemas.BlogPostCreate(
        title=b["title"],
        slug=b["slug"],
        content=b["content"],
        image_url=b["image_url"],
        seo_keyword=b["seo_keyword"],
        status=b["status"],
        created_by=b["created_by"],
    )
    crud.create_blog_post(db=session, post=post_create)

print(f"Seed data inserted: {len(products)} products, {len(blog_posts)} blog posts")
