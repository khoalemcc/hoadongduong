from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from decimal import Decimal
from typing import List
from app import models, schemas
import bcrypt

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id, models.User.is_deleted == False).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email, models.User.is_deleted == False).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_deleted == False).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    from app.auth import get_password_hash
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: dict):
    db_user = db.query(models.User).filter(models.User.id == user_id, models.User.is_deleted == False).first()
    if not db_user:
        return None
    
    for key, value in user_update.items():
        if key == "password" and value:
            from app.auth import get_password_hash
            db_user.password_hash = get_password_hash(value)
        elif hasattr(db_user, key):
            setattr(db_user, key, value)
            
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id, models.User.is_deleted == False).first()
    if db_user:
        db_user.is_deleted = True
        db.commit()
        return True
    return False

# Product CRUD
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id, models.Product.is_deleted == False).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).filter(models.Product.is_deleted == False).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise
    db.refresh(db_product)
    return db_product

def update_product_stock(db: Session, product_id: int, stock: int, note: str = "Manual update"):
    db_product = db.query(models.Product).filter(models.Product.id == product_id, models.Product.is_deleted == False).first()
    if db_product:
        qty_before = db_product.stock
        db_product.stock = stock
        action = models.InventoryAction.import_stock if stock > qty_before else models.InventoryAction.export_stock
        log_inventory_change(db, db_product.id, qty_before, stock, action, note)
        db.commit()
        db.refresh(db_product)
    return db_product

def can_delete_product(db: Session, product_id: int) -> bool:
    has_orders = db.query(models.OrderItem).filter(
        models.OrderItem.product_id == product_id, 
        models.OrderItem.is_deleted == False
    ).first() is not None
    
    has_inventory = db.query(models.InventoryLog).filter(
        models.InventoryLog.product_id == product_id, 
        models.InventoryLog.is_deleted == False
    ).first() is not None
    
    return not (has_orders or has_inventory)

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id, models.Product.is_deleted == False).first()
    if db_product:
        db_product.is_deleted = True
        db.commit()
        return True
    return False

def force_delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id, models.Product.is_deleted == False).first()
    if db_product:
        db.query(models.CartItem).filter(models.CartItem.product_id == product_id).update({"is_deleted": True})
        db.query(models.OrderItem).filter(models.OrderItem.product_id == product_id).update({"is_deleted": True})
        db.query(models.Review).filter(models.Review.product_id == product_id).update({"is_deleted": True})
        db.query(models.InventoryLog).filter(models.InventoryLog.product_id == product_id).update({"is_deleted": True})
        db_product.is_deleted = True
        db.commit()
        return True
    return False

# Blog CRUD
def get_blog_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BlogPost).filter(models.BlogPost.is_deleted == False).offset(skip).limit(limit).all()

def get_blog_post(db: Session, slug: str):
    return db.query(models.BlogPost).filter(models.BlogPost.slug == slug, models.BlogPost.is_deleted == False).first()

def delete_blog_post(db: Session, post_id: int):
    db_post = db.query(models.BlogPost).filter(models.BlogPost.id == post_id, models.BlogPost.is_deleted == False).first()
    if db_post:
        db_post.is_deleted = True
        db.commit()
    return db_post

def update_blog_post(db: Session, post_id: int, title: str = None, content: str = None, image_url: str = None, seo_keyword: str = None, status: str = None):
    db_post = db.query(models.BlogPost).filter(models.BlogPost.id == post_id, models.BlogPost.is_deleted == False).first()
    if db_post:
        if title is not None:
            db_post.title = title
        if content is not None:
            db_post.content = content
        if image_url is not None:
            db_post.image_url = image_url
        if seo_keyword is not None:
            db_post.seo_keyword = seo_keyword
        if status is not None:
            db_post.status = status
        db.commit()
        db.refresh(db_post)
    return db_post

# Order CRUD
def _legacy_create_order(db: Session, order: schemas.OrderCreate):
    # Senior Logic: Validate stock for all items first
    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id, models.Product.is_deleted == False).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")

    # Create the order
    db_order = models.Order(
        user_id=order.user_id,
        total_price=order.total_price,
        shipping_fee=order.shipping_fee,
        status=order.status,
        payment_status=order.payment_status,
        payment_method=order.payment_method,
        shipping_address=order.shipping_address
    )
    db.add(db_order)
    db.flush() # Get the order ID without committing yet
    
    # Process items and deduct stock
    for item in order.items:
        db_item = models.OrderItem(**item.model_dump(), order_id=db_order.id)
        db.add(db_item)
        
        # Deduct stock (Nghiệp vụ 19)
        product = db.query(models.Product).filter(models.Product.id == item.product_id, models.Product.is_deleted == False).first()
        qty_before = product.stock
        product.stock -= item.quantity
        log_inventory_change(db, product.id, qty_before, product.stock, models.InventoryAction.export_stock, f"Order #{db_order.id} placed")
    
    db.commit()
    db.refresh(db_order)
    return db_order

