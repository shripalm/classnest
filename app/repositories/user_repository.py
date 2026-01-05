from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import User
from app.models.child import Child
from app.schemas.auth_schema import UserCreate


class UserRepository:
    @staticmethod
    def create_user(db: Session, user: UserCreate, hashed_password: str) -> User:
        """Create a new user."""
        db_user = User(
            email=user.email,
            username=user.email.split("@")[0],
            full_name=user.name,
            name=user.name,
            phone=user.phone,
            country_code=user.country_code,
            address=user.address,
            hashed_password=hashed_password,
            terms_accepted=user.terms_accepted,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email (excluding soft-deleted users)."""
        return db.query(User).filter(User.email == email, User.is_deleted == False).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        """Get user by ID (excluding soft-deleted users)."""
        return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()

    @staticmethod
    def update_user_password(db: Session, user_id: str, hashed_password: str) -> User:
        """Update user password."""
        user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
        if user:
            user.hashed_password = hashed_password
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def get_user_with_children(db: Session, user_id: str) -> User:
        """Get user with children (excluding soft-deleted users)."""
        return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()

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
