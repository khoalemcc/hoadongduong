from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Numeric, TIMESTAMP, Enum, Table, CheckConstraint, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

IdType = BigInteger().with_variant(Integer, "sqlite")

# Enums
class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    banned = "banned"

class ReviewStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    spam = "spam"

class InventoryAction(enum.Enum):
    import_stock = "import"
    export_stock = "export"
    refund = "refund"
    order_lock = "lock"

class OrderStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    packing = "packing"
    shipping = "shipping"
    completed = "completed"
    cancelled = "cancelled"
    refunded = "refunded"

class PaymentStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"

class PaymentMethod(enum.Enum):
    cod = "cod"
    bank = "bank"
    momo = "momo"
    vnpay = "vnpay"

class DiscountType(enum.Enum):
    percent = "percent"
    fixed = "fixed"

class PostStatus(enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

# Association Tables
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", IdType, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", IdType, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", IdType, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", IdType, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
)

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", IdType, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", IdType, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)
)

order_coupons = Table(
    "order_coupons",
    Base.metadata,
    Column("order_id", IdType, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True),
    Column("coupon_id", IdType, ForeignKey("coupons.id", ondelete="CASCADE"), primary_key=True)
)

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, server_default="0", nullable=False)

# Models
class User(SoftDeleteMixin, Base):
    __tablename__ = "users"
    id = Column(IdType, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20), unique=True)
    gender = Column(String(10))  # male, female, other
    birthday = Column(TIMESTAMP, nullable=True)
    status = Column(Enum(UserStatus), default=UserStatus.active)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    addresses = relationship("UserAddress", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    blog_posts_created = relationship("BlogPost", foreign_keys="BlogPost.created_by", back_populates="creator")
    orders = relationship("Order", back_populates="user")

class Role(SoftDeleteMixin, Base):
    __tablename__ = "roles"
    id = Column(IdType, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(SoftDeleteMixin, Base):
    __tablename__ = "permissions"
    id = Column(IdType, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)
    description = Column(Text)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class UserAddress(SoftDeleteMixin, Base):
    __tablename__ = "user_addresses"
    id = Column(IdType, primary_key=True, autoincrement=True)
    user_id = Column(IdType, ForeignKey("users.id", ondelete="CASCADE"))
    full_name = Column(String(255))
    phone = Column(String(20))
    address_line = Column(Text)
    city = Column(String(100))
    district = Column(String(100))
    ward = Column(String(100))
    is_default = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="addresses")

class Product(SoftDeleteMixin, Base):
    __tablename__ = "products"
    id = Column(IdType, primary_key=True, autoincrement=True)
    sku = Column(String(50), unique=True, index=True)
    name = Column(String(255))
    slug = Column(String(255), unique=True, index=True)
    description = Column(Text)
    price = Column(Numeric(12, 2))
    stock = Column(BigInteger, default=0)
    brand_id = Column(IdType, ForeignKey("brands.id", ondelete="SET NULL"))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    attributes = relationship("ProductAttribute", back_populates="product", uselist=False)
    images = relationship("ProductImage", back_populates="product")
    categories = relationship("Category", secondary=product_categories, back_populates="products")
    reviews = relationship("Review", back_populates="product")

class ProductAttribute(SoftDeleteMixin, Base):
    __tablename__ = "product_attributes"
    id = Column(IdType, primary_key=True, autoincrement=True)
    product_id = Column(IdType, ForeignKey("products.id", ondelete="CASCADE"))
    hair_type = Column(String(100))
    ingredient = Column(Text)
    benefit = Column(Text)

    product = relationship("Product", back_populates="attributes")

class ProductImage(SoftDeleteMixin, Base):
    __tablename__ = "product_images"
    id = Column(IdType, primary_key=True, autoincrement=True)
    product_id = Column(IdType, ForeignKey("products.id", ondelete="CASCADE"))
    image_url = Column(Text)
    is_primary = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    product = relationship("Product", back_populates="images")

class Category(SoftDeleteMixin, Base):
    __tablename__ = "categories"
    id = Column(IdType, primary_key=True, autoincrement=True)
    name = Column(String(255))
    slug = Column(String(255), unique=True, index=True)
    parent_id = Column(IdType, ForeignKey("categories.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    parent = relationship("Category", remote_side=[id], backref="children")
    products = relationship("Product", secondary=product_categories, back_populates="categories")

class Cart(SoftDeleteMixin, Base):
    __tablename__ = "carts"
    id = Column(IdType, primary_key=True, autoincrement=True)
    user_id = Column(IdType, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    items = relationship("CartItem", back_populates="cart")

class CartItem(SoftDeleteMixin, Base):
    __tablename__ = "cart_items"
    id = Column(IdType, primary_key=True, autoincrement=True)
    cart_id = Column(IdType, ForeignKey("carts.id", ondelete="CASCADE"))
    product_id = Column(IdType, ForeignKey("products.id"))
    quantity = Column(BigInteger, default=1)
    price = Column(Numeric(12, 2))

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")

class Order(SoftDeleteMixin, Base):
    __tablename__ = "orders"
    id = Column(IdType, primary_key=True, autoincrement=True)
    user_id = Column(IdType, ForeignKey("users.id"))
    total_price = Column(Numeric(12, 2))
    shipping_fee = Column(Numeric(10, 2), default=0)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    payment_method = Column(Enum(PaymentMethod))
    shipping_address = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    coupons = relationship("Coupon", secondary=order_coupons, back_populates="orders")

class OrderItem(SoftDeleteMixin, Base):
    __tablename__ = "order_items"
    id = Column(IdType, primary_key=True, autoincrement=True)
    order_id = Column(IdType, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(IdType, ForeignKey("products.id"))
    quantity = Column(BigInteger)
    price = Column(Numeric(12, 2))

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Review(SoftDeleteMixin, Base):
    __tablename__ = "reviews"
    id = Column(IdType, primary_key=True, autoincrement=True)
    user_id = Column(IdType, ForeignKey("users.id"))
    product_id = Column(IdType, ForeignKey("products.id"))
    rating = Column(BigInteger)
    comment = Column(Text)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.pending)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_range'),)

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

class Coupon(SoftDeleteMixin, Base):
    __tablename__ = "coupons"
    id = Column(IdType, primary_key=True, autoincrement=True)
    code = Column(String(100), unique=True)
    discount_type = Column(Enum(DiscountType))
    discount_value = Column(Numeric(10, 2))
    expiry_date = Column(TIMESTAMP)
    usage_limit = Column(BigInteger)
    created_at = Column(TIMESTAMP, server_default=func.now())

    orders = relationship("Order", secondary=order_coupons, back_populates="coupons")

class BlogPost(SoftDeleteMixin, Base):
    __tablename__ = "blog_posts"
    id = Column(IdType, primary_key=True, autoincrement=True)
    title = Column(String(255))
    slug = Column(String(255), unique=True, index=True)
    content = Column(Text)
    image_url = Column(Text)
    seo_keyword = Column(String(255))
    status = Column(Enum(PostStatus))
    created_by = Column(IdType, ForeignKey("users.id"))
    updated_by = Column(IdType, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)

    creator = relationship("User", foreign_keys=[created_by], back_populates="blog_posts_created")
    updater = relationship("User", foreign_keys=[updated_by])

class Payment(SoftDeleteMixin, Base):
    __tablename__ = "payments"
    id = Column(IdType, primary_key=True, autoincrement=True)
    order_id = Column(IdType, ForeignKey("orders.id", ondelete="CASCADE"))
    amount = Column(Numeric(12, 2))
    method = Column(Enum(PaymentMethod))
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    transaction_id = Column(String(255), unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

class SEOMeta(SoftDeleteMixin, Base):
    __tablename__ = "seo_meta"
    id = Column(IdType, primary_key=True, autoincrement=True)
    page_type = Column(String(50))  # product, category, blog, home
    target_id = Column(IdType)  # ID of the product/blog
    meta_title = Column(String(255))
    meta_description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Brand(SoftDeleteMixin, Base):
    __tablename__ = "brands"
    id = Column(IdType, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True)
    slug = Column(String(150), unique=True)
    logo_url = Column(Text)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Shipment(SoftDeleteMixin, Base):
    __tablename__ = "shipments"
    id = Column(IdType, primary_key=True, autoincrement=True)
    order_id = Column(IdType, ForeignKey("orders.id", ondelete="CASCADE"))
    tracking_code = Column(String(100), unique=True)
    shipping_provider = Column(String(100))
    status = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

class Banner(SoftDeleteMixin, Base):
    __tablename__ = "banners"
    id = Column(IdType, primary_key=True, autoincrement=True)
    title = Column(String(255))
    image_url = Column(Text)
    redirect_url = Column(Text)
    position = Column(String(50)) # home_main, home_side, popup
    is_active = Column(Boolean, default=True)

class InventoryLog(SoftDeleteMixin, Base):
    __tablename__ = "inventory_logs"
    id = Column(IdType, primary_key=True, autoincrement=True)
    product_id = Column(IdType, ForeignKey("products.id"))
    quantity_before = Column(BigInteger)
    quantity_after = Column(BigInteger)
    action = Column(Enum(InventoryAction))
    note = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class AuditLog(SoftDeleteMixin, Base):
    __tablename__ = "audit_logs"
    id = Column(IdType, primary_key=True, autoincrement=True)
    admin_id = Column(IdType, ForeignKey("users.id"))
    action = Column(String(255))
    module = Column(String(100))
    payload = Column(Text) # JSON string of data
    ip_address = Column(String(45))
    created_at = Column(TIMESTAMP, server_default=func.now())

class UserProductInteraction(SoftDeleteMixin, Base):
    __tablename__ = "user_product_interactions"
    id = Column(IdType, primary_key=True, autoincrement=True)
    user_id = Column(IdType, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(IdType, ForeignKey("products.id", ondelete="CASCADE"))
    action = Column(String(20))  # view, click, add_to_cart, purchase
    timestamp = Column(TIMESTAMP, server_default=func.now())
    user = relationship("User", backref="interactions")
    product = relationship("Product", backref="interactions")
