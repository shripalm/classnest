from fastapi import APIRouter
from app.utils.logging import logger

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check requested, and App is healthy.")
    return {
        "status": "healthy",
        "message": "API is running"
    }
