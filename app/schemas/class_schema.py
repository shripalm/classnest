from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ClassCreate(BaseModel):
    """Schema for creating a new class."""
    class_name: str
    course_id: int
    course_name: str
    subject_id: int
    subject_name: str
    tutor_id: Optional[UUID] = None
    institute_id: Optional[UUID] = None
    tutor_institute_name: str
    location: str
    description: str
    runtime_per_session_min: int
    total_sessions: Optional[int] = None
    cost: float
    duration: str
    min_age: int
    max_age: int
    default_reviews_count: int = 0
    default_rating: float = 0.0


class ClassUpdate(BaseModel):
    """Schema for updating a class."""
    class_name: Optional[str] = None
    course_id: Optional[int] = None
    course_name: Optional[str] = None
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    tutor_id: Optional[UUID] = None
    institute_id: Optional[UUID] = None
    tutor_institute_name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    runtime_per_session_min: Optional[int] = None
    total_sessions: Optional[int] = None
    cost: Optional[float] = None
    duration: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    default_reviews_count: Optional[int] = None
    default_rating: Optional[float] = None


class ClassResponse(BaseModel):
    """Schema for class response."""
    id: int
    class_name: str
    course_id: int
    course_name: str
    subject_id: int
    subject_name: str
    tutor_id: Optional[UUID] = None
    institute_id: Optional[UUID] = None
    tutor_institute_name: str
    location: str
    description: str
    runtime_per_session_min: int
    total_sessions: Optional[int] = None
    cost: float
    duration: str
    min_age: int
    max_age: int
    default_reviews_count: int
    default_rating: float
    is_deleted: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
