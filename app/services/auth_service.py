from sqlalchemy.orm import Session
from app.schemas.auth_schema import (
    UserCreate, UserResponse, RegisterResponse, SignupRequest, 
    SigninRequest, VerifyOTPRequest
)
from app.repositories.user_repository import UserRepository
from app.repositories.child_repository import ChildRepository
from app.repositories.otp_repository import OTPRepository
from app.models.otp import OTP
from app.core.security import create_access_token
from app.core.config import settings
from fastapi import HTTPException, status
from datetime import datetime
import logging
import random
import string

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def generate_otp() -> str:
        """Generate OTP code."""
        # In local environment, return hardcoded OTP
        if settings.APP_ENV == "local":
            return "1010"
        
        # In production, generate random OTP
        return ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))

    @staticmethod
    def signup(db: Session, request: SignupRequest) -> dict:
        """Register a new user and send OTP to email and phone.
        
        Creates an inactive user and sends OTP to both email and phone.
        """
        # Check if email already exists (for non-deleted users)
        if UserRepository.email_exists(db, request.email):
            logger.warning(f"Signup attempt with existing email: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if phone already exists (for non-deleted users)
        if request.phone and UserRepository.phone_exists(db, request.phone):
            logger.warning(f"Signup attempt with existing phone: {request.phone}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
        
        # Create user from signup request (convert to UserCreate)
        user_create = UserCreate(
            full_name=request.full_name,
            email=request.email,
            country_code=request.country_code,
            phone=request.phone,
            address=request.address,
            children=request.children,
            terms_accepted=request.terms_accepted
        )
        
        # Create user (inactive)
        db_user = UserRepository.create_user_otp(db, request.email, user_create)
        logger.info(f"New user created (inactive): {db_user.email}")
        
        # Generate OTP
        otp_code = AuthService.generate_otp()
        
        # Create OTP record with email and phone
        otp = OTPRepository.create_otp(db, request.email, otp_code, phone=request.phone)
        logger.info(f"OTP generated for user: {request.email}")
        
        # TODO: Send OTP via email and SMS (integrate with SendGrid and SMS service)
        logger.debug(f"OTP for {request.email}: {otp_code}")
        logger.debug(f"OTP for phone {request.phone}: {otp_code}")
        
        return {
            "user_id": str(db_user.id),
            "message": "OTP sent to email and phone",
            "otp_expires_in": settings.OTP_EXPIRE_MINUTES
        }

    @staticmethod
    def signin(db: Session, request: SigninRequest) -> dict:
        """Request OTP for login via email or phone.
        
        User provides either email or phone. OTP is sent to the provided contact.
        """
        # Validate that at least one contact method is provided
        if not request.email and not request.phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either email or phone is required"
            )
        
        # Determine which contact to use
        contact_email = request.email
        contact_phone = request.phone
        
        # If email provided, try to find user by email
        if contact_email:
            user = UserRepository.get_user_by_email(db, contact_email)
        # If only phone provided, search by phone
        elif contact_phone:
            user = UserRepository.get_user_by_phone(db, contact_phone)
        else:
            user = None
        
        if not user:
            logger.warning(f"Signin attempt with non-existent contact: {contact_email or contact_phone}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_verified:
            logger.warning(f"Signin attempt for unverified user: {contact_email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account not verified. Please complete signup."
            )
        
        # Generate OTP
        otp_code = AuthService.generate_otp()
        
        # Create OTP record with user's email and the contact method used
        otp_email = user.email  # Always use user's email for OTP record
        otp_phone = contact_phone or user.phone  # Use provided phone or user's phone
        otp = OTPRepository.create_otp(db, otp_email, otp_code, phone=otp_phone)
        
        contact_info = contact_email or contact_phone
        logger.info(f"OTP generated for signin via {contact_info}")
        
        # TODO: Send OTP via email or SMS
        logger.debug(f"OTP for {contact_info}: {otp_code}")
        
        return {
            "message": "OTP sent successfully",
            "expires_in": settings.OTP_EXPIRE_MINUTES
        }

    @staticmethod
    def verify_otp(db: Session, request: VerifyOTPRequest) -> dict:
        """Verify OTP for both signup completion and signin.
        
        Determines if this is signup or signin based on user verification status.
        Supports both email and phone for OTP verification.
        Returns JWT token and marks user as verified if signup.
        """
        # Validate that at least email or phone is provided
        if not request.email and not request.phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either email or phone is required"
            )
        
        # Determine which contact was used
        contact_email = request.email
        contact_phone = request.phone
        
        # Get valid OTP by email or phone
        otp = None
        user = None
        
        if contact_email:
            otp = OTPRepository.get_valid_otp(db, contact_email)
            if otp:
                user = UserRepository.get_user_by_email(db, contact_email)
        elif contact_phone:
            # Get OTP by phone
            otp = db.query(OTP).filter(
                OTP.phone == contact_phone,
                OTP.is_verified == False,
                OTP.expires_at > datetime.utcnow()
            ).order_by(OTP.created_at.desc()).first()
            if otp:
                user = UserRepository.get_user_by_phone(db, contact_phone)
        
        if not otp:
            contact_info = contact_email or contact_phone
            logger.warning(f"No valid OTP found for: {contact_info}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP expired or not found"
            )
        
        # Check maximum attempts
        if otp.attempts >= 5:
            logger.warning(f"Too many failed attempts for OTP: {otp.id}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed attempts. Please request a new OTP"
            )
        
        # Verify OTP code
        if otp.otp_code != request.otp_code:
            OTPRepository.increment_attempts(db, otp.id)
            contact_info = contact_email or contact_phone
            logger.warning(f"Invalid OTP attempt for: {contact_info}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP code"
            )
        
        # Get user if not already retrieved
        if not user:
            if contact_email:
                user = UserRepository.get_user_by_email(db, contact_email)
            else:
                user = UserRepository.get_user_by_phone(db, contact_phone)
        
        if not user:
            contact_info = contact_email or contact_phone
            logger.warning(f"User not found for OTP verification: {contact_info}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Mark OTP as verified
        if contact_email:
            OTPRepository.verify_otp(db, otp.id, email=contact_email)
        else:
            OTPRepository.verify_otp(db, otp.id, phone=contact_phone)
        
        # Determine if this is signup or signin
        is_new_user = not user.is_verified
        
        if is_new_user:
            # Signup completion: mark user as verified
            UserRepository.verify_user(db, user.id)
            logger.info(f"User verified: {user.email}")
        else:
            # Signin: ensure user is verified
            if not user.is_verified:
                logger.warning(f"Signin attempt for unverified user: {user.email}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User account not verified"
                )
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email, "user_id": str(user.id)})
        
        logger.info(f"OTP verification successful for: {user.email}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "is_new_user": is_new_user,
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES
        }

    @staticmethod
    def get_current_user(db: Session, user_id: str) -> UserResponse:
        """Get current user details."""
        user = UserRepository.get_user_with_children(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.from_orm(user)

    @staticmethod
    def soft_delete_user(db: Session, user_id: str) -> dict:
        """Soft delete a user account."""
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        deleted_user = UserRepository.soft_delete_user(db, user_id)
        logger.info(f"User soft deleted: {user.email}")
        
        return {
            "message": "User account deleted successfully",
            "user_id": str(deleted_user.id),
            "deleted_at": deleted_user.deleted_at
        }

