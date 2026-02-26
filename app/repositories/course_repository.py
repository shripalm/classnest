from sqlalchemy.orm import Session
from app.models.course_model import Subject


class SubjectRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Subject).all()

    @staticmethod
    def get_by_id(db: Session, subject_id: int):
        return db.query(Subject).filter(Subject.id == subject_id).first()

    @staticmethod
    def create(db: Session, subject_name: str, course_id: int):
        subject = Subject(subject_name=subject_name, course_id=course_id)
        db.add(subject)
        db.commit()
        db.refresh(subject)
        return subject
