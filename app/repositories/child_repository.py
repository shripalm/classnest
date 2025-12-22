from sqlalchemy.orm import Session
from app.models.child import Child
from app.schemas.auth_schema import ChildCreate
from datetime import datetime


class ChildRepository:
    @staticmethod
    def create_child(db: Session, parent_id: str, child: ChildCreate) -> Child:
        """Create a new child."""
        date_of_birth = datetime.strptime(child.date_of_birth, "%d/%m/%Y").date()
        
        db_child = Child(
            parent_id=parent_id,
            name=child.name,
            date_of_birth=date_of_birth,
            gender=child.gender,
            photo=child.photo,
            interest=child.interest,
        )
        db.add(db_child)
        db.commit()
        db.refresh(db_child)
        return db_child

    @staticmethod
    def get_children_by_parent(db: Session, parent_id: str) -> list:
        """Get all children of a parent."""
        return db.query(Child).filter(Child.parent_id == parent_id).all()

    @staticmethod
    def get_child_by_id(db: Session, child_id: str) -> Child:
        """Get a child by ID."""
        return db.query(Child).filter(Child.id == child_id).first()

    @staticmethod
    def update_child(db: Session, child_id: str, **kwargs) -> Child:
        """Update a child."""
        child = db.query(Child).filter(Child.id == child_id).first()
        if child:
            for key, value in kwargs.items():
                setattr(child, key, value)
            db.commit()
            db.refresh(child)
        return child

    @staticmethod
    def delete_child(db: Session, child_id: str) -> bool:
        """Delete a child."""
        child = db.query(Child).filter(Child.id == child_id).first()
        if child:
            db.delete(child)
            db.commit()
            return True
        return False
