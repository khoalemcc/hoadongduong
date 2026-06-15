import pytest
from app import auth, models

def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "phone": "0123456789",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_user_duplicate_email(client):
    # First creation
    client.post(
        "/users/",
        json={
            "email": "dup@example.com",
            "password": "testpassword"
        }
    )
    # Duplicate creation
    response = client.post(
        "/users/",
        json={
            "email": "dup@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_read_user(client, make_user):
    user, headers = make_user("read@example.com", "abc")

    response = client.get(f"/users/{user['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "read@example.com"


def test_role_name_containing_admin_is_not_admin(client, db):
    role = models.Role(name="notadmin", description="Should not grant admin")
    user = models.User(
        email="notadmin@example.com",
        password_hash=auth.get_password_hash("testpassword"),
        roles=[role],
    )
    db.add(user)
    db.commit()

    login = client.post(
        "/auth/login",
        data={"username": "notadmin@example.com", "password": "testpassword"},
    )
    assert login.status_code == 200
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.get("/users/", headers=headers)
    assert response.status_code == 403
