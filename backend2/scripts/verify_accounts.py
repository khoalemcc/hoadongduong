import sys, os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import models, database

def main():
    db = database.SessionLocal()
    try:
        emails = ["admin@example.com", "customer@example.com"]
        users = db.query(models.User).filter(models.User.email.in_(emails)).all()
        if not users:
            print("No matching users found.")
            return
        for user in users:
            role_names = [role.name for role in user.roles]
            print(f"User: {user.email}, Roles: {', '.join(role_names) if role_names else 'None'}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
