from sqlalchemy.orm import Session
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
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update_user_password(db: Session, user_id: str, hashed_password: str) -> User:
        """Update user password."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.hashed_password = hashed_password
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def get_user_with_children(db: Session, user_id: str) -> User:
        """Get user with children."""
        return db.query(User).filter(User.id == user_id).first()
