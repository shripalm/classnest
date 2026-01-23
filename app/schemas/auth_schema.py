from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID


class ChildCreate(BaseModel):
    name: str
    date_of_birth: str
    gender: str
    photo: Optional[str] = None
    interest: Optional[str] = None


class ChildResponse(BaseModel):
    id: str
    name: str
    date_of_birth: date
    gender: Optional[str]
    photo: Optional[str]
    interest: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    country_code: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    children: List[ChildCreate] = []
    terms_accepted: bool

    @field_validator("terms_accepted")
    @classmethod
    def terms_must_be_accepted(cls, v):
        if not v:
            raise ValueError("Terms must be accepted")
        return v


class SendOTPRequest(BaseModel):
    """Request to send OTP."""
    email: EmailStr = Field(..., description="Email address to send OTP")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }


class SendOTPResponse(BaseModel):
    """Response after sending OTP."""
    message: str
    expires_in: int = Field(..., description="OTP expiration time in minutes")


class VerifyOTPRequest(BaseModel):
    """Request to verify OTP - email or phone required."""
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    otp_code: str = Field(
        ...,
        description="OTP code",
        min_length=4,
        max_length=10
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "phone": None,
                "otp_code": "1010"
            }
        }


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    phone: Optional[str]
    country_code: Optional[str]
    address: Optional[str]
    is_verified: bool
    is_email_verified: Optional[bool] = None
    is_phone_verified: Optional[bool] = None
    children: List[ChildResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str
    full_name: str
    expires_in: int


class RegisterRequest(BaseModel):
    """User registration request schema with OTP verification."""
    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(
        ..., 
        description="User full name",
        min_length=2,
        max_length=255
    )
    country_code: Optional[str] = Field(None, description="Country code")
    phone: Optional[str] = Field(None, description="Phone number")
    address: Optional[str] = Field(None, description="Address")
    children: List[ChildCreate] = Field(default=[], description="Children data")
    terms_accepted: bool = Field(..., description="Terms acceptance")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "country_code": "+1",
                "phone": "1234567890",
                "address": "123 Main St",
                "children": [],
                "terms_accepted": True
            }
        }


class RegisterResponse(BaseModel):
    """User registration response schema."""
    user_id: str = Field(..., description="User UUID")
    email: str = Field(..., description="User email")
    full_name: str = Field(..., description="User full name")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


class LoginResponse(BaseModel):
    """Login response schema with user info and JWT token."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user_id: str = Field(..., description="User UUID")
    email: str = Field(..., description="User email")
    full_name: str = Field(..., description="User full name")
    expires_in: int = Field(..., description="Token expiration time in minutes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "expires_in": 60
            }
        }


class TokenPayload(BaseModel):
    """JWT token payload schema."""
    user_id: str
    email: str
    exp: Optional[datetime] = None
    iat: Optional[datetime] = None


class SignupRequest(BaseModel):
    """Signup request schema - creates user and sends OTP."""
    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(
        ...,
        description="User full name",
        min_length=2,
        max_length=255
    )
    phone: str = Field(..., description="Phone number")
    country_code: Optional[str] = Field(None, description="Country code")
    address: Optional[str] = Field(None, description="Address")
    children: List[ChildCreate] = Field(default=[], description="Children data")
    terms_accepted: bool = Field(..., description="Terms acceptance")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "phone": "1234567890",
                "country_code": "+1",
                "address": "123 Main St",
                "children": [
                    {
                        "name": "Emma Doe",
                        "date_of_birth": "20/05/2015",
                        "gender": "female",
                        "photo": "https://example.com/emma.jpg",
                        "interest": "Drawing, Mathematics"
                    },
                    {
                        "name": "Alex Doe",
                        "date_of_birth": "15/08/2018",
                        "gender": "male",
                        "photo": "https://example.com/alex.jpg",
                        "interest": "Sports, Science"
                    }
                ],
                "terms_accepted": True
            }
        }


class SignupResponse(BaseModel):
    """Signup response - OTP sent."""
    user_id: str = Field(..., description="User UUID")
    message: str = Field(..., description="Success message")
    otp_expires_in: int = Field(..., description="OTP expiration time in minutes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "message": "OTP sent to email and phone",
                "otp_expires_in": 10
            }
        }


class SigninRequest(BaseModel):
    """Signin request - provide email OR phone."""
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "email": "user@example.com",
                    "phone": None
                },
                {
                    "email": None,
                    "phone": "1234567890"
                }
            ]
        }


class VerifyOTPResponse(BaseModel):
    """Unified OTP verification response for signup and signin."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user_id: str = Field(..., description="User UUID")
    email: str = Field(..., description="User email")
    full_name: str = Field(..., description="User full name")
    is_new_user: bool = Field(..., description="Whether this was a signup verification")
    expires_in: int = Field(..., description="Token expiration time in minutes")
    children: List[ChildResponse] = Field(default_factory=list, description="User's children profiles")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_new_user": True,
                "expires_in": 60,
                "children": [
                    {
                        "id": "child-uuid",
                        "name": "Jane Doe",
                        "date_of_birth": "2015-05-15",
                        "gender": "female",
                        "photo": "url",
                        "interest": "Math",
                        "created_at": "2026-01-23T00:00:00",
                        "updated_at": "2026-01-23T00:00:00"
                    }
                ]
            }
        }


class InitiateDeleteRequest(BaseModel):
    """Request to initiate account deletion and send OTP."""
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "phone": None
            }
        }


class VerifyDeleteRequest(BaseModel):
    """Request to verify OTP and complete account deletion."""
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    otp_code: str = Field(
        ...,
        description="OTP code",
        min_length=4,
        max_length=10
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "phone": None,
                "otp_code": "1010"
            }
        }


class DeleteResponse(BaseModel):
    """Response after successful account deletion."""
    message: str = Field(..., description="Success message")
    user_id: str = Field(..., description="Deleted user ID")
    email: str = Field(..., description="Deleted user email")
