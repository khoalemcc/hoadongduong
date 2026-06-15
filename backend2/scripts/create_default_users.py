import os
import sys
# Add the backend2 project root to sys.path so that 'app' package can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import application modules
from app import models, auth, database
from sqlalchemy.orm import Session


def create_default_users():
    db: Session = database.SessionLocal()
    try:
        # Ensure admin role exists
        admin_role = db.query(models.Role).filter(models.Role.name == "admin").first()
        if not admin_role:
            admin_role = models.Role(name="admin", description="Administrator role")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
        # Ensure customer role exists
        customer_role = db.query(models.Role).filter(models.Role.name == "customer").first()
        if not customer_role:
            customer_role = models.Role(name="customer", description="Customer role")
            db.add(customer_role)
            db.commit()
            db.refresh(customer_role)
        # Create admin user if not exists
        admin_email = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@example.com")
        admin_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")
        admin_user = db.query(models.User).filter(models.User.email == admin_email).first()
        if not admin_user:
            admin_user = models.User(
                email=admin_email,
                password_hash=auth.get_password_hash(admin_password),
                full_name="Admin User",
                phone="1234567890"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        # Assign admin role
        if admin_role not in admin_user.roles:
            admin_user.roles.append(admin_role)
        # Create customer user if not exists
        cust_email = os.getenv("DEFAULT_CUSTOMER_EMAIL", "customer@example.com")
        cust_password = os.getenv("DEFAULT_CUSTOMER_PASSWORD", "cust123")
        cust_user = db.query(models.User).filter(models.User.email == cust_email).first()
        if not cust_user:
            cust_user = models.User(
                email=cust_email,
                password_hash=auth.get_password_hash(cust_password),
                full_name="Customer User",
                phone="0987654321"
            )
            db.add(cust_user)
            db.commit()
            db.refresh(cust_user)
        # Assign customer role
        if customer_role not in cust_user.roles:
            cust_user.roles.append(customer_role)
        db.commit()
        print("Default admin and customer accounts created.")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_users()
