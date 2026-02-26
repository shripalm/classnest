from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.api.v1.routers import courses, health, auth, dev_settings, subjects, tutors, favorites, schools, cart, calendar, schedule, classes

from app.core.config import settings
from app.utils.logging import logger

from app.middleware.logging_middleware import LoggingMiddleware
from app.utils.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import sys
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    root_path=settings.STAGE_PATH
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("App running", stage=settings.STAGE_PATH)

# Add exception handlers for standardized error responses
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Register middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/v1", tags=["courses - subjects and classes"])
app.include_router(subjects.router, prefix="/api/v1", tags=["courses - subjects and classes"])
app.include_router(classes.router, prefix="/api/v1", tags=["courses - subjects and classes"])
app.include_router(tutors.router, prefix="/api/v1", tags=["tutors"])
app.include_router(favorites.router, prefix="/api/v1", tags=["favorites"])
app.include_router(schools.router, prefix="/api/v1", tags=["schools"])
app.include_router(cart.router, tags=["cart"])
app.include_router(calendar.router, tags=["calendar"])
app.include_router(schedule.router, tags=["schedule"])
app.include_router(dev_settings.router, prefix="/api/v1/dev_settings", tags=["dev_settings"])

from app.db.listeners import before_cursor_execute, after_cursor_execute
from sqlalchemy import event
from app.db.session import async_engine as engine

@app.on_event("startup")
async def on_startup():
    # Register SQLAlchemy event listeners
    event.listen(engine.sync_engine, "before_cursor_execute", before_cursor_execute)
    event.listen(engine.sync_engine, "after_cursor_execute", after_cursor_execute)
    logger.info("Application startup complete")
    await health.health_check()
    
    # Run Alembic migrations to head
    try:
        logger.info("++++++++++++++++++++++++++++++++++++++++++++")
        logger.info("Running Alembic migrations to head")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True,
            text=True,
            timeout=300
        )
        print(result.stdout)
        print(result.stderr)
        if result.returncode == 0:
            logger.info("Alembic migrations completed successfully")
        else:
            logger.error(
                "Alembic migration failed",
                stdout=result.stdout,
                stderr=result.stderr
            )
    except subprocess.TimeoutExpired:
        logger.error("Alembic migration timed out")
    except Exception as e:
        logger.error(f"Failed to run Alembic migrations: {str(e)}")
    logger.info("Running Alembic migrations to head is done")
    logger.info("++++++++++++++++++++++++++++++++++++++++++++")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Application shutdown")
    pass