def create_order(db: Session, order: schemas.OrderCreate):
    products_by_id = {}
    calculated_total = Decimal(order.shipping_fee or 0)

    for item in order.items:
        product = (
            db.query(models.Product)
            .filter(
                models.Product.id == item.product_id,
                models.Product.is_deleted == False,
                models.Product.is_active == True,
            )
            .with_for_update()
            .first()
        )
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        products_by_id[item.product_id] = product
        calculated_total += Decimal(product.price or 0) * item.quantity

    db_order = models.Order(
        user_id=order.user_id,
        total_price=calculated_total,
        shipping_fee=order.shipping_fee,
        status=order.status,
        payment_status=order.payment_status,
        payment_method=order.payment_method,
        shipping_address=order.shipping_address,
    )
    db.add(db_order)
    db.flush()

    for item in order.items:
        product = products_by_id[item.product_id]
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price,
        )
        db.add(db_item)
        qty_before = product.stock
        product.stock -= item.quantity
        log_inventory_change(db, product.id, qty_before, product.stock, models.InventoryAction.export_stock, f"Order #{db_order.id} placed")

    db.commit()
    db.refresh(db_order)
    return db_order

# Review CRUD
def create_review(db: Session, review: dict):
    # Only allow if user has purchased (Simplified check here, can be expanded)
    db_review = models.Review(**review)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def create_blog_post(db: Session, post: schemas.BlogPostCreate):
    db_post = models.BlogPost(**post.model_dump(), updated_by=post.created_by)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_order(db: Session, order_id: int, order_update: dict):
    db_order = db.query(models.Order).filter(models.Order.id == order_id, models.Order.is_deleted == False).first()
    if not db_order:
        return None
    
    old_status = db_order.status
    new_status = order_update.get("status")
    if isinstance(new_status, str):
        new_status = models.OrderStatus(new_status)
        order_update["status"] = new_status

    for key, value in order_update.items():
        if hasattr(db_order, key):
            setattr(db_order, key, value)
    
    # Logic Nghiệp vụ 8: Hoàn kho nếu đơn hàng bị hủy
    if old_status != models.OrderStatus.cancelled and new_status == models.OrderStatus.cancelled:
        for item in db_order.items:
            product = db.query(models.Product).filter(models.Product.id == item.product_id, models.Product.is_deleted == False).first()
            if product:
                qty_before = product.stock
                product.stock += item.quantity
                log_inventory_change(db, product.id, qty_before, product.stock, models.InventoryAction.refund, f"Refund from cancelled Order #{db_order.id}")

    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id, models.Order.is_deleted == False).first()
    if db_order:
        db_order.is_deleted = True
        db.commit()
        return True
    return False

# Cart Merging (Nghiệp vụ 7)
def get_or_create_cart(db: Session, user_id: int):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id, models.Cart.is_deleted == False).first()
    if not cart:
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def merge_carts(db: Session, user_id: int, local_items: List[dict]):
    cart = get_or_create_cart(db, user_id)

    for item in local_items:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)
        
        # Check if item exists in DB cart
        existing_item = db.query(models.CartItem).filter(
            models.CartItem.cart_id == cart.id,
            models.CartItem.product_id == product_id
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = models.CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                price=item.get('price')
            )
            db.add(new_item)
    
    db.commit()
    db.refresh(cart)
    return cart

# SEO CRUD (Nghiệp vụ 18)
def create_seo_meta(db: Session, seo: schemas.SEOMetaCreate):
    db_seo = models.SEOMeta(**seo.model_dump())
    db.add(db_seo)
    db.commit()
    db.refresh(db_seo)
    return db_seo

# Operational Helpers
def log_inventory_change(db: Session, product_id: int, before: int, after: int, action: models.InventoryAction, note: str = None):
    log = models.InventoryLog(
        product_id=product_id,
        quantity_before=before,
        quantity_after=after,
        action=action,
        note=note
    )
    db.add(log)

def log_admin_action(db: Session, admin_id: int, action: str, module: str, payload: str = None, ip: str = None):
    log = models.AuditLog(
        admin_id=admin_id,
        action=action,
        module=module,
        payload=payload,
        ip_address=ip
    )
    db.add(log)
    db.commit()

# Brand CRUD
def create_brand(db: Session, brand: schemas.BrandCreate):
    db_brand = models.Brand(**brand.model_dump())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

# Banner CRUD
def create_banner(db: Session, banner: schemas.BannerBase):
    db_banner = models.Banner(**banner.model_dump())
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return db_banner
