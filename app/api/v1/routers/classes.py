from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db_sync
from app.schemas.class_schema import ClassCreate, ClassUpdate, ClassResponse
from app.schemas.response import SuccessResponse, PaginatedResponse
from app.repositories.class_repository import ClassRepository
from app.utils.pagination import PaginationParams
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/classes")


@router.post("", response_model=SuccessResponse[ClassResponse], status_code=status.HTTP_201_CREATED)
def create_class(class_data: ClassCreate, db: Session = Depends(get_db_sync)):
    """Create a new class.
    
    - **class_name**: Name of the class
    - **course_id**: Course ID (Integer)
    - **subject_id**: Subject ID (Integer)
    - **tutor_id**: Tutor ID (UUID, optional)
    - **institute_id**: Institute ID (UUID, optional)
    - **cost**: Cost of the class
    - **min_age**: Minimum age for students
    - **max_age**: Maximum age for students
    """
    try:
        db_class = ClassRepository.create_class(db, class_data)
        class_response = ClassResponse.from_orm(db_class)
        return SuccessResponse(
            status="success",
            message="Class created successfully",
            data=class_response
        )
    except Exception as e:
        logger.error(f"Error creating class: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create class"
        )


@router.get("/{class_id}", response_model=SuccessResponse[ClassResponse])
def get_class(class_id: str, db: Session = Depends(get_db_sync)):
    """Get a specific class by ID."""
    try:
        db_class = ClassRepository.get_class_by_id(db, class_id)
        if not db_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        
        class_response = ClassResponse.from_orm(db_class)
        return SuccessResponse(
            status="success",
            message="Class retrieved successfully",
            data=class_response
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting class: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve class"
        )


@router.get("", response_model=PaginatedResponse[ClassResponse])
def get_all_classes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    subject_id: Optional[int] = Query(None, description="Filter by subject ID"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    tutor_id: Optional[str] = Query(None, description="Filter by tutor ID (UUID)"),
    institute_id: Optional[str] = Query(None, description="Filter by institute ID (UUID)"),
    min_age: Optional[int] = Query(None, ge=0, description="Filter classes suitable for this minimum age"),
    max_age: Optional[int] = Query(None, ge=0, description="Filter classes suitable for this maximum age"),
    sort_by: str = Query("created_at", regex="^(class_name|cost|rating|created_at|min_age|max_age)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db_sync)
):
    """Get all classes with optional filtering and pagination.
    
    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20, max: 100)
    - **subject_id**: Filter by subject ID
    - **course_id**: Filter by course ID
    - **tutor_id**: Filter by tutor ID (UUID)
    - **institute_id**: Filter by institute ID (UUID)
    - **min_age**: Filter classes where min_age <= this value
    - **max_age**: Filter classes where max_age >= this value
    - **sort_by**: Field to sort by (class_name, cost, rating, created_at, min_age, max_age)
    - **sort_order**: Sort order (asc or desc)
    """
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        classes, total = ClassRepository.get_all_classes(
            db,
            skip=pagination.skip,
            limit=pagination.limit,
            subject_id=subject_id,
            course_id=course_id,
            tutor_id=tutor_id,
            institute_id=institute_id,
            min_age=min_age,
            max_age=max_age,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        pagination_data = pagination.get_pagination_data(total)
        class_responses = [ClassResponse.from_orm(cls) for cls in classes]
        
        return PaginatedResponse(
            status="success",
            message="Classes retrieved successfully",
            data=class_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error retrieving classes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve classes"
        )


@router.put("/{class_id}", response_model=SuccessResponse[ClassResponse])
def update_class(
    class_id: str,
    class_data: ClassUpdate,
    db: Session = Depends(get_db_sync)
):
    """Update a class's information."""
    try:
        db_class = ClassRepository.update_class(db, class_id, class_data)
        if not db_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        
        class_response = ClassResponse.from_orm(db_class)
        return SuccessResponse(
            status="success",
            message="Class updated successfully",
            data=class_response
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating class: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update class"
        )


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(class_id: str, db: Session = Depends(get_db_sync)):
    """Delete (soft delete) a class."""
    try:
        success = ClassRepository.delete_class(db, class_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting class: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete class"
        )


@router.get("/course/{course_id}", response_model=PaginatedResponse[ClassResponse])
def get_classes_by_course(
    course_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Get all classes for a specific course."""
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        classes, total = ClassRepository.get_classes_by_course(
            db,
            course_id=course_id,
            skip=pagination.skip,
            limit=pagination.limit
        )
        
        pagination_data = pagination.get_pagination_data(total)
        class_responses = [ClassResponse.from_orm(cls) for cls in classes]
        
        return PaginatedResponse(
            status="success",
            message="Classes retrieved successfully",
            data=class_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error retrieving classes by course: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve classes"
        )


@router.get("/subject/{subject_id}", response_model=PaginatedResponse[ClassResponse])
def get_classes_by_subject(
    subject_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Get all classes for a specific subject."""
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        classes, total = ClassRepository.get_classes_by_subject(
            db,
            subject_id=subject_id,
            skip=pagination.skip,
            limit=pagination.limit
        )
        
        pagination_data = pagination.get_pagination_data(total)
        class_responses = [ClassResponse.from_orm(cls) for cls in classes]
        
        return PaginatedResponse(
            status="success",
            message="Classes retrieved successfully",
            data=class_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error retrieving classes by subject: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve classes"
        )


@router.get("/tutor/{tutor_id}", response_model=PaginatedResponse[ClassResponse])
def get_classes_by_tutor(
    tutor_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Get all classes taught by a specific tutor."""
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        classes, total = ClassRepository.get_classes_by_tutor(
            db,
            tutor_id=tutor_id,
            skip=pagination.skip,
            limit=pagination.limit
        )
        
        pagination_data = pagination.get_pagination_data(total)
        class_responses = [ClassResponse.from_orm(cls) for cls in classes]
        
        return PaginatedResponse(
            status="success",
            message="Classes retrieved successfully",
            data=class_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error retrieving classes by tutor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve classes"
        )


@router.get("/institute/{institute_id}", response_model=PaginatedResponse[ClassResponse])
def get_classes_by_institute(
    institute_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Get all classes offered by a specific institute."""
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        classes, total = ClassRepository.get_classes_by_institute(
            db,
            institute_id=institute_id,
            skip=pagination.skip,
            limit=pagination.limit
        )
        
        pagination_data = pagination.get_pagination_data(total)
        class_responses = [ClassResponse.from_orm(cls) for cls in classes]
        
        return PaginatedResponse(
            status="success",
            message="Classes retrieved successfully",
            data=class_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error retrieving classes by institute: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve classes"
        )


@router.get("/age/{age}", response_model=PaginatedResponse[ClassResponse])
def get_classes_by_age(
    age: int = Query(..., ge=0, description="Student age"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Get all classes suitable for a specific age."""
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        classes, total = ClassRepository.get_classes_by_age_range(
            db,
            age=age,
            skip=pagination.skip,
            limit=pagination.limit
        )
        
        pagination_data = pagination.get_pagination_data(total)
        class_responses = [ClassResponse.from_orm(cls) for cls in classes]
        
        return PaginatedResponse(
            status="success",
            message="Classes retrieved successfully",
            data=class_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error retrieving classes by age: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve classes"
        )
