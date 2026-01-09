from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# OTP is hardcoded to "1010" in local environment
TEST_OTP = "1010"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_send_otp():
    """Test sending OTP to email."""
    response = client.post(
        "/api/v1/auth/send-otp",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "OTP sent successfully"
    assert data["data"]["expires_in"] == 10


def test_register_user_with_otp():
    """Test user registration with OTP verification."""
    email = "testuser@example.com"
    
    # Step 1: Send OTP
    send_response = client.post(
        "/api/v1/auth/send-otp",
        json={"email": email}
    )
    assert send_response.status_code == 200
    
    # Step 2: Register with OTP
    response = client.post(
        "/api/v1/auth/verify-otp-register",
        json={
            "verify_request": {
                "email": email,
                "otp_code": TEST_OTP
            },
            "register_data": {
                "email": email,
                "full_name": "Test User",
                "country_code": "+1",
                "phone": "1234567890",
                "address": "123 Main St",
                "children": [],
                "terms_accepted": True
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["email"] == email
    assert data["data"]["full_name"] == "Test User"


def test_register_duplicate_email():
    """Test registration with duplicate email."""
    email = "duplicate@example.com"
    
    # First registration
    client.post(
        "/api/v1/auth/send-otp",
        json={"email": email}
    )
    client.post(
        "/api/v1/auth/verify-otp-register",
        json={
            "verify_request": {
                "email": email,
                "otp_code": TEST_OTP
            },
            "register_data": {
                "email": email,
                "full_name": "Test User",
                "country_code": "+1",
                "phone": "1234567890",
                "address": "123 Main St",
                "children": [],
                "terms_accepted": True
            }
        }
    )
    
    # Second registration with same email should fail
    client.post(
        "/api/v1/auth/send-otp",
        json={"email": email}
    )
    response = client.post(
        "/api/v1/auth/verify-otp-register",
        json={
            "verify_request": {
                "email": email,
                "otp_code": TEST_OTP
            },
            "register_data": {
                "email": email,
                "full_name": "Another User",
                "country_code": "+1",
                "phone": "9876543210",
                "address": "456 Oak St",
                "children": [],
                "terms_accepted": True
            }
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_with_otp():
    """Test user login with OTP."""
    email = "logintest@example.com"
    
    # Register user first
    client.post(
        "/api/v1/auth/send-otp",
        json={"email": email}
    )
    client.post(
        "/api/v1/auth/verify-otp-register",
        json={
            "verify_request": {
                "email": email,
                "otp_code": TEST_OTP
            },
            "register_data": {
                "email": email,
                "full_name": "Test User",
                "country_code": "+1",
                "phone": "1234567890",
                "address": "123 Main St",
                "children": [],
                "terms_accepted": True
            }
        }
    )
    
    # Login with OTP
    client.post(
        "/api/v1/auth/send-otp",
        json={"email": email}
    )
    response = client.post(
        "/api/v1/auth/verify-otp-login",
        json={
            "email": email,
            "otp_code": TEST_OTP
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]
    assert data["data"]["email"] == email


def test_login_with_invalid_otp():
    """Test login with invalid OTP."""
    email = "invalidotp@example.com"
    
    # Register user
    client.post(
        "/api/v1/auth/send-otp",
        json={"email": email}
    )
    client.post(
        "/api/v1/auth/verify-otp-register",
        json={
            "verify_request": {
                "email": email,
                "otp_code": TEST_OTP
            },
            "register_data": {
                "email": email,
                "full_name": "Test User",
                "country_code": "+1",
                "phone": "1234567890",
                "address": "123 Main St",
                "children": [],
                "terms_accepted": True
            }
        }
    )
    
    # Send OTP and try to login with wrong OTP
    client.post(
        "/api/v1/auth/send-otp",
        json={"email": email}
    )
    response = client.post(
        "/api/v1/auth/verify-otp-login",
        json={
            "email": email,
            "otp_code": "9999"
        }
    )
    assert response.status_code == 400
    assert "Invalid OTP" in response.json()["detail"]

