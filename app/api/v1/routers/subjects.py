from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.db.session import get_db_sync
from app.repositories.course_repository import SubjectRepository
from app.schemas.course_schema import SubjectResponse

router = APIRouter(prefix="/subjects")


class SubjectListResponse(BaseModel):
    data: List[SubjectResponse]


class SubjectDetailResponse(BaseModel):
    data: SubjectResponse


@router.get("", response_model=SubjectListResponse)
def get_subjects(db: Session = Depends(get_db_sync)):
    """Get all subjects."""
    subjects = SubjectRepository.get_all(db)
    return {"data": subjects}


@router.get("/{subject_id}", response_model=SubjectDetailResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db_sync)):
    """Get a specific subject by ID."""
    subject = SubjectRepository.get_by_id(db, subject_id)
    return {"data": subject}
