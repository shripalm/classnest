from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.db.session import get_db_sync
from app.repositories.course_repository import CourseRepository
from app.schemas.course_schema import CourseResponse

router = APIRouter(prefix="/courses")


class CourseListResponse(BaseModel):
    data: List[CourseResponse]


class CourseDetailResponse(BaseModel):
    data: CourseResponse


@router.get("", response_model=CourseListResponse)
def get_courses(db: Session = Depends(get_db_sync)):
    """Get all courses with their subjects."""
    courses = CourseRepository.get_all(db)
    return {"data": courses}


@router.get("/{course_id}", response_model=CourseDetailResponse)
def get_course(course_id: int, db: Session = Depends(get_db_sync)):
    """Get a specific course by ID with its subjects."""
    course = CourseRepository.get_by_id(db, course_id)
    return {"data": course}
