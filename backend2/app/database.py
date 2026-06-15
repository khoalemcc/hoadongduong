from sqlalchemy import create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

# Configure Connection Pooling (MySQL/PostgreSQL) or threading (SQLite)
engine_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}
else:
    engine_args.update({
        "pool_size": 20,
        "max_overflow": 10,
        "pool_recycle": 1800,
        "pool_pre_ping": True
    })

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def ensure_blog_post_columns():
    inspector = inspect(engine)
    if not inspector.has_table("blog_posts"):
        return
    columns = {column["name"] for column in inspector.get_columns("blog_posts")}
    if "image_url" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE blog_posts ADD COLUMN image_url TEXT"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
