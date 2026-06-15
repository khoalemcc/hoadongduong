import os
import random
from faker import Faker
import pandas as pd

fake = Faker()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
os.makedirs(BASE_DIR, exist_ok=True)

NUM_EXTRA = 100
products = []
for i in range(1, NUM_EXTRA + 1):
    name = fake.word().title() + " " + fake.word().title()
    sku = f"EXTRA{i:05d}"
    price = round(random.uniform(5, 200), 2)
    stock = random.randint(0, 100)
    description = fake.sentence(nb_words=12)
    slug = f"extra-{i}-{name.lower().replace(' ', '-') }"
    products.append({
        "sku": sku,
        "name": name,
        "slug": slug,
        "description": description,
        "price": price,
        "stock": stock,
        "is_active": True,
    })

pd.DataFrame(products).to_csv(os.path.join(BASE_DIR, "extra_products.csv"), index=False)
print(f"Generated {NUM_EXTRA} extra products in {BASE_DIR}")
