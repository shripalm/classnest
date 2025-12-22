from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.db.session import get_db_sync
from app.repositories.class_repository import ClassRepository
from app.schemas.class_schema import ClassResponse

router = APIRouter(prefix="/classes", tags=["classes"])


class ClassListResponse(BaseModel):
    data: List[ClassResponse]


class ClassDetailResponse(BaseModel):
    data: ClassResponse


@router.get("", response_model=ClassListResponse)
def get_classes(db: Session = Depends(get_db_sync)):
    """Get all classes with their courses."""
    classes = ClassRepository.get_all(db)
    return {"data": classes}


@router.get("/{class_id}", response_model=ClassDetailResponse)
def get_class(class_id: int, db: Session = Depends(get_db_sync)):
    """Get a specific class by ID with its courses."""
    class_obj = ClassRepository.get_by_id(db, class_id)
    return {"data": class_obj}
