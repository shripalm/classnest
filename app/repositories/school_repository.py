from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_, cast, Text
from datetime import datetime
from uuid import UUID
from app.models.school import School
from app.schemas.school_schema import SchoolCreate, SchoolUpdate


class SchoolRepository:
    """Repository for school database operations."""

    @staticmethod
    def create_school(db: Session, school_data: SchoolCreate) -> School:
        """Create a new school."""
        db_school = School(**school_data.model_dump())
        db.add(db_school)
        db.commit()
        db.refresh(db_school)
        return db_school

    @staticmethod
    def get_school_by_id(db: Session, school_id: str) -> School:
        """Get a school by ID (excluding soft-deleted)."""
        try:
            school_uuid = UUID(school_id) if isinstance(school_id, str) else school_id
        except (ValueError, TypeError):
            return None
        
        return db.query(School).filter(
            School.id == school_uuid,
            School.is_deleted == False
        ).first()

    @staticmethod
    def get_all_schools(db: Session, skip: int = 0, limit: int = 20, sort_by: str = "created_at", sort_order: str = "desc") -> tuple[list[School], int]:
        """Get all schools with pagination and sorting."""
        query = db.query(School).filter(School.is_deleted == False)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        if sort_by == "rating":
            query = query.order_by(desc(School.rating)) if sort_order == "desc" else query.order_by(School.rating)
        elif sort_by == "price":
            query = query.order_by(School.price) if sort_order == "asc" else query.order_by(desc(School.price))
        elif sort_by == "name":
            query = query.order_by(School.name)
        else:
            query = query.order_by(desc(School.created_at))
        
        schools = query.offset(skip).limit(limit).all()
        
        return schools, total

    @staticmethod
    def update_school(db: Session, school_id: str, school_data: SchoolUpdate) -> School:
        """Update a school."""
        try:
            school_uuid = UUID(school_id) if isinstance(school_id, str) else school_id
        except (ValueError, TypeError):
            return None
        
        db_school = db.query(School).filter(
            School.id == school_uuid,
            School.is_deleted == False
        ).first()
        
        if not db_school:
            return None
        
        # Update only provided fields
        update_data = school_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_school, key, value)
        
        db_school.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_school)
        return db_school

    @staticmethod
    def delete_school(db: Session, school_id: str) -> bool:
        """Soft delete a school."""
        try:
            school_uuid = UUID(school_id) if isinstance(school_id, str) else school_id
        except (ValueError, TypeError):
            return False
        
        db_school = db.query(School).filter(
            School.id == school_uuid,
            School.is_deleted == False
        ).first()
        
        if not db_school:
            return False
        
        db_school.is_deleted = True
        db_school.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def search_schools(db: Session, query_text: str, skip: int = 0, limit: int = 20) -> tuple[list[School], int]:
        """Search schools by name or about_us."""
        query = db.query(School).filter(
            School.is_deleted == False,
            or_(
                School.name.ilike(f"%{query_text}%"),
                School.about_us.ilike(f"%{query_text}%")
            )
        ).order_by(desc(School.rating))
        
        total = query.count()
        schools = query.offset(skip).limit(limit).all()
        
        return schools, total

    @staticmethod
    def get_verified_schools(db: Session, skip: int = 0, limit: int = 20) -> tuple[list[School], int]:
        """Get only verified schools."""
        query = db.query(School).filter(
            School.is_deleted == False,
            School.verified == True
        ).order_by(desc(School.rating))
        
        total = query.count()
        schools = query.offset(skip).limit(limit).all()
        
        return schools, total

    @staticmethod
    def get_top_rated_schools(db: Session, limit: int = 10) -> list[School]:
        """Get top rated schools."""
        return db.query(School).filter(
            School.is_deleted == False
        ).order_by(desc(School.rating)).limit(limit).all()

    @staticmethod
    def filter_schools(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        price_min: float = None,
        price_max: float = None,
        locations: list = None,
        languages: list = None,
        times: list = None,
        days: list = None,
        professional_only: bool = False,
        verified_only: bool = False,
        min_rating: float = None,
        sort_by: str = "rating"
    ) -> tuple[list[School], int]:
        """Filter schools based on multiple criteria."""
        query = db.query(School).filter(School.is_deleted == False)
        
        # Apply filters
        if price_min is not None:
            query = query.filter(School.price >= price_min)
        
        if price_max is not None:
            query = query.filter(School.price <= price_max)
        
        if locations:
            location_filters = [School.country_of_birth.ilike(f"%{loc}%") for loc in locations]
            query = query.filter(or_(*location_filters))
        
        if languages:
            for lang in languages:
                query = query.filter(cast(School.languages, Text).contains(f'"{lang}"'))
        
        if times:
            for time in times:
                query = query.filter(cast(School.times_available, Text).contains(f'"{time}"'))
        
        if days:
            for day in days:
                query = query.filter(cast(School.days_available, Text).contains(f'"{day}"'))
        
        if professional_only:
            query = query.filter(School.is_professional_tutor == True)
        
        if verified_only:
            query = query.filter(School.verified == True)
        
        if min_rating is not None:
            query = query.filter(School.rating >= min_rating)
        
        # Apply sorting
        sort_map = {
            "rating": desc(School.rating),
            "price": School.price,
            "reviews": desc(School.reviews),
            "students": desc(School.students),
            "name": School.name
        }
        sort_field = sort_map.get(sort_by, desc(School.rating))
        query = query.order_by(sort_field)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        schools = query.offset(skip).limit(limit).all()
        
        return schools, total
