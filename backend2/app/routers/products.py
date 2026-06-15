from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
import os
from app import crud, schemas, auth, models
from app.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), admin: models.User = Depends(auth.check_admin)):
    try:
        return crud.create_product(db=db, product=product)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Product slug already exists")
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=400, detail=f"Unable to create product: {exc.__class__.__name__}")

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.patch("/{product_id}/stock", response_model=schemas.Product)
def update_stock(product_id: int, stock: int, db: Session = Depends(get_db), admin: models.User = Depends(auth.check_admin)):
    db_product = crud.update_product_stock(db, product_id=product_id, stock=stock)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, force: bool = False, db: Session = Depends(get_db), admin: models.User = Depends(auth.check_admin)):
    if not force and not crud.can_delete_product(db, product_id=product_id):
        raise HTTPException(
            status_code=400,
            detail="Cannot delete product because it is referenced in inventory logs or orders."
        )

    if force:
        success = crud.force_delete_product(db, product_id=product_id)
    else:
        success = crud.delete_product(db, product_id=product_id)
        
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"status": "success", "message": "Product removed from collection"}

from fastapi import UploadFile, File

@router.post("/{product_id}/image", response_model=schemas.ProductImage)
def upload_product_image(
    product_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    admin: models.User = Depends(auth.check_admin)
):
    # Verify product exists
    product = crud.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    try:
        import cloudinary
        import cloudinary.uploader
        
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        api_key = os.getenv("CLOUDINARY_API_KEY")
        api_secret = os.getenv("CLOUDINARY_API_SECRET")
        if not all([cloud_name, api_key, api_secret]):
            raise HTTPException(status_code=500, detail="Cloudinary configuration is missing")

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        
        # Upload directly to Cloudinary
        upload_result = cloudinary.uploader.upload(file.file)
        public_id = upload_result.get("public_id")
        
        # Automatically generate optimized transformed URL using f_auto and q_auto
        transformed_url = cloudinary.CloudinaryImage(public_id).build_url(
            fetch_format="auto",
            quality="auto"
        )
        
        # Save reference to Database
        db_image = models.ProductImage(
            product_id=product_id,
            image_url=transformed_url,
            is_primary=True
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Image upload to Cloudinary failed: {str(e)}")
from fastapi import UploadFile, File
import shutil

@router.post("/{product_id}/upload-image", response_model=schemas.ProductImage)
def upload_image_without_pillow(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.check_admin)
):
    """Upload an image file for a product without using Pillow.
    The file is saved to the local static directory and its URL is stored in the database.
    """
    # Verify product exists
    product = crud.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Ensure static directory exists
    static_dir = os.path.join(os.getcwd(), "static", "product_images")
    os.makedirs(static_dir, exist_ok=True)
    # Construct safe file path
    filename = f"{product_id}_{file.filename}"
    file_path = os.path.join(static_dir, filename)
    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Build a URL path (adjust based on your static file serving configuration)
    image_url = f"/static/product_images/{filename}"

    # Save reference to Database
    db_image = models.ProductImage(
        product_id=product_id,
        image_url=image_url,
        is_primary=True
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
