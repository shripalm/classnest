from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db_sync
from app.schemas.tutor_schema import (
    TutorCreate, TutorUpdate, TutorResponse, TutorFiltersResponse,
    FilterOption, PriceRangeFilter, LocationFilter, SuperClassFilter,
    LanguageFilter, TimeFilter, DayFilter, TutorFiltersData, TutorFilterRequest
)
from app.schemas.response import SuccessResponse, PaginatedResponse
from app.repositories.tutor_repository import TutorRepository
from app.utils.pagination import PaginationParams
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tutors", tags=["tutors"])


@router.post("", response_model=SuccessResponse[TutorResponse], status_code=status.HTTP_201_CREATED)
def create_tutor(tutor_data: TutorCreate, db: Session = Depends(get_db_sync)):
    """Create a new tutor profile.
    
    - **name**: Tutor's full name
    - **price**: Hourly rate
    - **lesson_duration**: Duration in minutes
    - **languages**: List of languages spoken
    """
    try:
        db_tutor = TutorRepository.create_tutor(db, tutor_data)
        tutor_response = TutorResponse.from_orm(db_tutor)
        return SuccessResponse(
            status="success",
            message="Tutor created successfully",
            data=tutor_response
        )
    except Exception as e:
        logger.error(f"Error creating tutor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create tutor"
        )


@router.get("/{tutor_id}", response_model=SuccessResponse[TutorResponse])
def get_tutor(tutor_id: str, db: Session = Depends(get_db_sync)):
    """Get a specific tutor by ID."""
    try:
        db_tutor = TutorRepository.get_tutor_by_id(db, tutor_id)
        if not db_tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tutor not found"
            )
        
        tutor_response = TutorResponse.from_orm(db_tutor)
        return SuccessResponse(
            status="success",
            message="Tutor retrieved successfully",
            data=tutor_response
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tutor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tutor"
        )


@router.get("", response_model=PaginatedResponse[TutorResponse])
def get_all_tutors(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at", regex="^(name|rating|price|created_at|lessons|students)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db_sync)
):
    """Get all tutors with pagination.
    
    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20, max: 100)
    - **sort_by**: Field to sort by (name, rating, price, created_at, lessons, students)
    - **sort_order**: Sort order (asc or desc)
    """
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        tutors, total = TutorRepository.get_all_tutors(
            db,
            skip=pagination.skip,
            limit=pagination.limit,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        pagination_data = pagination.get_pagination_data(total)
        tutor_responses = [TutorResponse.from_orm(tutor) for tutor in tutors]
        
        return PaginatedResponse(
            status="success",
            message="Tutors retrieved successfully",
            data=tutor_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error retrieving tutors: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tutors"
        )


@router.put("/{tutor_id}", response_model=SuccessResponse[TutorResponse])
def update_tutor(
    tutor_id: str,
    tutor_data: TutorUpdate,
    db: Session = Depends(get_db_sync)
):
    """Update a tutor's information."""
    try:
        db_tutor = TutorRepository.update_tutor(db, tutor_id, tutor_data)
        if not db_tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tutor not found"
            )
        
        tutor_response = TutorResponse.from_orm(db_tutor)
        return SuccessResponse(
            status="success",
            message="Tutor updated successfully",
            data=tutor_response
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating tutor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update tutor"
        )


