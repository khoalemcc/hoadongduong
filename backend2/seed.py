import random
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models, auth

def seed_data():
    # Ensure all tables are created (especially new ones like brands, shipments, etc.)
    print("Resetting database tables for a clean test state...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Brands
        print("Seeding Brands...")
        brands = []
        for i in range(20):
            brand = models.Brand(
                name=f"Brand {i+1}",
                slug=f"brand-{i+1}",
                logo_url=f"https://placehold.co/200x200?text=Brand+{i+1}",
                description=f"Premium brand partnership number {i+1}"
            )
            db.add(brand)
            brands.append(brand)
        db.flush()

        # 2. Categories
        print("Seeding Categories...")
        categories = []
        for i in range(20):
            category = models.Category(
                name=f"Category {i+1}",
                slug=f"category-{i+1}"
            )
            db.add(category)
            categories.append(category)
        db.flush()

        # 3. Products
        print("Seeding Products...")
        products = []
        for i in range(20):
            product = models.Product(
                sku=f"HDD-PROD-{i+1:03d}",
                name=f"Product Name {i+1}",
                slug=f"product-name-{i+1}",
                description=f"Detailed description for high-quality product {i+1}",
                price=Decimal(random.randint(100000, 5000000)),
                stock=random.randint(10, 100),
                brand_id=random.choice(brands).id,
                is_active=True
            )
            db.add(product)
            products.append(product)
        db.flush()

        # 4. Users
        print("Seeding Users...")
        users = []
        for i in range(20):
            user = models.User(
                email=f"user{i+1}@example.com",
                password_hash=auth.get_password_hash("password123"),
                full_name=f"Customer Full Name {i+1}",
                phone=f"098765432{i:02d}",
                status=models.UserStatus.active
            )
            db.add(user)
            users.append(user)
        # 5. Admin and Roles
        print("Seeding Admin and Roles...")
        super_admin_role = models.Role(name="Super Admin", description="Full system access")
        db.add(super_admin_role)
        db.flush()

        admin_user = models.User(
            email="admin@verdant.com",
            password_hash=auth.get_password_hash("@Kingdom9x"),
            full_name="Super Administrator",
            phone="0900000000",
            status=models.UserStatus.active
        )
        admin_user.roles.append(super_admin_role)
        db.add(admin_user)

        # User's specific account
        user_khoa = models.User(
            email="lephananhkhoa@gmail.com",
            password_hash=auth.get_password_hash("@Kingdom9x"),
            full_name="Le Phan Anh Khoa",
            phone="0912345678",
            status=models.UserStatus.active
        )
        user_khoa.roles.append(super_admin_role)
        db.add(user_khoa)
        
        db.flush()

        # Update users list for order seeding
        users.extend([admin_user, user_khoa])

        # 5. Orders
        print("Seeding Orders...")
        orders = []
        for i in range(20):
            order = models.Order(
                user_id=random.choice(users).id,
                total_price=Decimal(0), # Calculate later
                shipping_fee=Decimal(30000),
                status=random.choice(list(models.OrderStatus)),
                payment_status=random.choice(list(models.PaymentStatus)),
                payment_method=random.choice(list(models.PaymentMethod)),
                shipping_address=f"{i+1} Hoa Dong Duong St, District {random.randint(1,12)}"
            )
            db.add(order)
            db.flush()
            
            # Order Items
            total = Decimal(0)
            for _ in range(random.randint(1, 3)):
                p = random.choice(products)
                qty = random.randint(1, 2)
                item_price = p.price
                item = models.OrderItem(
                    order_id=order.id,
                    product_id=p.id,
                    quantity=qty,
                    price=item_price
                )
                db.add(item)
                total += item_price * qty
            
            order.total_price = total + order.shipping_fee
            orders.append(order)
        db.flush()

        # 6. Reviews
        print("Seeding Reviews...")
        for i in range(20):
            review = models.Review(
                user_id=random.choice(users).id,
                product_id=random.choice(products).id,
                rating=random.randint(4, 5),
                comment=f"Excellent product quality! Recommended! {i+1}",
                status=models.ReviewStatus.approved
            )
            db.add(review)

        # 7. Banners
        print("Seeding Banners...")
        positions = ["home_main", "home_side", "popup"]
        for i in range(20):
            banner = models.Banner(
                title=f"Promotion Banner {i+1}",
                image_url=f"https://placehold.co/1200x400?text=Campaign+{i+1}",
                redirect_url="/shop",
                position=random.choice(positions),
                is_active=True
            )
            db.add(banner)

        # 8. Blog Posts
        print("Seeding Blog Posts...")
        for i in range(20):
            post = models.BlogPost(
                title=f"The Future of E-Commerce {i+1}",
                slug=f"future-ecommerce-{i+1}",
                content=f"Content for blog post {i+1}. Discover the latest trends in technology and design.",
                status=models.PostStatus.published,
                created_by=users[0].id,
                updated_by=users[0].id
            )
            db.add(post)

        # 9. Inventory Logs
        print("Seeding Inventory Logs...")
        for i in range(20):
            log = models.InventoryLog(
                product_id=random.choice(products).id,
                quantity_before=100,
                quantity_after=random.randint(80, 120),
                action=random.choice(list(models.InventoryAction)),
                note="Initial seed data log"
            )
            db.add(log)

        # 10. Audit Logs
        print("Seeding Audit Logs...")
        for i in range(20):
            audit = models.AuditLog(
                admin_id=users[0].id,
                action="CREATE_RECORD",
                module="SEEDER",
                payload="{\"action\": \"seed\"}",
                ip_address="127.0.0.1"
            )
            db.add(audit)

        db.commit()
        print("Successfully seeded all tables with 20 records each!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
