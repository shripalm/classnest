from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db_sync
from app.schemas.favorite_tutor_schema import (
    FavoriteTutorCreate, FavoriteTutorsListCreate, FavoriteTutorResponse, FavoriteTutorsResponse
)
from app.schemas.response import SuccessResponse, PaginatedResponse
from app.schemas.tutor_schema import TutorResponse
from app.repositories.favorite_tutor_repository import FavoriteTutorRepository
from app.repositories.tutor_repository import TutorRepository
from app.utils.pagination import PaginationParams
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post("/tutors", response_model=SuccessResponse[FavoriteTutorResponse], status_code=status.HTTP_201_CREATED)
def add_favorite_tutor(
    request: FavoriteTutorCreate,
    db: Session = Depends(get_db_sync)
):
    """Add a tutor to user's favorites.
    
    - **user_id**: UUID of the user
    - **tutor_id**: UUID of the tutor to favorite
    """
    try:
        # Verify tutor exists
        tutor = TutorRepository.get_tutor_by_id(db, request.tutor_id)
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tutor not found"
            )
        
        db_favorite = FavoriteTutorRepository.add_favorite(db, request.user_id, request.tutor_id)
        if not db_favorite:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user or tutor ID"
            )
        
        favorite_response = FavoriteTutorResponse.from_orm(db_favorite)
        return SuccessResponse(
            status="success",
            message="Tutor added to favorites",
            data=favorite_response
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding favorite tutor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add favorite tutor"
        )


@router.delete("/tutors/{user_id}/{tutor_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite_tutor(
    user_id: str,
    tutor_id: str,
    db: Session = Depends(get_db_sync)
):
    """Remove a tutor from user's favorites.
    
    - **user_id**: UUID of the user
    - **tutor_id**: UUID of the tutor to remove from favorites
    """
    try:
        success = FavoriteTutorRepository.remove_favorite(db, user_id, tutor_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing favorite tutor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove favorite tutor"
        )


@router.get("/tutors/{user_id}", response_model=PaginatedResponse[TutorResponse])
def get_user_favorite_tutors(
    user_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_sync)
):
    """Get all tutors favorited by a user with pagination.
    
    - **user_id**: UUID of the user
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    """
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        tutors, total = FavoriteTutorRepository.get_user_favorite_tutors(
            db,
            user_id=user_id,
            skip=pagination.skip,
            limit=pagination.limit
        )
        
        pagination_data = pagination.get_pagination_data(total)
        tutor_responses = [TutorResponse.from_orm(tutor) for tutor in tutors]
        
        return PaginatedResponse(
            status="success",
            message="Favorite tutors retrieved successfully",
            data=tutor_responses,
            total=pagination_data["total"],
            page=pagination_data["page"],
            page_size=pagination_data["page_size"],
            total_pages=pagination_data["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error retrieving favorite tutors: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve favorite tutors"
        )


@router.get("/{user_id}/list", response_model=SuccessResponse[FavoriteTutorsResponse])
def get_favorite_tutors_list(
    user_id: str,
    db: Session = Depends(get_db_sync)
):
    """Get list of favorite tutor IDs for a user.
    
    Returns a simple list of tutor IDs that the user has favorited.
    
    - **user_id**: UUID of the user
    """
    try:
        favorite_ids = FavoriteTutorRepository.get_user_favorite_tutor_ids(db, user_id)
        
        return SuccessResponse(
            status="success",
            message="Favorite tutors list retrieved successfully",
            data=FavoriteTutorsResponse(
                user_id=user_id,
                favourite_tutors=favorite_ids
            )
        )
    except Exception as e:
        logger.error(f"Error retrieving favorite tutors list: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve favorite tutors list"
        )


@router.post("/{user_id}/set", response_model=SuccessResponse[list[FavoriteTutorResponse]], status_code=status.HTTP_200_OK)
def set_favorite_tutors(
    user_id: str,
    request: FavoriteTutorsListCreate,
    db: Session = Depends(get_db_sync)
):
    """Set user's favorite tutors (replaces existing list).
    
    This endpoint replaces all existing favorites with the provided list.
    
    Request body:
    ```json
    {
      "favouriteTutors": ["tutor_id_1", "tutor_id_2", "tutor_id_3"]
    }
    ```
    """
    try:
        # Verify user_id matches
        if request.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID mismatch"
            )
        
        # Verify all tutors exist
        for tutor_id in request.favorite_tutor_ids:
            tutor = TutorRepository.get_tutor_by_id(db, tutor_id)
            if not tutor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tutor {tutor_id} not found"
                )
        
        db_favorites = FavoriteTutorRepository.set_favorite_tutors(
            db,
            user_id=user_id,
            tutor_ids=request.favorite_tutor_ids
        )
        
        if not db_favorites:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID or tutor IDs"
            )
        
        favorite_responses = [FavoriteTutorResponse.from_orm(fav) for fav in db_favorites]
        
        return SuccessResponse(
            status="success",
            message=f"{len(db_favorites)} tutors added to favorites",
            data=favorite_responses
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting favorite tutors: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set favorite tutors"
        )


@router.get("/{user_id}/count", response_model=SuccessResponse[dict])
def get_favorite_count(
    user_id: str,
    db: Session = Depends(get_db_sync)
):
    """Get count of favorite tutors for a user.
    
    - **user_id**: UUID of the user
    """
    try:
        count = FavoriteTutorRepository.get_favorite_count(db, user_id)
        
        return SuccessResponse(
            status="success",
            message="Favorite count retrieved successfully",
            data={"user_id": user_id, "favorite_count": count}
        )
    except Exception as e:
        logger.error(f"Error getting favorite count: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get favorite count"
        )


@router.get("/tutor/{tutor_id}/favorite-count", response_model=SuccessResponse[dict])
def get_tutor_favorite_count(
    tutor_id: str,
    db: Session = Depends(get_db_sync)
):
    """Get count of users who favorited a specific tutor.
    
    - **tutor_id**: UUID of the tutor
    """
    try:
        # Verify tutor exists
        tutor = TutorRepository.get_tutor_by_id(db, tutor_id)
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tutor not found"
            )
        
        count = FavoriteTutorRepository.get_tutor_favorite_count(db, tutor_id)
        
        return SuccessResponse(
            status="success",
            message="Tutor favorite count retrieved successfully",
            data={"tutor_id": tutor_id, "favorite_count": count}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tutor favorite count: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get tutor favorite count"
        )


@router.get("/{user_id}/{tutor_id}", response_model=SuccessResponse[dict])
def check_is_favorite(
    user_id: str,
    tutor_id: str,
    db: Session = Depends(get_db_sync)
):
    """Check if a tutor is favorited by a user.
    
    - **user_id**: UUID of the user
    - **tutor_id**: UUID of the tutor
    """
    try:
        is_fav = FavoriteTutorRepository.is_favorite(db, user_id, tutor_id)
        
        return SuccessResponse(
            status="success",
            message="Favorite status retrieved successfully",
            data={"user_id": user_id, "tutor_id": tutor_id, "is_favorite": is_fav}
        )
    except Exception as e:
        logger.error(f"Error checking favorite status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check favorite status"
        )
