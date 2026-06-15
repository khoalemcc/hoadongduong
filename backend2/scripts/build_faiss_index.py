# build_faiss_index.py
"""Generate FAISS index for product recommendation.
Uses SentenceTransformer to embed product name + description.
Saves:
- faiss_index.bin (binary index)
- faiss_meta.json (mapping from index id -> product_id)
"""
import os
import json
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
PRODUCT_CSV = os.path.join(BASE_DIR, "products.csv")
INDEX_PATH = os.path.join(BASE_DIR, "faiss_index.bin")
META_PATH = os.path.join(BASE_DIR, "faiss_meta.json")

# Load model (lightweight)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load product data
print(f"Loading products from {PRODUCT_CSV}")
products = pd.read_csv(PRODUCT_CSV)
texts = (products['name'].fillna('') + ' ' + products['description'].fillna('')).tolist()

# Encode
embeddings = model.encode(texts, normalize_embeddings=True)
embeddings = embeddings.astype('float32')

# Build index (inner product for similarity)
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# Save index
faiss.write_index(index, INDEX_PATH)
print(f"FAISS index saved to {INDEX_PATH}")

# Save meta mapping
meta = {str(i): int(pid) for i, pid in enumerate(products['id'])}
with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump(meta, f)
print(f"Metadata saved to {META_PATH}")
