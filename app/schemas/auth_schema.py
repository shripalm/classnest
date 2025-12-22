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
    name: str
    email: EmailStr
    country_code: str
    phone: str
    password: str
    confirm_password: str
    address: str
    children: List[ChildCreate]
    terms_accepted: bool

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, v):
        if not v or len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError("Passwords do not match")
        return v

    @field_validator("terms_accepted")
    @classmethod
    def terms_must_be_accepted(cls, v):
        if not v:
            raise ValueError("Terms must be accepted")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    username: str
    name: Optional[str]
    phone: Optional[str]
    country_code: Optional[str]
    address: Optional[str]
    is_active: bool
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
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema - accepts email or username."""
    email_or_username: str = Field(
        ..., 
        description="Email address or username",
        min_length=3,
        max_length=255,
        examples=["user@example.com", "john_doe"]
    )
    password: str = Field(
        ..., 
        description="User password",
        min_length=6,
        max_length=100
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email_or_username": "user@example.com",
                "password": "yourpassword123"
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


class RegisterRequest(BaseModel):
    """User registration request schema."""
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(
        ..., 
        description="Username",
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_-]+$"
    )
    password: str = Field(
        ..., 
        description="User password",
        min_length=8,
        max_length=100
    )
    full_name: str = Field(
        ..., 
        description="User full name",
        min_length=2,
        max_length=255
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "john_doe",
                "password": "SecurePass123!",
                "full_name": "John Doe"
            }
        }


class RegisterResponse(BaseModel):
    """User registration response schema."""
    user_id: str = Field(..., description="User UUID")
    email: str = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="User full name")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "username": "john_doe",
                "full_name": "John Doe",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
