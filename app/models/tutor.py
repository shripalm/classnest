from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float, Index, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.db.base_class import Base


class Tutor(Base):
    """Tutor model for storing tutor profile information."""
    __tablename__ = "tutors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    profile_image = Column(String(500), nullable=True)
    intro_video_thumbnail = Column(String(500), nullable=True)
    country_flag = Column(String(500), nullable=True)
    country_of_birth = Column(String(255), nullable=True)
    verified = Column(Boolean, default=False, nullable=False)
    is_professional_tutor = Column(Boolean, default=False, nullable=False)
    is_super_tutor = Column(Boolean, default=False, nullable=False)
    badge = Column(String(100), nullable=True)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="SGD", nullable=False)
    lesson_duration = Column(Integer, nullable=False)  # in minutes
    rating = Column(Float, default=0.0, nullable=False)
    student_rating = Column(Float, default=0.0, nullable=False)
    is_favourite = Column(Boolean, default=False, nullable=False)
    reviews = Column(Integer, default=0, nullable=False)
    headline = Column(Text, nullable=True)
    teaches = Column(String(255), nullable=True)
    popularity = Column(String(100), nullable=True)
    popularity_info = Column(Text, nullable=True)
    students = Column(Integer, default=0, nullable=False)
    lessons = Column(Integer, default=0, nullable=False)
    about_me = Column(Text, nullable=True)
    professional = Column(Text, nullable=True)
    super_tutor = Column(Text, nullable=True)
    languages = Column(JSON, default=[], nullable=False)  # Stores array of language strings
    resume = Column(JSON, nullable=True)  # Stores resume file info
    student_comments = Column(JSON, default=[], nullable=False)  # Stores array of comments
    times_available = Column(JSON, default=[], nullable=False)  # Stores array of available times (e.g., ["07", "08", "09"])
    days_available = Column(JSON, default=[], nullable=False)  # Stores array of available days (e.g., ["mon", "tue", "wed"])
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_tutors_name', 'name'),
        Index('idx_tutors_verified', 'verified'),
        Index('idx_tutors_rating', 'rating'),
    )

    def __repr__(self):
        return f"<Tutor(id={self.id}, name={self.name}, rating={self.rating})>"
