from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime
from uuid import UUID
from app.models.classes import Class
from app.schemas.class_schema import ClassCreate, ClassUpdate


class ClassRepository:
    """Repository for class database operations."""

    @staticmethod
    def create_class(db: Session, class_data: ClassCreate) -> Class:
        """Create a new class."""
        db_class = Class(**class_data.model_dump())
        db.add(db_class)
        db.commit()
        db.refresh(db_class)
        return db_class

    @staticmethod
    def get_class_by_id(db: Session, class_id: str) -> Class:
        """Get a class by ID (excluding soft-deleted)."""
        try:
            class_uuid = UUID(class_id) if isinstance(class_id, str) else class_id
        except (ValueError, TypeError):
            return None
        
        return db.query(Class).filter(
            Class.id == class_uuid,
            Class.is_deleted == 0
        ).first()

    @staticmethod
    def get_all_classes(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        subject_id: int = None,
        course_id: int = None,
        tutor_id: str = None,
        institute_id: str = None,
        min_age: int = None,
        max_age: int = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> tuple[list[Class], int]:
        """
        Get all classes with optional filtering and pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            subject_id: Filter by subject ID
            course_id: Filter by course ID
            tutor_id: Filter by tutor ID
            institute_id: Filter by institute ID
            min_age: Filter by minimum age requirement (classes where min_age <= this value)
            max_age: Filter by maximum age requirement (classes where max_age >= this value)
            sort_by: Field to sort by
            sort_order: Sort order ('asc' or 'desc')
        
        Returns:
            Tuple of (list of classes, total count)
        """
        query = db.query(Class).filter(Class.is_deleted == 0)
        
        # Apply filters
        if subject_id is not None:
            query = query.filter(Class.subject_id == subject_id)
        
        if course_id is not None:
            query = query.filter(Class.course_id == course_id)
        
        if tutor_id is not None:
            try:
                tutor_uuid = UUID(tutor_id) if isinstance(tutor_id, str) else tutor_id
                query = query.filter(Class.tutor_id == tutor_uuid)
            except (ValueError, TypeError):
                pass
        
        if institute_id is not None:
            try:
                institute_uuid = UUID(institute_id) if isinstance(institute_id, str) else institute_id
                query = query.filter(Class.institute_id == institute_uuid)
            except (ValueError, TypeError):
                pass
        
        if min_age is not None:
            query = query.filter(Class.min_age <= min_age)
        
        if max_age is not None:
            query = query.filter(Class.max_age >= max_age)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        if hasattr(Class, sort_by):
            sort_column = getattr(Class, sort_by)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
        else:
            query = query.order_by(desc(Class.created_at))
        
        # Apply pagination
        classes = query.offset(skip).limit(limit).all()
        
        return classes, total

    @staticmethod
    def update_class(db: Session, class_id: str, class_data: ClassUpdate) -> Class:
        """Update a class by ID."""
        try:
            class_uuid = UUID(class_id) if isinstance(class_id, str) else class_id
        except (ValueError, TypeError):
            return None
        
        db_class = db.query(Class).filter(
            Class.id == class_uuid,
            Class.is_deleted == 0
        ).first()
        
        if not db_class:
            return None
        
        # Update only provided fields
        update_data = class_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(db_class, key, value)
        
        db_class.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_class)
        return db_class

    @staticmethod
    def delete_class(db: Session, class_id: str) -> bool:
        """Soft delete a class."""
        try:
            class_uuid = UUID(class_id) if isinstance(class_id, str) else class_id
        except (ValueError, TypeError):
            return False
        
        db_class = db.query(Class).filter(
            Class.id == class_uuid,
            Class.is_deleted == 0
        ).first()
        
        if not db_class:
            return False
        
        db_class.is_deleted = 1
        db_class.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def get_classes_by_course(db: Session, course_id: int, skip: int = 0, limit: int = 20) -> tuple[list[Class], int]:
        """Get all classes for a specific course."""
        query = db.query(Class).filter(
            Class.course_id == course_id,
            Class.is_deleted == 0
        ).order_by(desc(Class.created_at))
        
        total = query.count()
        classes = query.offset(skip).limit(limit).all()
        
        return classes, total

    @staticmethod
    def get_classes_by_subject(db: Session, subject_id: int, skip: int = 0, limit: int = 20) -> tuple[list[Class], int]:
        """Get all classes for a specific subject."""
        query = db.query(Class).filter(
            Class.subject_id == subject_id,
            Class.is_deleted == 0
        ).order_by(desc(Class.created_at))
        
        total = query.count()
        classes = query.offset(skip).limit(limit).all()
        
        return classes, total

    @staticmethod
    def get_classes_by_tutor(db: Session, tutor_id: str, skip: int = 0, limit: int = 20) -> tuple[list[Class], int]:
        """Get all classes for a specific tutor."""
        try:
            tutor_uuid = UUID(tutor_id) if isinstance(tutor_id, str) else tutor_id
        except (ValueError, TypeError):
            return [], 0
        
        query = db.query(Class).filter(
            Class.tutor_id == tutor_uuid,
            Class.is_deleted == 0
        ).order_by(desc(Class.created_at))
        
        total = query.count()
        classes = query.offset(skip).limit(limit).all()
        
        return classes, total

    @staticmethod
    def get_classes_by_institute(db: Session, institute_id: str, skip: int = 0, limit: int = 20) -> tuple[list[Class], int]:
        """Get all classes for a specific institute."""
        try:
            institute_uuid = UUID(institute_id) if isinstance(institute_id, str) else institute_id
        except (ValueError, TypeError):
            return [], 0
        
        query = db.query(Class).filter(
            Class.institute_id == institute_uuid,
            Class.is_deleted == 0
        ).order_by(desc(Class.created_at))
        
        total = query.count()
        classes = query.offset(skip).limit(limit).all()
        
        return classes, total

    @staticmethod
    def get_classes_by_age_range(db: Session, age: int, skip: int = 0, limit: int = 20) -> tuple[list[Class], int]:
        """Get all classes suitable for a specific age."""
        query = db.query(Class).filter(
            Class.min_age <= age,
            Class.max_age >= age,
            Class.is_deleted == 0
        ).order_by(desc(Class.rating))
        
        total = query.count()
        classes = query.offset(skip).limit(limit).all()
        
        return classes, total
