# generate_fake_data.py
"""Generate synthetic data for the Hoa Dong Duong project.
Creates CSV files under `data/` directory:
- products.csv
- users.csv
- orders.csv
- interactions.csv (user‑product clicks/purchases)
"""

import os
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

fake = Faker()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(BASE_DIR, exist_ok=True)

# ------------------- Products -------------------
NUM_PRODUCTS = 200
products = []
for i in range(1, NUM_PRODUCTS + 1):
    name = fake.word().title() + " " + fake.word().title()
    sku = f"SKU{i:05d}"
    price = round(random.uniform(10, 500), 2)
    stock = random.randint(0, 200)
    description = fake.sentence(nb_words=12)
    products.append({
        "id": i,
        "sku": sku,
        "name": name,
        "slug": name.lower().replace(' ', '-') + f"-{i}",
        "description": description,
        "price": price,
        "stock": stock,
        "is_active": True,
    })
pd.DataFrame(products).to_csv(os.path.join(BASE_DIR, "products.csv"), index=False)

# ------------------- Users -------------------
NUM_USERS = 100
users = []
for i in range(1, NUM_USERS + 1):
    email = fake.unique.email()
    full_name = fake.name()
    phone = fake.phone_number()
    gender = random.choice(["male", "female", "other"])
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=70)
    users.append({
        "id": i,
        "email": email,
        "full_name": full_name,
        "phone": phone,
        "gender": gender,
        "birthday": birthday,
        "status": "active",
    })
pd.DataFrame(users).to_csv(os.path.join(BASE_DIR, "users.csv"), index=False)

# ------------------- Orders -------------------
NUM_ORDERS = 300
orders = []
order_items = []
for i in range(1, NUM_ORDERS + 1):
    user_id = random.randint(1, NUM_USERS)
    created_at = fake.date_time_between(start_date="-180d", end_date="now")
    total_price = 0
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        product = random.choice(products)
        qty = random.randint(1, 3)
        price = product["price"] * qty
        total_price += price
        order_items.append({
            "order_id": i,
            "product_id": product["id"],
            "quantity": qty,
            "price": price,
        })
    orders.append({
        "id": i,
        "user_id": user_id,
        "total_price": round(total_price, 2),
        "shipping_fee": round(random.uniform(0, 20), 2),
        "status": random.choice(["pending", "confirmed", "shipping", "completed"]),
        "payment_status": random.choice(["paid", "pending"]),
        "payment_method": random.choice(["cod", "bank", "momo", "vnpay"]),
        "created_at": created_at,
    })
pd.DataFrame(orders).to_csv(os.path.join(BASE_DIR, "orders.csv"), index=False)
pd.DataFrame(order_items).to_csv(os.path.join(BASE_DIR, "order_items.csv"), index=False)

# ------------------- Interactions -------------------
# Simulate clicks and purchases (type: click=0, purchase=1)
interactions = []
for user_id in range(1, NUM_USERS + 1):
    # each user interacts with 10‑20 products
    for _ in range(random.randint(10, 20)):
        product_id = random.randint(1, NUM_PRODUCTS)
        interaction_type = random.choices([0, 1], weights=[0.8, 0.2])[0]
        timestamp = fake.date_time_between(start_date="-180d", end_date="now")
        interactions.append({
            "user_id": user_id,
            "product_id": product_id,
            "interaction_type": interaction_type,
            "timestamp": timestamp,
        })
pd.DataFrame(interactions).to_csv(os.path.join(BASE_DIR, "interactions.csv"), index=False)

print("Fake data generated in", BASE_DIR)
