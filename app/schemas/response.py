from pydantic import BaseModel
from typing import Any, Generic, TypeVar, Optional, Dict

T = TypeVar('T')


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response schema."""
    status: str = "success"
    message: str
    data: Optional[T] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully",
                "data": {}
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    status: str = "error"
    message: str
    data: dict[str, Any] = {}
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "An error occurred",
                "data": {}
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema."""
    status: str = "success"
    message: str
    data: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Data retrieved successfully",
                "data": [],
                "total": 100,
                "page": 1,
                "page_size": 20,
                "total_pages": 5
            }
        }

class StandardResponse(BaseModel, Generic[T]):
    """
    Standard API response format for all endpoints
    """
    status: str
    message: str
    data: T = {}

    class Config:
        json_encoders = {
            # Add custom encoders if needed
        }

class CreatedResponse(StandardResponse[T]):
    """
    Standard created response
    """
    status: str = "201"
    message: str = "Success"
    data: T = {}

class NoContentResponse(StandardResponse[None]):
    """
    Standard no content response for delete operations
    """
    status: str = "204"
    message: str = "Success"
    data: dict = {}
