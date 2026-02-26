from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Course(Base):
    """Course model for storing course information."""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    
    # Relationship to subjects
    subjects = relationship("Subject", back_populates="course", cascade="all, delete-orphan")
