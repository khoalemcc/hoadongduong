from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import users, products, orders, cart, blog

# Create database tables if they don't exist
# Note: In production, use migrations like Alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hoa Dong Duong E-Commerce API",
    description="Backend API for Hoa Dong Duong marketplace",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.include_router(blog.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Hoa Dong Duong API"}
