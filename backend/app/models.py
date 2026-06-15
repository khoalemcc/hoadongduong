from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Numeric, TIMESTAMP, Enum, Table, BigInteger, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

# Enums
class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    banned = "banned"

class OrderStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipping = "shipping"
    completed = "completed"
    cancelled = "cancelled"

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
    Column("user_id", BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", BigInteger, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
)

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", BigInteger, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", BigInteger, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)
)

order_coupons = Table(
    "order_coupons",
    Base.metadata,
    Column("order_id", BigInteger, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True),
    Column("coupon_id", BigInteger, ForeignKey("coupons.id", ondelete="CASCADE"), primary_key=True)
)

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    status = Column(Enum(UserStatus), default=UserStatus.active)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    addresses = relationship("UserAddress", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    blog_posts_created = relationship("BlogPost", foreign_keys="BlogPost.created_by", back_populates="creator")
    orders = relationship("Order", back_populates="user")

class Role(Base):
    __tablename__ = "roles"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)
    description = Column(Text)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class UserAddress(Base):
    __tablename__ = "user_addresses"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    full_name = Column(String(255))
    phone = Column(String(20))
    address_line = Column(Text)
    city = Column(String(100))
    district = Column(String(100))
    ward = Column(String(100))
    is_default = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="addresses")

class Product(Base):
    __tablename__ = "products"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))
    slug = Column(String(255), unique=True, index=True)
    description = Column(Text)
    price = Column(Numeric(12, 2))
    stock = Column(Integer, default=0)
    brand = Column(String(150))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    attributes = relationship("ProductAttribute", back_populates="product", uselist=False)
    images = relationship("ProductImage", back_populates="product")
    categories = relationship("Category", secondary=product_categories, back_populates="products")
    reviews = relationship("Review", back_populates="product")

class ProductAttribute(Base):
    __tablename__ = "product_attributes"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"))
    hair_type = Column(String(100))
    ingredient = Column(Text)
    benefit = Column(Text)

    product = relationship("Product", back_populates="attributes")

class ProductImage(Base):
    __tablename__ = "product_images"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"))
    image_url = Column(Text)
    is_primary = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    product = relationship("Product", back_populates="images")

class Category(Base):
    __tablename__ = "categories"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))
    slug = Column(String(255), unique=True, index=True)
    parent_id = Column(BigInteger, ForeignKey("categories.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    parent = relationship("Category", remote_side=[id], backref="children")
    products = relationship("Product", secondary=product_categories, back_populates="categories")

class Cart(Base):
    __tablename__ = "carts"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    items = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cart_id = Column(BigInteger, ForeignKey("carts.id", ondelete="CASCADE"))
    product_id = Column(BigInteger, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price = Column(Numeric(12, 2))

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    total_price = Column(Numeric(12, 2))
    status = Column(Enum(OrderStatus))
    payment_method = Column(Enum(PaymentMethod))
    shipping_address = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    coupons = relationship("Coupon", secondary=order_coupons, back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(BigInteger, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Numeric(12, 2))

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    product_id = Column(BigInteger, ForeignKey("products.id"))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_range'),)

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(100), unique=True)
    discount_type = Column(Enum(DiscountType))
    discount_value = Column(Numeric(10, 2))
    expiry_date = Column(TIMESTAMP)
    usage_limit = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())

    orders = relationship("Order", secondary=order_coupons, back_populates="coupons")

class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255))
    slug = Column(String(255), unique=True, index=True)
    content = Column(Text)
    seo_keyword = Column(String(255))
    status = Column(Enum(PostStatus))
    created_by = Column(BigInteger, ForeignKey("users.id"))
    updated_by = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)

    creator = relationship("User", foreign_keys=[created_by], back_populates="blog_posts_created")
    updater = relationship("User", foreign_keys=[updated_by])
