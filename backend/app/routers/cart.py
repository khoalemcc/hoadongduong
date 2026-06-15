from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)

@router.get("/{user_id}", response_model=schemas.Cart)
def get_user_cart(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not cart:
        # Create a new cart if not exists
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.post("/items")
def add_to_cart(cart_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    # Simple logic to add item to cart
    item = models.CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
    db.add(item)
    db.commit()
    return {"message": "Product added to cart"}
