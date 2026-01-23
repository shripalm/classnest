from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db_sync
from app.schemas.auth_schema import (
    SignupRequest, SignupResponse, SigninRequest, VerifyOTPRequest,
    VerifyOTPResponse, UserResponse, InitiateDeleteRequest, VerifyDeleteRequest,
    DeleteResponse
)
from app.schemas.response import SuccessResponse, PaginatedResponse
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.utils.pagination import PaginationParams
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


@router.get("/users", response_model=PaginatedResponse[UserResponse])
def get_all_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    include_deleted: bool = Query(False, description="Include soft-deleted users"),
    db: Session = Depends(get_db_sync)
):
    """Get all users with pagination.
    
    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20, max: 100)
    - **include_deleted**: Include soft-deleted users (default: false)
    """
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        users, total = UserRepository.get_all_users(
            db,
            skip=pagination.skip,
            limit=pagination.limit,
            include_deleted=include_deleted
        )
        
        pagination_data = pagination.get_pagination_data(total)
        user_responses = [UserResponse.from_orm(user) for user in users]
        
        return PaginatedResponse(
            status="success",
            message="Users retrieved successfully",
            data=user_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.get("/users/{user_id}", response_model=SuccessResponse[UserResponse])
def get_user_profile(user_id: str, db: Session = Depends(get_db_sync)):
    """Get a specific user's profile by ID.
    
    Args:
        user_id: The UUID of the user to retrieve
    
    Returns:
        User profile with all details
    """
    try:
        user = UserRepository.get_user_by_id(db, user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_response = UserResponse.from_orm(user)
        return SuccessResponse(
            status="success",
            message="User profile retrieved successfully",
            data=user_response
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )


@router.post("/delete-account/initiate", response_model=SuccessResponse[dict])
def initiate_account_deletion(request: InitiateDeleteRequest, db: Session = Depends(get_db_sync)):
    """Initiate account deletion process.
    
    Accepts email or mobile number and sends OTP to the user.
    
    Args:
        request: Contains email or phone number
    
    Returns:
        Success message with OTP expiration time
    """
    try:
        result = AuthService.initiate_account_deletion(db, email=request.email, phone=request.phone)
        return SuccessResponse(
            status="success",
            message="OTP sent successfully",
            data=result
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initiating account deletion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate account deletion"
        )


@router.post("/delete-account/verify", response_model=SuccessResponse[DeleteResponse])
def verify_and_delete_account(request: VerifyDeleteRequest, db: Session = Depends(get_db_sync)):
    """Verify OTP and delete user account.
    
    After verifying the OTP code, the user account is soft-deleted.
    
    Args:
        request: Contains email or phone, and OTP code
    
    Returns:
        Success message with deleted user details
    """
    try:
        result = AuthService.verify_and_delete_account(db, email=request.email, phone=request.phone, otp_code=request.otp_code)
        return SuccessResponse(
            status="success",
            message="Account deleted successfully",
            data=result
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying and deleting account: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )
