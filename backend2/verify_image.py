# verify_images.py
from app.database import SessionLocal
from app import models

db = SessionLocal()
for p in db.query(models.Product).all():
    print(p.id, [img.image_url for img in p.images])
db.close()
