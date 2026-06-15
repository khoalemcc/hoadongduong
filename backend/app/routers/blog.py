from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/blog",
    tags=["blog"],
)

@router.get("/", response_model=List[schemas.BlogPost])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_blog_posts(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.BlogPost)
def create_post(post: schemas.BlogPostCreate, db: Session = Depends(get_db)):
    return crud.create_blog_post(db=db, post=post)

@router.get("/{slug}", response_model=schemas.BlogPost)
def read_post_by_slug(slug: str, db: Session = Depends(get_db)):
    db_post = db.query(models.BlogPost).filter(models.BlogPost.slug == slug).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_post
