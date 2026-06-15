import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.database import engine, Base, ensure_blog_post_columns
from app.routers import users, products, orders, cart, blog, auth, admin
from app.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("app.main")

# Ensure static directory exists
if not os.path.exists("static/images"):
    os.makedirs("static/images", exist_ok=True)

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)
ensure_blog_post_columns()

app = FastAPI(
    title="Hoa Dong Duong E-Commerce API V2",
    description="Backend API for Hoa Dong Duong marketplace (Database: hh)",
    version="2.0.0"
)

# Attach limiter and error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code >= 500:
        logger.error(f"HTTP {exc.status_code} error on {request.method} {request.url.path}: {exc.detail}")
    else:
        logger.info(f"HTTP {exc.status_code} client error on {request.method} {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.critical(
        f"Unhandled exception on {request.method} {request.url.path}: {exc}",
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred."}
    )

cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    if origin.strip()
]

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
from app.routers import auth, users, products, orders, cart, blog, admin, reviews, admin_ops, content_factory, recommend

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.include_router(blog.router)
app.include_router(admin.router)
app.include_router(admin_ops.router)
app.include_router(recommend.router)
app.include_router(content_factory.router)
app.include_router(reviews.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Hoa Dong Duong API V2"}
