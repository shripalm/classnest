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
    """Schema for school resume."""
    file_name: Optional[str] = Field(None, alias="fileName")
    resume_url: Optional[str] = Field(None, alias="resumeUrl")
    is_downloadable: Optional[bool] = Field(None, alias="isDownloadable")

    model_config = ConfigDict(populate_by_name=True)


class SchoolCreate(BaseModel):
    """Schema for creating a new school."""
    name: str
    profile_images: List[str] = Field(default_factory=list)
    intro_video_thumbnail: Optional[str] = None
    country_flag: Optional[str] = None
    flag: Optional[str] = None
    country_of_birth: Optional[str] = None
    about_us: Optional[str] = None
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
    professional: Optional[str] = None
    super_tutor: Optional[str] = None
    languages: List[str] = Field(default_factory=list)
    coursepick: List[str] = Field(default_factory=list)
    resume: Optional[Resume] = None
    student_comments: List[StudentComment] = Field(default_factory=list)
    times_available: List[str] = Field(default_factory=list)
    days_available: List[str] = Field(default_factory=list)


class SchoolUpdate(BaseModel):
    """Schema for updating a school."""
    name: Optional[str] = None
    profile_images: Optional[List[str]] = None
    intro_video_thumbnail: Optional[str] = None
    country_flag: Optional[str] = None
    flag: Optional[str] = None
    country_of_birth: Optional[str] = None
    about_us: Optional[str] = None
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
    professional: Optional[str] = None
    super_tutor: Optional[str] = None
    languages: Optional[List[str]] = None
    coursepick: Optional[List[str]] = None
    resume: Optional[Resume] = None
    student_comments: Optional[List[StudentComment]] = None
    times_available: Optional[List[str]] = None
    days_available: Optional[List[str]] = None


class SchoolResponse(BaseModel):
    """Schema for school response."""
    id: str
    name: str
    profile_images: List[str] = Field(default_factory=list, alias="profileImages")
    intro_video_thumbnail: Optional[str] = Field(None, alias="introVideoThumbnail")
    country_flag: Optional[str] = Field(None, alias="countryFlag")
    flag: Optional[str] = None
    country_of_birth: Optional[str] = Field(None, alias="countryOfBirth")
    about_us: Optional[str] = Field(None, alias="aboutus")
    verified: bool
    is_professional_tutor: bool = Field(alias="isProfessionalTutor")
    is_super_tutor: bool = Field(alias="isSuperTutor")
    badge: Optional[str] = None
    price: float = Field(alias="pricePerLesson")
    currency: str
    lesson_duration: int = Field(alias="lessonDuration")
    rating: float
    student_rating: float = Field(alias="studentRating")
    is_favourite: bool = Field(alias="isFavourite")
    reviews: int
    headline: Optional[str] = None
    teaches: Optional[str] = None
    popularity: Optional[str] = None
    popularity_info: Optional[str] = Field(None, alias="popularityInfo")
    students: int
    lessons: int
    professional: Optional[str] = None
    super_tutor: Optional[str] = Field(None, alias="superTutor")
    languages: List[str]
    coursepick: List[str]
    resume: Optional[Resume] = None
    student_comments: List[StudentComment] = Field(default_factory=list, alias="studentComments")
    times_available: List[str] = Field(default_factory=list, alias="timesAvailable")
    days_available: List[str] = Field(default_factory=list, alias="daysAvailable")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @classmethod
    def from_orm(cls, obj):
        """Convert UUID to string and handle nested objects."""
        # Handle resume
        resume_obj = None
        if obj.resume:
            resume_obj = Resume(**obj.resume) if isinstance(obj.resume, dict) else obj.resume

        # Handle student comments
        student_comments = []
        if obj.student_comments:
            student_comments = [StudentComment(**comment) if isinstance(comment, dict) else comment 
                              for comment in obj.student_comments]

        data = {
            "id": str(obj.id),
            "name": obj.name,
            "profile_images": obj.profile_images or [],
            "intro_video_thumbnail": obj.intro_video_thumbnail,
            "country_flag": obj.country_flag,
            "flag": obj.flag,
            "country_of_birth": obj.country_of_birth,
            "about_us": obj.about_us,
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
            "professional": obj.professional,
            "super_tutor": obj.super_tutor,
            "languages": obj.languages or [],
            "coursepick": obj.coursepick or [],
            "resume": resume_obj,
            "student_comments": student_comments,
            "times_available": obj.times_available or [],
            "days_available": obj.days_available or [],
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }
        return cls(**data)
