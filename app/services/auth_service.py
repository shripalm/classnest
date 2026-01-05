from sqlalchemy.orm import Session
from app.schemas.auth_schema import UserCreate, UserLogin, UserResponse, AuthResponse, ChildCreate
from app.repositories.user_repository import UserRepository
from app.repositories.child_repository import ChildRepository
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def sign_up(db: Session, user_data: UserCreate) -> UserResponse:
        """Register a new user with children."""
        # Check if user already exists
        existing_user = UserRepository.get_user_by_email(db, user_data.email)
        if existing_user:
            logger.warning(f"Signup attempt with existing email: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Create user
        db_user = UserRepository.create_user(db, user_data, hashed_password)
        logger.info(f"New user created: {db_user.email}")

        # Create children
        for child_data in user_data.children:
            child = ChildRepository.create_child(db, db_user.id, child_data)
            logger.info(f"Child created for user {db_user.email}: {child.name}")

        # Refresh to get children relationship
        db.refresh(db_user)
        return UserResponse.from_orm(db_user)

    @staticmethod
    def sign_in(db: Session, credentials: UserLogin) -> AuthResponse:
        """Sign in user with email and password."""
        user = UserRepository.get_user_by_email(db, credentials.email)
        
        if not user or not verify_password(credentials.password, user.hashed_password):
            logger.warning(f"Failed signin attempt for email: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            logger.warning(f"Signin attempt for inactive user: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        # Create access token
        access_token = create_access_token(data={"sub": user.email, "user_id": str(user.id)})
        
        logger.info(f"User signed in successfully: {user.email}")

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.from_orm(user)
        )

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

