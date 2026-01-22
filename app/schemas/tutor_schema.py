from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class StudentComment(BaseModel):
    """Schema for student comments."""
    name: str
    date: str = Field(alias="Date")
    rating: int = Field(alias="Rating")
    comment: str = Field(alias="Comment")
    image: str = Field(alias="Image")

    model_config = ConfigDict(populate_by_name=True)


class Resume(BaseModel):
    """Schema for tutor resume."""
    file_name: Optional[str] = Field(None, alias="fileName")
    resume_url: Optional[str] = Field(None, alias="resumeUrl")
    is_downloadable: Optional[bool] = Field(None, alias="isDownloadable")

    model_config = ConfigDict(populate_by_name=True)


class TutorCreate(BaseModel):
    """Schema for creating a new tutor."""
    name: str
    profile_image: Optional[str] = None
    intro_video_thumbnail: Optional[str] = None
    country_flag: Optional[str] = None
    country_of_birth: Optional[str] = None
    verified: bool = False
    is_professional_tutor: bool = False
    is_super_tutor: bool = False
    badge: Optional[str] = None
    price: float
    currency: str = "SGD"
    lesson_duration: int  # in minutes
    rating: float = 0.0
    student_rating: float = 0.0
    is_favourite: bool = False
    reviews: int = 0
    headline: Optional[str] = None
    teaches: Optional[str] = None
    popularity: Optional[str] = None
    popularity_info: Optional[str] = None
    students: int = 0
    lessons: int = 0
    about_me: Optional[str] = None
    professional: Optional[str] = None
    super_tutor: Optional[str] = None
    languages: List[str] = Field(default_factory=list)
    resume: Optional[Resume] = None
    student_comments: List[StudentComment] = Field(default_factory=list)
    times_available: List[str] = Field(default_factory=list)  # e.g., ["07", "08", "09"]
    days_available: List[str] = Field(default_factory=list)  # e.g., ["mon", "tue", "wed"]


class TutorUpdate(BaseModel):
    """Schema for updating a tutor."""
    name: Optional[str] = None
    profile_image: Optional[str] = None
    intro_video_thumbnail: Optional[str] = None
    country_flag: Optional[str] = None
    country_of_birth: Optional[str] = None
    verified: Optional[bool] = None
    is_professional_tutor: Optional[bool] = None
    is_super_tutor: Optional[bool] = None
    badge: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    lesson_duration: Optional[int] = None
    rating: Optional[float] = None
    student_rating: Optional[float] = None
    is_favourite: Optional[bool] = None
    reviews: Optional[int] = None
    headline: Optional[str] = None
    teaches: Optional[str] = None
    popularity: Optional[str] = None
    popularity_info: Optional[str] = None
    students: Optional[int] = None
    lessons: Optional[int] = None
    about_me: Optional[str] = None
    professional: Optional[str] = None
    super_tutor: Optional[str] = None
    languages: Optional[List[str]] = None
    resume: Optional[Resume] = None
    student_comments: Optional[List[StudentComment]] = None
    times_available: Optional[List[str]] = None
    days_available: Optional[List[str]] = None


