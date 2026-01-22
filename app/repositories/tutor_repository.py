from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_, cast, Text
from datetime import datetime
from uuid import UUID
from app.models.tutor import Tutor
from app.schemas.tutor_schema import TutorCreate, TutorUpdate


class TutorRepository:
    """Repository for tutor database operations."""

    @staticmethod
    def create_tutor(db: Session, tutor_data: TutorCreate) -> Tutor:
        """Create a new tutor."""
        db_tutor = Tutor(**tutor_data.model_dump())
        db.add(db_tutor)
        db.commit()
        db.refresh(db_tutor)
        return db_tutor

    @staticmethod
    def get_tutor_by_id(db: Session, tutor_id: str) -> Tutor:
        """Get a tutor by ID (excluding soft-deleted)."""
        try:
            tutor_uuid = UUID(tutor_id) if isinstance(tutor_id, str) else tutor_id
        except (ValueError, TypeError):
            return None
        
        return db.query(Tutor).filter(
            Tutor.id == tutor_uuid,
            Tutor.is_deleted == False
        ).first()

    @staticmethod
    def get_all_tutors(db: Session, skip: int = 0, limit: int = 20, sort_by: str = "created_at", sort_order: str = "desc") -> tuple[list[Tutor], int]:
        """Get all tutors with pagination and sorting.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            sort_by: Field to sort by (name, rating, price, created_at)
            sort_order: Sort order ('asc' or 'desc')
        
        Returns:
            Tuple of (list of tutors, total count)
        """
        query = db.query(Tutor).filter(Tutor.is_deleted == False)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        if hasattr(Tutor, sort_by):
            sort_column = getattr(Tutor, sort_by)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
        else:
            query = query.order_by(desc(Tutor.created_at))
        
        # Apply pagination
        tutors = query.offset(skip).limit(limit).all()
        
        return tutors, total

    @staticmethod
    def update_tutor(db: Session, tutor_id: str, tutor_data: TutorUpdate) -> Tutor:
        """Update a tutor by ID."""
        try:
            tutor_uuid = UUID(tutor_id) if isinstance(tutor_id, str) else tutor_id
        except (ValueError, TypeError):
            return None
        
        db_tutor = db.query(Tutor).filter(
            Tutor.id == tutor_uuid,
            Tutor.is_deleted == False
        ).first()
        
        if not db_tutor:
            return None
        
        # Update only provided fields
        update_data = tutor_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(db_tutor, key, value)
        
        db_tutor.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_tutor)
        return db_tutor

    @staticmethod
    def delete_tutor(db: Session, tutor_id: str) -> bool:
        """Soft delete a tutor."""
        try:
            tutor_uuid = UUID(tutor_id) if isinstance(tutor_id, str) else tutor_id
        except (ValueError, TypeError):
            return False
        
        db_tutor = db.query(Tutor).filter(
            Tutor.id == tutor_uuid,
            Tutor.is_deleted == False
        ).first()
        
        if not db_tutor:
            return False
        
        db_tutor.is_deleted = True
        db_tutor.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def search_tutors(db: Session, search_term: str, skip: int = 0, limit: int = 20) -> tuple[list[Tutor], int]:
        """Search tutors by name or headline."""
        query = db.query(Tutor).filter(
            Tutor.is_deleted == False
        ).filter(
            (Tutor.name.ilike(f"%{search_term}%")) |
            (Tutor.headline.ilike(f"%{search_term}%"))
        )
        
        total = query.count()
        tutors = query.offset(skip).limit(limit).all()
        
        return tutors, total

    @staticmethod
    def get_verified_tutors(db: Session, skip: int = 0, limit: int = 20) -> tuple[list[Tutor], int]:
        """Get only verified tutors."""
        query = db.query(Tutor).filter(
            Tutor.is_deleted == False,
            Tutor.verified == True
        ).order_by(desc(Tutor.rating))
        
        total = query.count()
        tutors = query.offset(skip).limit(limit).all()
        
        return tutors, total

    @staticmethod
    def get_top_rated_tutors(db: Session, limit: int = 10) -> list[Tutor]:
        """Get top rated tutors."""
        return db.query(Tutor).filter(
            Tutor.is_deleted == False
        ).order_by(desc(Tutor.rating)).limit(limit).all()

    @staticmethod
    def filter_tutors(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        price_min: float = None,
        price_max: float = None,
        locations: list = None,
        languages: list = None,
        times: list = None,
        days: list = None,
        super_tutor_only: bool = False,
        professional_only: bool = False,
        verified_only: bool = False,
        min_rating: float = None,
        sort_by: str = "rating"
    ) -> tuple[list[Tutor], int]:
        """Filter tutors based on multiple criteria.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            price_min: Minimum price per lesson
            price_max: Maximum price per lesson
            locations: List of location keys (e.g., ["singapore", "malaysia"])
            languages: List of language codes (e.g., ["en", "zh"])
            times: List of available times (e.g., ["07", "08"])
            days: List of available days (e.g., ["mon", "tue"])
            super_tutor_only: Filter only super tutors
            professional_only: Filter only professional tutors
            verified_only: Filter only verified tutors
            min_rating: Minimum rating threshold
            sort_by: Sort field (rating, price, reviews, students)
        
        Returns:
            Tuple of (filtered tutors list, total count)
        """
        query = db.query(Tutor).filter(Tutor.is_deleted == False)
        
        # Apply filters
        if price_min is not None:
            query = query.filter(Tutor.price >= price_min)
        
        if price_max is not None:
            query = query.filter(Tutor.price <= price_max)
        
        if locations:
            # Filter by country_of_birth or location field
            location_filters = [Tutor.country_of_birth.ilike(f"%{loc}%") for loc in locations]
            query = query.filter(or_(*location_filters))
        
        if languages:
            # Languages are stored as JSON array, check if any language is in the list
            # Cast JSON to text for string matching
            for lang in languages:
                query = query.filter(cast(Tutor.languages, Text).contains(f'"{lang}"'))
        
        if times:
            # Times are stored as JSON array, check if any requested time is available
            for time in times:
                query = query.filter(cast(Tutor.times_available, Text).contains(f'"{time}"'))
        
        if days:
            # Days are stored as JSON array, check if any requested day is available
            for day in days:
                query = query.filter(cast(Tutor.days_available, Text).contains(f'"{day}"'))
        
        if super_tutor_only:
            query = query.filter(Tutor.is_super_tutor == True)
        
        if professional_only:
            query = query.filter(Tutor.is_professional_tutor == True)
        
        if verified_only:
            query = query.filter(Tutor.verified == True)
        
        if min_rating is not None:
            query = query.filter(Tutor.rating >= min_rating)
        
        # Apply sorting
        sort_map = {
            "rating": desc(Tutor.rating),
            "price": Tutor.price,
            "reviews": desc(Tutor.reviews),
            "students": desc(Tutor.students),
            "name": Tutor.name
        }
        sort_field = sort_map.get(sort_by, desc(Tutor.rating))
        query = query.order_by(sort_field)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        tutors = query.offset(skip).limit(limit).all()
        
        return tutors, total
