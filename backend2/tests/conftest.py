import os

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("TESTING", "True")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import auth, models
from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


def auth_headers(client, email: str, password: str = "testpassword"):
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def make_user(client):
    def _make_user(email: str, password: str = "testpassword", **payload):
        response = client.post(
            "/users/",
            json={"email": email, "password": password, **payload},
        )
        assert response.status_code == 200
        return response.json(), auth_headers(client, email, password)

    return _make_user


@pytest.fixture
def admin_headers(db, client):
    admin_role = models.Role(name="admin", description="Administrator")
    admin_user = models.User(
        email="admin@example.com",
        password_hash=auth.get_password_hash("adminpassword"),
        roles=[admin_role],
    )
    db.add(admin_user)
    db.commit()
    return auth_headers(client, "admin@example.com", "adminpassword")
