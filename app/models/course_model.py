from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Course(Base):
    """Course model for storing course information."""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    
    # Relationship to class
    class_ = relationship("Class", back_populates="courses")
