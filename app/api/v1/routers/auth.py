from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db_sync
from app.schemas.auth_schema import (
    SignupRequest, SignupResponse, SigninRequest, VerifyOTPRequest,
    VerifyOTPResponse
)
from app.schemas.response import SuccessResponse
from app.services.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/signup", response_model=SuccessResponse[SignupResponse], status_code=status.HTTP_201_CREATED)
def signup(request: SignupRequest, db: Session = Depends(get_db_sync)):
    """Register a new user and send OTP to email and phone.
    
    Creates an inactive user and sends OTP to both email and phone number.
    """
    try:
        result = AuthService.signup(db, request)
        return SuccessResponse(
            status="success",
            message="OTP sent to email and phone",
            data=result
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Signup failed"
        )


@router.post("/signin", response_model=SuccessResponse[dict])
def signin(request: SigninRequest, db: Session = Depends(get_db_sync)):
    """Request OTP for login via email or phone.
    
    Provide either email or phone (at least one required).
    OTP will be sent to the provided contact method.
    """
    try:
        result = AuthService.signin(db, request)
        return SuccessResponse(
            status="success",
            message="OTP sent successfully",
            data=result
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signin error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Signin failed"
        )


@router.post("/verify-otp", response_model=SuccessResponse[VerifyOTPResponse])
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db_sync)):
    """Verify OTP for both signup completion and signin.
    
    Provide email or phone with the OTP code.
    Returns JWT token for signin or completes signup for new users.
    """
    try:
        result = AuthService.verify_otp(db, request)
        return SuccessResponse(
            status="success",
            message="OTP verified successfully",
            data=result
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OTP verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OTP verification failed"
        )


@router.post("/resend-otp", response_model=SuccessResponse[dict])
def resend_otp(request: SigninRequest, db: Session = Depends(get_db_sync)):
    """Resend OTP for signup or signin.
    
    Provide either email or phone (at least one required).
    Generates a new OTP and sends it to the provided contact method.
    """
    try:
        result = AuthService.resend_otp(db, request)
        return SuccessResponse(
            status="success",
            message="OTP resent successfully",
            data=result
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resend OTP error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Resend OTP failed"
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