from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, schemas, crud, auth
from app.database import get_db

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)

@router.get("/me", response_model=schemas.Cart)
def get_user_cart(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    user_id = current_user.id
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id, models.Cart.is_deleted == False).first()
    if not cart:
        # Create a new cart if not exists
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.post("/items")
def add_to_cart(
    item: schemas.CartItemCreate | None = Body(None),
    product_id: int | None = Query(None),
    quantity: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if item:
        product_id = item.product_id
        quantity = item.quantity
    if product_id is None:
        raise HTTPException(status_code=422, detail="product_id is required")
    quantity = quantity or 1
    if quantity < 1:
        raise HTTPException(status_code=422, detail="quantity must be greater than zero")

    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.is_deleted == False,
        models.Product.is_active == True,
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cart = crud.get_or_create_cart(db, current_user.id)
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == product_id,
        models.CartItem.is_deleted == False,
    ).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = models.CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            price=product.price,
        )
        db.add(cart_item)
    db.commit()
    return {"message": "Product added to cart"}

@router.post("/merge/me")
def merge_user_cart(local_items: list[dict], db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.merge_carts(db, user_id=current_user.id, local_items=local_items)
