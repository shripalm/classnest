from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user():
    """Test user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["email"] == "test@example.com"
    assert data["data"]["username"] == "testuser"


def test_register_duplicate_email():
    """Test registration with duplicate email."""
    # First registration
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
    )
    
    # Second registration with same email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "anotheruser",
            "password": "TestPassword123!",
            "full_name": "Another User"
        }
    )
    assert response.status_code == 400


def test_login():
    """Test user login."""
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email_or_username": "test@example.com",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]
    assert data["data"]["email"] == "test@example.com"


def test_login_with_invalid_credentials():
    """Test login with invalid credentials."""
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
    )
    
    # Login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email_or_username": "test@example.com",
            "password": "WrongPassword"
        }
    )
    assert response.status_code == 401
