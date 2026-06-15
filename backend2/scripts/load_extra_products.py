import os
import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import pandas as pd
from app.database import SessionLocal, engine, Base
from app import models

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
extra_csv_path = os.path.join(BASE_DIR, 'extra_products.csv')

if not os.path.exists(extra_csv_path):
    raise FileNotFoundError(f"Extra products CSV not found at {extra_csv_path}")

def load_extra_products(csv_path: str):
    df = pd.read_csv(csv_path)
    df = df.where(pd.notnull(df), None)
    df = df.drop(columns=['created_at', 'updated_at'], errors='ignore')
    records = df.to_dict(orient='records')
    with SessionLocal() as session:
        for rec in records:
            if session.query(models.Product).filter_by(slug=rec.get('slug')).first():
                continue
            obj = models.Product(**rec)
            session.add(obj)
        session.commit()
    print(f"Loaded {len(records)} extra product rows into the database.")

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    load_extra_products(extra_csv_path)
