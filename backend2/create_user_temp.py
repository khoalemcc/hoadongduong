from app.database import SessionLocal
from app.models import User, Role
from app.auth import get_password_hash

def create_customer():
    db = SessionLocal()
    try:
        email = "lephananhkhoa@gmail.com"
        password = "@Kingdom9x"
        
        # Check if user exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"User {email} already exists.")
            return

        # Create user
        hashed_pw = get_password_hash(password)
        new_user = User(
            email=email,
            password_hash=hashed_pw,
            full_name="Le Phan Anh Khoa",
            phone="0123456789"
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"Successfully created customer: {email}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_customer()
