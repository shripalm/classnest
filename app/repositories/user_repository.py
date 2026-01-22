from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import User
from app.models.child import Child
from app.schemas.auth_schema import UserCreate


class UserRepository:
    @staticmethod
    def create_user_otp(db: Session, email: str, user: UserCreate) -> User:
        """Create a new user via OTP (no password). User is not verified until OTP verification."""
        db_user = User(
            email=email,
            full_name=user.full_name,
            country_code=user.country_code,
            phone=user.phone,
            address=user.address,
            terms_accepted=user.terms_accepted,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Create children if provided
        if user.children:
            from app.repositories.child_repository import ChildRepository
            for child_data in user.children:
                ChildRepository.create_child(db, str(db_user.id), child_data)
        
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email (excluding soft-deleted users)."""
        return db.query(User).filter(User.email == email, User.is_deleted == False).first()

    @staticmethod
    def email_exists(db: Session, email: str) -> bool:
        """Check if email exists for non-deleted users."""
        user = db.query(User).filter(User.email == email, User.is_deleted == False).first()
        return user is not None

    @staticmethod
    def phone_exists(db: Session, phone: str) -> bool:
        """Check if phone exists for non-deleted users."""
        if not phone:
            return False
        user = db.query(User).filter(User.phone == phone, User.is_deleted == False).first()
        return user is not None

    @staticmethod
    def get_user_by_phone(db: Session, phone: str) -> User:
        """Get user by phone (excluding soft-deleted users)."""
        return db.query(User).filter(User.phone == phone, User.is_deleted == False).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        """Get user by ID (excluding soft-deleted users)."""
        return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()

    @staticmethod
    def get_user_with_children(db: Session, user_id: str) -> User:
        """Get user with children (excluding soft-deleted users)."""
        return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()

    @staticmethod
    def verify_email(db: Session, user_id: str) -> User:
        """Mark user email as verified."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_email_verified = True
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def verify_user(db: Session, user_id: str) -> User:
        """Mark user as verified (after OTP verification during signup)."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_verified = True
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def verify_phone(db: Session, user_id: str) -> User:
        """Mark user phone as verified."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_phone_verified = True
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def soft_delete_user(db: Session, user_id: str) -> User:
        """Soft delete a user by marking as deleted."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_deleted = True
            user.deleted_at = datetime.utcnow()
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def restore_user(db: Session, user_id: str) -> User:
        """Restore a soft-deleted user."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_deleted = False
            user.deleted_at = None
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 20, include_deleted: bool = False) -> tuple[list[User], int]:
        """Get all users with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: Whether to include soft-deleted users
        
        Returns:
            Tuple of (list of users, total count)
        """
        query = db.query(User)
        
        if not include_deleted:
            query = query.filter(User.is_deleted == False)
        
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        
        return users, total
