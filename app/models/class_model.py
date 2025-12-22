from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Class(Base):
    """Class model for storing class information."""
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    
    # Relationship to courses
    courses = relationship("Course", back_populates="class_", cascade="all, delete-orphan")
