from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from uuid import UUID
from app.models.favorite_tutor import FavoriteTutor
from app.models.tutor import Tutor


class FavoriteTutorRepository:
    """Repository for favorite tutor database operations."""

    @staticmethod
    def add_favorite(db: Session, user_id: str, tutor_id: str) -> FavoriteTutor:
        """Add a tutor to user's favorites."""
        try:
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
            tutor_uuid = UUID(tutor_id) if isinstance(tutor_id, str) else tutor_id
        except (ValueError, TypeError):
            return None
        
        # Check if already favorited
        existing = db.query(FavoriteTutor).filter(
            and_(
                FavoriteTutor.user_id == user_uuid,
                FavoriteTutor.tutor_id == tutor_uuid,
                FavoriteTutor.is_deleted == False
            )
        ).first()
        
        if existing:
            return existing
        
        db_favorite = FavoriteTutor(user_id=user_uuid, tutor_id=tutor_uuid)
        db.add(db_favorite)
        db.commit()
        db.refresh(db_favorite)
        return db_favorite

    @staticmethod
    def remove_favorite(db: Session, user_id: str, tutor_id: str) -> bool:
        """Remove a tutor from user's favorites (soft delete)."""
        try:
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
            tutor_uuid = UUID(tutor_id) if isinstance(tutor_id, str) else tutor_id
        except (ValueError, TypeError):
            return False
        
        db_favorite = db.query(FavoriteTutor).filter(
            and_(
                FavoriteTutor.user_id == user_uuid,
                FavoriteTutor.tutor_id == tutor_uuid,
                FavoriteTutor.is_deleted == False
            )
        ).first()
        
        if not db_favorite:
            return False
        
        db_favorite.is_deleted = True
        db_favorite.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def get_user_favorite_tutors(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> tuple[list[Tutor], int]:
        """Get all tutors favorited by a user."""
        try:
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        except (ValueError, TypeError):
            return [], 0
        
        query = db.query(Tutor).join(
            FavoriteTutor,
            and_(
                FavoriteTutor.tutor_id == Tutor.id,
                FavoriteTutor.user_id == user_uuid,
                FavoriteTutor.is_deleted == False
            )
        ).filter(Tutor.is_deleted == False)
        
        total = query.count()
        tutors = query.offset(skip).limit(limit).all()
        
        return tutors, total

    @staticmethod
    def get_user_favorite_tutor_ids(db: Session, user_id: str) -> list[str]:
        """Get list of tutor IDs favorited by a user."""
        try:
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        except (ValueError, TypeError):
            return []
        
        favorites = db.query(FavoriteTutor.tutor_id).filter(
            and_(
                FavoriteTutor.user_id == user_uuid,
                FavoriteTutor.is_deleted == False
            )
        ).all()
        
        return [str(fav[0]) for fav in favorites]

    @staticmethod
    def set_favorite_tutors(db: Session, user_id: str, tutor_ids: list[str]) -> list[FavoriteTutor]:
        """Set user's favorite tutors (replace existing list)."""
        try:
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        except (ValueError, TypeError):
            return []
        
        # Soft delete all existing favorites for this user
        existing_favorites = db.query(FavoriteTutor).filter(
            and_(
                FavoriteTutor.user_id == user_uuid,
                FavoriteTutor.is_deleted == False
            )
        ).all()
        
        for fav in existing_favorites:
            fav.is_deleted = True
            fav.deleted_at = datetime.utcnow()
        
        # Add new favorites
        new_favorites = []
        for tutor_id in tutor_ids:
            try:
                tutor_uuid = UUID(tutor_id) if isinstance(tutor_id, str) else tutor_id
                db_favorite = FavoriteTutor(user_id=user_uuid, tutor_id=tutor_uuid)
                db.add(db_favorite)
                new_favorites.append(db_favorite)
            except (ValueError, TypeError):
                continue
        
        db.commit()
        for fav in new_favorites:
            db.refresh(fav)
        
        return new_favorites

    @staticmethod
    def is_favorite(db: Session, user_id: str, tutor_id: str) -> bool:
        """Check if tutor is favorited by user."""
        try:
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
            tutor_uuid = UUID(tutor_id) if isinstance(tutor_id, str) else tutor_id
        except (ValueError, TypeError):
            return False
        
        favorite = db.query(FavoriteTutor).filter(
            and_(
                FavoriteTutor.user_id == user_uuid,
                FavoriteTutor.tutor_id == tutor_uuid,
                FavoriteTutor.is_deleted == False
            )
        ).first()
        
        return favorite is not None

    @staticmethod
    def get_favorite_count(db: Session, user_id: str) -> int:
        """Get count of favorite tutors for a user."""
        try:
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        except (ValueError, TypeError):
            return 0
        
        return db.query(FavoriteTutor).filter(
            and_(
                FavoriteTutor.user_id == user_uuid,
                FavoriteTutor.is_deleted == False
            )
        ).count()

    @staticmethod
    def get_tutor_favorite_count(db: Session, tutor_id: str) -> int:
        """Get count of users who favorited a tutor."""
        try:
            tutor_uuid = UUID(tutor_id) if isinstance(tutor_id, str) else tutor_id
        except (ValueError, TypeError):
            return 0
        
        return db.query(FavoriteTutor).filter(
            and_(
                FavoriteTutor.tutor_id == tutor_uuid,
                FavoriteTutor.is_deleted == False
            )
        ).count()