@router.delete("/{tutor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tutor(tutor_id: str, db: Session = Depends(get_db_sync)):
    """Delete (soft delete) a tutor."""
    try:
        success = TutorRepository.delete_tutor(db, tutor_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tutor not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting tutor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete tutor"
        )


@router.get("/search/query", response_model=PaginatedResponse[TutorResponse])
def search_tutors(
    q: str = Query(..., min_length=1, description="Search term"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Search tutors by name or headline."""
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        tutors, total = TutorRepository.search_tutors(
            db,
            search_term=q,
            skip=pagination.skip,
            limit=pagination.limit
        )
        
        pagination_data = pagination.get_pagination_data(total)
        tutor_responses = [TutorResponse.from_orm(tutor) for tutor in tutors]
        
        return PaginatedResponse(
            status="success",
            message="Search results retrieved successfully",
            data=tutor_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error searching tutors: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search tutors"
        )


@router.get("/verified/list", response_model=PaginatedResponse[TutorResponse])
def get_verified_tutors(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Get only verified tutors, sorted by rating."""
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        tutors, total = TutorRepository.get_verified_tutors(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
        
        pagination_data = pagination.get_pagination_data(total)
        tutor_responses = [TutorResponse.from_orm(tutor) for tutor in tutors]
        
        return PaginatedResponse(
            status="success",
            message="Verified tutors retrieved successfully",
            data=tutor_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error retrieving verified tutors: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve verified tutors"
        )


@router.get("/top-rated/list", response_model=SuccessResponse[list[TutorResponse]])
def get_top_rated_tutors(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db_sync)
):
    """Get top rated tutors."""
    try:
        tutors = TutorRepository.get_top_rated_tutors(db, limit=limit)
        tutor_responses = [TutorResponse.from_orm(tutor) for tutor in tutors]
        
        return SuccessResponse(
            status="success",
            message="Top rated tutors retrieved successfully",
            data=tutor_responses
        )
    except Exception as e:
        logger.error(f"Error retrieving top rated tutors: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve top rated tutors"
        )


@router.get("/filters/options", response_model=TutorFiltersResponse)
def get_tutor_filters():
    """Get available filter options for tutor search."""
    try:
        filters_data = TutorFiltersData(
            price_per_lesson=PriceRangeFilter(
                currency="SGD",
                min=3,
                max=52,
                slider_min=0,
                slider_max=60,
                params={"min": 3, "max": 52}
            ),
            location=LocationFilter(
                items=[
                    FilterOption(label="Singapore", key="singapore"),
                    FilterOption(label="Malaysia", key="malaysia"),
                    FilterOption(label="China", key="china"),
                    FilterOption(label="USA", key="usa")
                ],
                params={}
            ),
            super_class=SuperClassFilter(
                enabled=True,
                params={"superClass": True}
            ),
            also_speaks=LanguageFilter(
                items=[
                    FilterOption(label="English", key="en"),
                    FilterOption(label="Chinese", key="zh"),
                    FilterOption(label="Spanish", key="es"),
                    FilterOption(label="French", key="fr"),
                    FilterOption(label="German", key="de"),
                    FilterOption(label="Arabic", key="ar"),
                    FilterOption(label="Russian", key="ru"),
                    FilterOption(label="Korean", key="ko")
                ],
                params={}
            ),
            times_available=TimeFilter(
                items=[
                    FilterOption(label="7:00", key="07"),
                    FilterOption(label="8:00", key="08"),
                    FilterOption(label="9:00", key="09"),
                    FilterOption(label="10:00", key="10"),
                    FilterOption(label="11:00", key="11"),
                    FilterOption(label="12:00", key="12"),
                    FilterOption(label="13:00", key="13"),
                    FilterOption(label="14:00", key="14"),
                    FilterOption(label="15:00", key="15"),
                    FilterOption(label="16:00", key="16"),
                    FilterOption(label="17:00", key="17"),
                    FilterOption(label="18:00", key="18")
                ],
                params={}
            ),
            days_available=DayFilter(
                items=[
                    FilterOption(label="Mon", key="mon"),
                    FilterOption(label="Tue", key="tue"),
                    FilterOption(label="Wed", key="wed"),
                    FilterOption(label="Thu", key="thu"),
                    FilterOption(label="Fri", key="fri"),
                    FilterOption(label="Sat", key="sat"),
                    FilterOption(label="Sun", key="sun")
                ],
                params={}
            )
        )
        
        return TutorFiltersResponse(status=True, data=filters_data)
    except Exception as e:
        logger.error(f"Error retrieving tutor filters: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tutor filters"
        )


@router.post("/search", response_model=PaginatedResponse[TutorResponse])
def search_tutors(
    filters: TutorFilterRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Search and filter tutors based on criteria.
    
    Filter parameters:
    - **price_min**: Minimum price per lesson
    - **price_max**: Maximum price per lesson
    - **locations**: List of location keys (e.g., ["singapore", "malaysia"])
    - **languages**: List of language codes (e.g., ["en", "zh", "es"])
    - **super_tutor_only**: Filter only super tutors
    - **professional_only**: Filter only professional tutors
    - **verified_only**: Filter only verified tutors
    - **min_rating**: Minimum rating threshold
    - **sort_by**: Sort field (rating, price, reviews, students)
    """
    try:
        skip = (page - 1) * page_size
        
        tutors, total = TutorRepository.filter_tutors(
            db,
            skip=skip,
            limit=page_size,
            price_min=filters.price_min,
            price_max=filters.price_max,
            locations=filters.locations,
            languages=filters.languages,
            times=filters.times,
            days=filters.days,
            super_tutor_only=filters.super_tutor_only or False,
            professional_only=filters.professional_only or False,
            verified_only=filters.verified_only or False,
            min_rating=filters.min_rating,
            sort_by=filters.sort_by or "rating"
        )
        
        total_pages = (total + page_size - 1) // page_size
        tutor_responses = [TutorResponse.from_orm(tutor) for tutor in tutors]
        
        return PaginatedResponse(
            status="success",
            message="Tutors filtered successfully",
            data=tutor_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    except Exception as e:
        logger.error(f"Error filtering tutors: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to filter tutors"
        )
