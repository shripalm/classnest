from sqlalchemy.orm import Session
from app.models.class_model import Course


class CourseRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Course).all()

    @staticmethod
    def get_by_id(db: Session, course_id: int):
        return db.query(Course).filter(Course.id == course_id).first()

    @staticmethod
    def create(db: Session, name: str):
        course = Course(name=name)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
