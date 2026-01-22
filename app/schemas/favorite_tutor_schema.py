from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class FavoriteTutorCreate(BaseModel):
    """Schema for adding a tutor to favorites."""
    user_id: str
    tutor_id: str


class FavoriteTutorsListCreate(BaseModel):
    """Schema for setting a list of favorite tutors."""
    user_id: str
    favorite_tutor_ids: List[str] = Field(..., alias="favouriteTutors")

    model_config = ConfigDict(populate_by_name=True)


class FavoriteTutorResponse(BaseModel):
    """Schema for favorite tutor response."""
    id: str
    user_id: str
    tutor_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        """Convert UUID to string."""
        data = {
            "id": str(obj.id) if isinstance(obj.id, UUID) else obj.id,
            "user_id": str(obj.user_id) if isinstance(obj.user_id, UUID) else obj.user_id,
            "tutor_id": str(obj.tutor_id) if isinstance(obj.tutor_id, UUID) else obj.tutor_id,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }
        return cls(**data)


class FavoriteTutorsResponse(BaseModel):
    """Schema for list of favorite tutor IDs."""
    user_id: str
    favourite_tutors: List[str]

    model_config = ConfigDict(populate_by_name=True)


class TutorWithFavoriteStatus(BaseModel):
    """Schema for tutor with favorite status indicator."""
    id: str
    name: str
    price: float
    currency: str
    rating: float
    is_favourite: bool
    profile_image: Optional[str] = None
    country_flag: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
