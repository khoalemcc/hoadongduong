from sqlalchemy import text
from app.database import engine, SessionLocal
from app.models import Base

def clear_data():
    db = SessionLocal()
    try:
        print("--- Clearing Tables ---")
        # Disable foreign key checks for MySQL
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        
        # Get all table names from Base metadata
        for table in reversed(Base.metadata.sorted_tables):
            print(f"Clearing table: {table.name}")
            db.execute(table.delete())
        
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        db.commit()
        print("--- Database Cleared Successfully ---")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_data()
