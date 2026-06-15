import os
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product, UserProductInteraction
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

router = APIRouter(prefix="/recommend", tags=["Recommendation"])

# Lazy-load model
_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

# Base directory (two levels up) to data folder
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
INDEX_PATH = os.path.join(BASE_DIR, "faiss_index.bin")
META_PATH = os.path.join(BASE_DIR, "faiss_meta.json")

def load_faiss_index():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        raise RuntimeError("FAISS index or metadata not found. Build it first.")
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return index, meta

_index_cache = None

def get_faiss():
    global _index_cache
    if _index_cache is None:
        _index_cache = load_faiss_index()
    return _index_cache

@router.get("/user/{user_id}", response_model=list[int])
def recommend_for_user(
    user_id: int,
    db: Session = Depends(get_db),
    top_k: int = 5,
):
    # Ensure user exists
    user_interaction = (
        db.query(UserProductInteraction)
        .filter(UserProductInteraction.user_id == user_id)
        .first()
    )
    if not user_interaction:
        raise HTTPException(status_code=404, detail="User not found or no interactions")

    recent = (
        db.query(UserProductInteraction)
        .filter(UserProductInteraction.user_id == user_id)
        .order_by(UserProductInteraction.timestamp.desc())
        .limit(10)
        .all()
    )
    if not recent:
        raise HTTPException(status_code=404, detail="No interaction data for user")

    # Build query embedding from product names of recent interactions
    texts = []
    for r in recent:
        prod = db.query(Product).filter(Product.id == r.product_id).first()
        if prod:
            texts.append(f"{prod.name} {prod.description}")
    if not texts:
        raise HTTPException(status_code=404, detail="No valid products in interactions")

    model = get_model()
    query_vec = model.encode(texts, normalize_embeddings=True)
    query_vec = np.mean(query_vec, axis=0).astype("float32").reshape(1, -1)

    index, meta = get_faiss()
    distances, indices = index.search(query_vec, top_k)
    product_ids = [meta[str(idx)] for idx in indices[0] if str(idx) in meta]
    return product_ids