class TutorResponse(BaseModel):
    """Schema for tutor response."""
    id: str
    name: str
    profile_image: Optional[str] = None
    intro_video_thumbnail: Optional[str] = None
    country_flag: Optional[str] = None
    country_of_birth: Optional[str] = None
    verified: bool
    is_professional_tutor: bool
    is_super_tutor: bool
    badge: Optional[str] = None
    price: float
    currency: str
    lesson_duration: int
    rating: float
    student_rating: float
    is_favourite: bool
    reviews: int
    headline: Optional[str] = None
    teaches: Optional[str] = None
    popularity: Optional[str] = None
    popularity_info: Optional[str] = None
    students: int
    lessons: int
    about_me: Optional[str] = None
    professional: Optional[str] = None
    super_tutor: Optional[str] = None
    languages: List[str]
    resume: Optional[Resume] = None
    student_comments: List[StudentComment] = Field(default_factory=list)
    times_available: List[str] = Field(default_factory=list)
    days_available: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        """Convert UUID to string and handle nested objects."""
        # Handle resume
        resume_obj = None
        if obj.resume:
            if isinstance(obj.resume, dict):
                resume_obj = Resume(**obj.resume)
            else:
                resume_obj = obj.resume
        
        # Handle student comments
        student_comments = []
        if obj.student_comments:
            if isinstance(obj.student_comments, list):
                for comment in obj.student_comments:
                    if isinstance(comment, dict):
                        student_comments.append(StudentComment(**comment))
                    else:
                        student_comments.append(comment)
        
        data = {
            "id": str(obj.id) if isinstance(obj.id, UUID) else obj.id,
            "name": obj.name,
            "profile_image": obj.profile_image,
            "intro_video_thumbnail": obj.intro_video_thumbnail,
            "country_flag": obj.country_flag,
            "country_of_birth": obj.country_of_birth,
            "verified": obj.verified,
            "is_professional_tutor": obj.is_professional_tutor,
            "is_super_tutor": obj.is_super_tutor,
            "badge": obj.badge,
            "price": obj.price,
            "currency": obj.currency,
            "lesson_duration": obj.lesson_duration,
            "rating": obj.rating,
            "student_rating": obj.student_rating,
            "is_favourite": obj.is_favourite,
            "reviews": obj.reviews,
            "headline": obj.headline,
            "teaches": obj.teaches,
            "popularity": obj.popularity,
            "popularity_info": obj.popularity_info,
            "students": obj.students,
            "lessons": obj.lessons,
            "about_me": obj.about_me,
            "professional": obj.professional,
            "super_tutor": obj.super_tutor,
            "languages": obj.languages or [],
            "resume": resume_obj,
            "student_comments": student_comments,
            "times_available": obj.times_available or [],
            "days_available": obj.days_available or [],
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }
        return cls(**data)


# Filter Schemas
class FilterOption(BaseModel):
    """Schema for a single filter option."""
    label: str
    key: str


class PriceRangeFilter(BaseModel):
    """Schema for price range filter."""
    currency: str = "SGD"
    min: float
    max: float
    slider_min: float = Field(alias="sliderMin")
    slider_max: float = Field(alias="sliderMax")
    params: dict = Field(default_factory=lambda: {"min": 3, "max": 52})

    model_config = ConfigDict(populate_by_name=True)


class LocationFilter(BaseModel):
    """Schema for location filter."""
    items: List[FilterOption]
    params: dict = Field(default_factory=dict)


class SuperClassFilter(BaseModel):
    """Schema for super class filter."""
    enabled: bool = True
    params: dict = Field(default_factory=lambda: {"superClass": True})


class LanguageFilter(BaseModel):
    """Schema for language filter."""
    items: List[FilterOption]
    params: dict = Field(default_factory=dict)


class TimeFilter(BaseModel):
    """Schema for time availability filter."""
    items: List[FilterOption]
    params: dict = Field(default_factory=dict)


class DayFilter(BaseModel):
    """Schema for day availability filter."""
    items: List[FilterOption]
    params: dict = Field(default_factory=dict)


class TutorFiltersData(BaseModel):
    """Schema for tutor filter data."""
    price_per_lesson: PriceRangeFilter = Field(alias="pricePerLesson")
    location: LocationFilter
    super_class: SuperClassFilter = Field(alias="superClass")
    also_speaks: LanguageFilter = Field(alias="alsoSpeaks")
    times_available: TimeFilter = Field(alias="timesAvailable")
    days_available: DayFilter = Field(alias="daysAvailable")

    model_config = ConfigDict(populate_by_name=True)


class TutorFiltersResponse(BaseModel):
    """Schema for tutor filters API response."""
    status: bool
    data: TutorFiltersData


class TutorFilterRequest(BaseModel):
    """Schema for tutor filter request parameters."""
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    locations: Optional[List[str]] = None  # e.g., ["singapore", "malaysia"]
    languages: Optional[List[str]] = None  # e.g., ["en", "zh", "es"]
    times: Optional[List[str]] = None  # e.g., ["07", "08", "09"]
    days: Optional[List[str]] = None  # e.g., ["mon", "tue", "wed"]
    super_tutor_only: Optional[bool] = False
    professional_only: Optional[bool] = False
    verified_only: Optional[bool] = False
    min_rating: Optional[float] = None
    sort_by: Optional[str] = "rating"  # rating, price, reviews, students
