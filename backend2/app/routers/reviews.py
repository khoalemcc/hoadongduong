from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas, auth
from app.database import get_db

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)

@router.post("/", response_model=schemas.Review)
def create_review(
    review: schemas.ReviewCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Ensure user is the one reviewing
    review_data = review.model_dump()
    review_data["user_id"] = current_user.id
    return crud.create_review(db=db, review=review_data)

@router.get("/product/{product_id}", response_model=List[schemas.Review])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    return db.query(models.Review).filter(models.Review.product_id == product_id, models.Review.is_deleted == False).all()
