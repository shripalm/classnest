from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db_sync
from app.schemas.school_schema import SchoolCreate, SchoolUpdate, SchoolResponse
from app.schemas.response import SuccessResponse, PaginatedResponse
from app.repositories.school_repository import SchoolRepository
from app.utils.pagination import PaginationParams
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/schools", tags=["schools"])


@router.post("", response_model=SuccessResponse[SchoolResponse], status_code=status.HTTP_201_CREATED)
def create_school(school_data: SchoolCreate, db: Session = Depends(get_db_sync)):
    """Create a new school profile.
    
    - **name**: School's name
    - **price**: Price per lesson
    - **lesson_duration**: Duration in minutes
    """
    try:
        db_school = SchoolRepository.create_school(db, school_data)
        school_response = SchoolResponse.from_orm(db_school)
        return SuccessResponse(
            status="success",
            message="School created successfully",
            data=school_response
        )
    except Exception as e:
        logger.error(f"Error creating school: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create school"
        )


@router.get("/{school_id}", response_model=SuccessResponse[SchoolResponse])
def get_school(school_id: str, db: Session = Depends(get_db_sync)):
    """Get a specific school by ID."""
    try:
        db_school = SchoolRepository.get_school_by_id(db, school_id)
        if not db_school:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="School not found"
            )
        
        school_response = SchoolResponse.from_orm(db_school)
        return SuccessResponse(
            status="success",
            message="School retrieved successfully",
            data=school_response
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving school: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve school"
        )


@router.get("", response_model=PaginatedResponse[SchoolResponse])
def get_all_schools(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("rating"),
    db: Session = Depends(get_db_sync)
):
    """Get all schools with pagination and sorting.
    
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **sort_by**: Sort field (rating, price, name, created_at)
    """
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        schools, total = SchoolRepository.get_all_schools(
            db, pagination.skip, pagination.limit, sort_by=sort_by
        )
        pagination_data = pagination.get_pagination_data(total)
        school_responses = [SchoolResponse.from_orm(school) for school in schools]
        
        return PaginatedResponse(
            status="success",
            message="Schools retrieved successfully",
            data=school_responses,
            **pagination_data
        )
    except Exception as e:
        logger.error(f"Error retrieving schools: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve schools"
        )


@router.put("/{school_id}", response_model=SuccessResponse[SchoolResponse])
def update_school(
    school_id: str,
    school_data: SchoolUpdate,
    db: Session = Depends(get_db_sync)
):
    """Update a school profile."""
    try:
        db_school = SchoolRepository.update_school(db, school_id, school_data)
        if not db_school:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="School not found"
            )
        
        school_response = SchoolResponse.from_orm(db_school)
        return SuccessResponse(
            status="success",
            message="School updated successfully",
            data=school_response
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating school: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update school"
        )


@router.delete("/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school(school_id: str, db: Session = Depends(get_db_sync)):
    """Delete a school (soft delete)."""
    try:
        success = SchoolRepository.delete_school(db, school_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="School not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting school: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete school"
        )


@router.post("/search", response_model=PaginatedResponse[SchoolResponse])
def search_schools(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Search schools by name or description."""
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        schools, total = SchoolRepository.search_schools(
            db, q, pagination.skip, pagination.limit
        )
        pagination_data = pagination.get_pagination_data(total)
        school_responses = [SchoolResponse.from_orm(school) for school in schools]
        
        return PaginatedResponse(
            status="success",
            message="Schools searched successfully",
            data=school_responses,
            **pagination_data
        )
    except Exception as e:
        logger.error(f"Error searching schools: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search schools"
        )


@router.get("/verified", response_model=PaginatedResponse[SchoolResponse])
def get_verified_schools(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Get only verified schools."""
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        schools, total = SchoolRepository.get_verified_schools(
            db, pagination.skip, pagination.limit
        )
        pagination_data = pagination.get_pagination_data(total)
        school_responses = [SchoolResponse.from_orm(school) for school in schools]
        
        return PaginatedResponse(
            status="success",
            message="Verified schools retrieved successfully",
            data=school_responses,
            **pagination_data
        )
    except Exception as e:
        logger.error(f"Error retrieving verified schools: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve verified schools"
        )


@router.get("/top-rated", response_model=SuccessResponse[list[SchoolResponse]])
def get_top_rated_schools(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Get top rated schools."""
    try:
        schools = SchoolRepository.get_top_rated_schools(db, limit=limit)
        school_responses = [SchoolResponse.from_orm(school) for school in schools]
        
        return SuccessResponse(
            status="success",
            message="Top rated schools retrieved successfully",
            data=school_responses
        )
    except Exception as e:
        logger.error(f"Error retrieving top rated schools: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve top rated schools"
        )


@router.post("/filter", response_model=PaginatedResponse[SchoolResponse])
def filter_schools(
    filters: dict = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Filter schools based on multiple criteria.
    
    Filter parameters (optional):
    - **price_min**: Minimum price per lesson
    - **price_max**: Maximum price per lesson
    - **locations**: List of location keys
    - **languages**: List of language codes
    - **professional_only**: Filter only professional schools
    - **verified_only**: Filter only verified schools
    - **min_rating**: Minimum rating threshold
    - **sort_by**: Sort field (rating, price, reviews, students)
    """
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        
        schools, total = SchoolRepository.filter_schools(
            db,
            skip=pagination.skip,
            limit=pagination.limit,
            price_min=filters.get("price_min") if filters else None,
            price_max=filters.get("price_max") if filters else None,
            locations=filters.get("locations") if filters else None,
            languages=filters.get("languages") if filters else None,
            times=filters.get("times") if filters else None,
            days=filters.get("days") if filters else None,
            professional_only=filters.get("professional_only", False) if filters else False,
            verified_only=filters.get("verified_only", False) if filters else False,
            min_rating=filters.get("min_rating") if filters else None,
            sort_by=filters.get("sort_by", "rating") if filters else "rating"
        )
        
        pagination_data = pagination.get_pagination_data(total)
        school_responses = [SchoolResponse.from_orm(school) for school in schools]
        
        return PaginatedResponse(
            status="success",
            message="Schools filtered successfully",
            data=school_responses,
            **pagination_data
        )
    except Exception as e:
        logger.error(f"Error filtering schools: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to filter schools"
        )
