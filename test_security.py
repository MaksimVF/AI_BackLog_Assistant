


import pytest
from fastapi.testclient import TestClient
from api.main import app
from security.user_db import user_db
from models.user import UserCreate, UserRole

client = TestClient(app)

def test_register_user():
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "role": "user"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

def test_login_user():
    """Test user login and token generation"""
    # First register a user
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
    )

    # Then login
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_admin_access_denied():
    """Test that non-admin users cannot access admin endpoints"""
    # Register a regular user
    client.post(
        "/auth/register",
        json={
            "username": "regularuser",
            "email": "regular@example.com",
            "password": "regularpassword"
        }
    )

    # Login to get token
    login_response = client.post(
        "/auth/token",
        data={"username": "regularuser", "password": "regularpassword"}
    )
    token = login_response.json()["access_token"]

    # Try to access admin endpoint
    response = client.post(
        "/admin/command",
        json={"command": "test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

def test_admin_access_allowed():
    """Test that admin users can access admin endpoints"""
    # Register an admin user
    client.post(
        "/auth/register",
        json={
            "username": "adminuser",
            "email": "admin@example.com",
            "password": "adminpassword",
            "role": "admin"
        }
    )

    # Login to get token
    login_response = client.post(
        "/auth/token",
        data={"username": "adminuser", "password": "adminpassword"}
    )
    token = login_response.json()["access_token"]

    # Access admin endpoint
    response = client.post(
        "/admin/command",
        json={"command": "test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

