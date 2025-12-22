from sqlalchemy.orm import Session
from app.models.class_model import Class


class ClassRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Class).all()

    @staticmethod
    def get_by_id(db: Session, class_id: int):
        return db.query(Class).filter(Class.id == class_id).first()

    @staticmethod
    def create(db: Session, name: str):
        class_obj = Class(name=name)
        db.add(class_obj)
        db.commit()
        db.refresh(class_obj)
        return class_obj
