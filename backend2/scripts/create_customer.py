import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
from app.models import User, Role
from app.auth import get_password_hash


def create_or_update_customer(email: str, password: str):

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # create new user
            user = User(email=email, password_hash=get_password_hash(password))
            db.add(user)
            db.flush()  # assign id
            # ensure role exists
            role = db.query(Role).filter(Role.name.ilike('customer')).first()
            if not role:
                role = Role(name='customer', description='Customer')
                db.add(role)
                db.flush()
            user.roles.append(role)
            db.commit()
            print(f"✅ Created customer user {email}")
        else:
            user.password_hash = get_password_hash(password)
            db.commit()
            print(f"✅ Updated password for existing user {email}")
    finally:
        db.close()

if __name__ == "__main__":
    create_or_update_customer("khoale.mcc@gmail.com", "1234")
