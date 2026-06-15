from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from app.models import UserStatus, OrderStatus, PaymentMethod, DiscountType, PostStatus, PaymentStatus, ReviewStatus, InventoryAction

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    status: Optional[UserStatus] = None
    password: Optional[str] = None

class RoleBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int
    status: UserStatus
    created_at: datetime
    updated_at: datetime
    roles: List[RoleBase] = []
    model_config = ConfigDict(from_attributes=True)

# Product Schemas
class ProductBase(BaseModel):
    sku: Optional[str] = None
    name: str
    slug: str
    description: Optional[str] = None
    price: Decimal
    stock: int = 0
    brand_id: Optional[int] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

# Product Image Schemas
class ProductImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class ProductImage(ProductImageBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    images: List[ProductImage] = []
    model_config = ConfigDict(from_attributes=True)

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    slug: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Order Schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)
    price: Optional[Decimal] = None

class OrderItem(OrderItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    user_id: int
    total_price: Decimal
    shipping_fee: Decimal = Decimal(0)
    status: OrderStatus = OrderStatus.pending
    payment_status: PaymentStatus = PaymentStatus.pending
    payment_method: PaymentMethod
    shipping_address: str

class OrderCreate(BaseModel):
    items: List[OrderItemBase] = Field(..., min_length=1)
    payment_method: PaymentMethod
    shipping_address: str
    shipping_fee: Decimal = Decimal(0)
    payment_status: PaymentStatus = PaymentStatus.pending
    status: OrderStatus = OrderStatus.pending
    user_id: Optional[int] = None
    total_price: Optional[Decimal] = None

class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem] = []
    model_config = ConfigDict(from_attributes=True)

# Blog Schemas
class BlogPostBase(BaseModel):
    title: str
    slug: str
    content: str
    image_url: Optional[str] = None
    seo_keyword: Optional[str] = None
    status: PostStatus

class BlogPostCreate(BlogPostBase):
    created_by: int

class BlogPost(BlogPostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: Optional[int]
    model_config = ConfigDict(from_attributes=True)

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    seo_keyword: Optional[str] = None
    status: Optional[PostStatus] = None

# Cart Schemas
class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)
    price: Optional[Decimal] = None

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=1)

class CartItem(CartItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CartBase(BaseModel):
    user_id: int

class Cart(CartBase):
    id: int
    items: List[CartItem] = []
    model_config = ConfigDict(from_attributes=True)

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    email: Optional[str] = None

# Review Schemas
class ReviewBase(BaseModel):
    product_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    user_id: int
    status: ReviewStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# New Business Schemas
class PaymentBase(BaseModel):
    order_id: int
    amount: Decimal
    method: PaymentMethod
    status: PaymentStatus
    transaction_id: Optional[str] = None

class Payment(PaymentBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SEOMetaBase(BaseModel):
    page_type: str
    target_id: int
    meta_title: str
    meta_description: str

class SEOMetaCreate(SEOMetaBase):
    pass

class SEOMeta(SEOMetaBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Admin & Operational Schemas
class BrandBase(BaseModel):
    name: str
    slug: str
    logo_url: Optional[str] = None
    description: Optional[str] = None

class BrandCreate(BrandBase):
    pass

class Brand(BrandBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ShipmentBase(BaseModel):
    order_id: int
    tracking_code: str
    shipping_provider: str
    status: str

class Shipment(ShipmentBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BannerBase(BaseModel):
    title: str
    image_url: str
    redirect_url: Optional[str] = None
    position: str
    is_active: bool = True

class Banner(BannerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class InventoryLogBase(BaseModel):
    product_id: int
    quantity_before: int
    quantity_after: int
    action: InventoryAction
    note: Optional[str] = None

class InventoryLog(InventoryLogBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AuditLogBase(BaseModel):
    admin_id: int
    action: str
    module: str
    payload: Optional[str] = None
    ip_address: Optional[str] = None

class AuditLog(AuditLogBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
