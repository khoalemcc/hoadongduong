# etl.py
"""ETL script to load synthetic CSV data into the database.
Assumes CSV files are located in ../data/ (relative to this script).
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Product, Order, OrderItem, UserProductInteraction
from app.database import DATABASE_URL

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def load_users(session):
    df = pd.read_csv(os.path.join(BASE_DIR, "users.csv"))
    for _, row in df.iterrows():
        user = User(
            id=row["id"],
            email=row["email"],
            full_name=row["full_name"],
            phone=row["phone"],
            gender=row["gender"],
            birthday=row["birthday"],
            status="active",
        )
        session.merge(user)
    session.commit()

def load_products(session):
    df = pd.read_csv(os.path.join(BASE_DIR, "products.csv"))
    for _, row in df.iterrows():
        product = Product(
            id=row["id"],
            sku=row["sku"],
            name=row["name"],
            slug=row["slug"],
            description=row["description"],
            price=row["price"],
            stock=row["stock"],
            is_active=row["is_active"],
        )
        session.merge(product)
    session.commit()

def load_orders(session):
    orders_df = pd.read_csv(os.path.join(BASE_DIR, "orders.csv"))
    items_df = pd.read_csv(os.path.join(BASE_DIR, "order_items.csv"))
    for _, row in orders_df.iterrows():
        order = Order(
            id=row["id"],
            user_id=row["user_id"],
            total_price=row["total_price"],
            shipping_fee=row["shipping_fee"],
            status=row["status"],
            payment_status=row["payment_status"],
            payment_method=row["payment_method"],
            shipping_address=row["shipping_address"],
            created_at=row["created_at"],
        )
        session.merge(order)
    session.commit()
    # load order items
    for _, row in items_df.iterrows():
        item = OrderItem(
            order_id=row["order_id"],
            product_id=row["product_id"],
            quantity=row["quantity"],
            price=row["price"],
        )
        session.merge(item)
    session.commit()

def load_interactions(session):
    df = pd.read_csv(os.path.join(BASE_DIR, "interactions.csv"))
    for _, row in df.iterrows():
        interaction = UserProductInteraction(
            user_id=row["user_id"],
            product_id=row["product_id"],
            action=row["action"],
            timestamp=row["timestamp"],
        )
        session.merge(interaction)
    session.commit()

def main():
    # ensure tables exist
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    load_users(session)
    load_products(session)
    load_orders(session)
    load_interactions(session)
    session.close()

if __name__ == "__main__":
    main()
