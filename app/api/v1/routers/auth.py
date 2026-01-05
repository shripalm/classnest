from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db_sync
from app.schemas.auth_schema import (
    UserCreate, UserLogin, UserResponse, AuthResponse, 
    LoginRequest, RegisterRequest, LoginResponse, RegisterResponse
)
from app.schemas.response import SuccessResponse
from app.services.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def sign_up(user_data: UserCreate, db: Session = Depends(get_db_sync)):
    """Register a new user with children.
    
    Expected payload:
    {
        "parent": {
            "name": "John Doe",
            "email": "john@example.com",
            "countryCode": "+1",
            "phone": "1234567890",
            "password": "SecurePass123",
            "confirmPassword": "SecurePass123",
            "address": "123 Main St"
        },
        "children": [
            {
                "name": "Jane Doe",
                "dateOfBirth": "14/02/2002",
                "gender": "Female",
                "photo": "url_or_base64",
                "interest": "Reading"
            }
        ],
        "termsAccepted": true
    }
    """
    try:
        return AuthService.sign_up(db, user_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/signin", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def sign_in(credentials: UserLogin, db: Session = Depends(get_db_sync)):
    """Sign in user with email and password.
    
    Expected payload:
    {
        "credentials": {
            "email": "john@example.com",
            "password": "SecurePass123"
        },
        "rememberMe": false
    }
    """
    try:
        return AuthService.sign_in(db, credentials)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signin error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: str, db: Session = Depends(get_db_sync)):
    """Soft delete a user account by user ID.
    
    This endpoint performs a soft delete - the user record is marked as deleted
    but not permanently removed from the database.
    
    Args:
        user_id: The UUID of the user to delete
    
    Returns:
        A success response with deletion timestamp
    """
    try:
        return AuthService.soft_delete_user(db, user_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )