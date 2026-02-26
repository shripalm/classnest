from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float, Index, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base


class Class(Base):
    """Class model for storing class information."""
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    class_name = Column(String(256), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    course_name = Column(String(256), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    subject_name = Column(String(256), nullable=False)
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutors.id"), nullable=True, index=True)
    institute_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=True, index=True)
    tutor_institute_name = Column(String(256), nullable=False)
    location = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    runtime_per_session_min = Column(Integer, nullable=False)
    total_sessions = Column(Integer, nullable=True)
    cost = Column(Float, nullable=False)
    duration = Column(String(64), nullable=False)
    min_age = Column(Integer, nullable=False)
    max_age = Column(Integer, nullable=False)
    default_reviews_count = Column(Integer, default=0, nullable=False)
    default_rating = Column(Float, default=0.0, nullable=False)
    is_deleted = Column(Integer, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_classes_course_id', 'course_id'),
        Index('idx_classes_subject_id', 'subject_id'),
        Index('idx_classes_tutor_id', 'tutor_id'),
        Index('idx_classes_institute_id', 'institute_id'),
        Index('idx_classes_location', 'location'),
    )

    def __repr__(self):
        return f"<Class(id={self.id}, class_name={self.class_name}, cost={self.cost})>"
