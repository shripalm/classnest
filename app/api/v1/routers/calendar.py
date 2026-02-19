from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db_sync
from app.schemas.calendar_schema import (
    CalendarResponse,
    CalendarEventCreate,
    CalendarEventUpdate,
    DailyScheduleItemCreate,
    DailyScheduleUpdate,
    CalendarMonthCreate,
    RescheduleRequest
)
from app.schemas.response import SuccessResponse
from app.repositories.calendar_repository import CalendarRepository
from app.utils.logging import logger

router = APIRouter(prefix="/api/v1/calendar", tags=["calendar"])


@router.get("/{user_id}/{month}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def get_calendar_month(
    user_id: str = Path(..., description="User ID"),
    month: str = Path(..., description="Month in format YYYY-MM"),
    db: Session = Depends(get_db_sync)
):
    """
    Get calendar data for a specific month.
    
    **Path parameters:**
    - user_id: UUID of the user
    - month: Month in format YYYY-MM (e.g., "2026-01")
    
    **Returns:**
    - month: The requested month
    - today: Today's date
    - calendar: Dictionary of dates with quick event previews
    - dailySchedule: Detailed schedule for each date
    """
    try:
        calendar_data = CalendarRepository.get_calendar_month(db, user_id, month)
        
        if not calendar_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Calendar data not found for month {month}"
            )
        
        return SuccessResponse(
            status="success",
            message="Calendar retrieved successfully",
            data={"data": [calendar_data]}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving calendar for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve calendar"
        )


@router.post("/{user_id}/month", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_calendar_month(
    user_id: str = Path(..., description="User ID"),
    month_data: CalendarMonthCreate = None,
    db: Session = Depends(get_db_sync)
):
    """
    Create or update calendar month metadata.
    
    **Path parameters:**
    - user_id: UUID of the user
    
    **Request body:**
    - month: Month in format YYYY-MM
    - today: Today's date in format YYYY-MM-DD
    """
    try:
        calendar_month = CalendarRepository.create_calendar_month(
            db=db,
            user_id=user_id,
            month=month_data.month,
            today=month_data.today
        )
        
        return SuccessResponse(
            status="success",
            message="Calendar month created successfully",
            data={
                "id": str(calendar_month.id),
                "month": calendar_month.month,
                "today": calendar_month.today
            }
        )
    except Exception as e:
        logger.error(f"Error creating calendar month: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create calendar month"
        )


@router.post("/{user_id}/event", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def add_calendar_event(
    user_id: str = Path(..., description="User ID"),
    event: CalendarEventCreate = None,
    db: Session = Depends(get_db_sync)
):
    """
    Add a calendar event to a specific date.
    
    **Path parameters:**
    - user_id: UUID of the user
    
    **Request body:**
    - event_date: Date in format YYYY-MM-DD
    - event_id: Reference ID (e.g., tutor ID)
    - title: Event title (e.g., student name)
    - color: Hex color code (e.g., "0xFFF4A3A3")
    """
    try:
        calendar_event = CalendarRepository.add_calendar_event(
            db=db,
            user_id=user_id,
            event_date=event.event_date,
            event_id=event.event_id,
            title=event.title,
            color=event.color
        )
        
        return SuccessResponse(
            status="success",
            message="Calendar event added successfully",
            data={
                "id": str(calendar_event.id),
                "date": calendar_event.event_date,
                "title": calendar_event.title,
                "color": calendar_event.color
            }
        )
    except Exception as e:
        logger.error(f"Error adding calendar event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add calendar event"
        )


@router.patch("/{user_id}/event/{event_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def update_calendar_event(
    user_id: str = Path(..., description="User ID"),
    event_id: str = Path(..., description="Calendar Event ID"),
    update_data: CalendarEventUpdate = None,
    db: Session = Depends(get_db_sync)
):
    """
    Update a calendar event.
    
    **Path parameters:**
    - user_id: UUID of the user
    - event_id: UUID of the calendar event
    
    **Request body:**
    - title: New title (optional)
    - color: New color (optional)
    """
    try:
        success = CalendarRepository.update_calendar_event(
            db=db,
            user_id=user_id,
            event_id=event_id,
            title=update_data.title,
            color=update_data.color
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Calendar event not found"
            )
        
        return SuccessResponse(
            status="success",
            message="Calendar event updated successfully",
            data={"id": event_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating calendar event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update calendar event"
        )


@router.delete("/{user_id}/event/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_calendar_event(
    user_id: str = Path(..., description="User ID"),
    event_id: str = Path(..., description="Calendar Event ID"),
    db: Session = Depends(get_db_sync)
):
    """
    Remove a calendar event.
    
    **Path parameters:**
    - user_id: UUID of the user
    - event_id: UUID of the calendar event
    """
    try:
        success = CalendarRepository.remove_calendar_event(db, user_id, event_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Calendar event not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing calendar event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove calendar event"
        )


@router.post("/{user_id}/schedule", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def add_daily_schedule(
    user_id: str = Path(..., description="User ID"),
    schedule: DailyScheduleItemCreate = None,
    db: Session = Depends(get_db_sync)
):
    """
    Add a daily schedule item.
    
    **Path parameters:**
    - user_id: UUID of the user
    
    **Request body:**
    - class_id: Class ID reference
    - start_time: Start time in format HH:MM
    - end_time: End time in format HH:MM
    - title: Class title
    - students: List of student names
    - student_colors: List of hex color codes for each student
    - status: Class status (completed, missed, upcoming, etc.)
    - can_reschedule: Whether the class can be rescheduled
    - notes: Additional notes (optional)
    """
    try:
        daily_schedule = CalendarRepository.add_daily_schedule(
            db=db,
            user_id=user_id,
            schedule_date=schedule.schedule_date,
            class_id=schedule.class_id,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            title=schedule.title,
            students=schedule.students,
            student_colors=schedule.student_colors,
            status=schedule.status,
            can_reschedule=schedule.can_reschedule,
            notes=schedule.notes
        )
        
        return SuccessResponse(
            status="success",
            message="Daily schedule added successfully",
            data={
                "id": str(daily_schedule.id),
                "date": daily_schedule.schedule_date,
                "title": daily_schedule.title
            }
        )
    except Exception as e:
        logger.error(f"Error adding daily schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add daily schedule"
        )


@router.get("/{user_id}/schedule/{date}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def get_daily_schedule_by_date(
    user_id: str = Path(..., description="User ID"),
    date: str = Path(..., description="Date in format YYYY-MM-DD"),
    db: Session = Depends(get_db_sync)
):
    """
    Get all schedules for a specific date.
    
    **Path parameters:**
    - user_id: UUID of the user
    - date: Date in format YYYY-MM-DD
    
    **Returns:**
    - List of schedule items for the date
    """
    try:
        schedules = CalendarRepository.get_daily_schedule(db, user_id, date)
        
        return SuccessResponse(
            status="success",
            message="Daily schedule retrieved successfully",
            data={"schedules": schedules}
        )
    except Exception as e:
        logger.error(f"Error retrieving daily schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve daily schedule"
        )


@router.patch("/{user_id}/schedule/{schedule_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def update_daily_schedule(
    user_id: str = Path(..., description="User ID"),
    schedule_id: str = Path(..., description="Schedule ID"),
    update_data: DailyScheduleUpdate = None,
    db: Session = Depends(get_db_sync)
):
    """
    Update a daily schedule item.
    
    **Path parameters:**
    - user_id: UUID of the user
    - schedule_id: UUID of the schedule
    
    **Request body:**
    - status: New status (optional)
    - students: New student list (optional)
    - student_colors: New color list (optional)
    - notes: New notes (optional)
    - can_reschedule: New reschedule status (optional)
    """
    try:
        success = CalendarRepository.update_daily_schedule(
            db=db,
            user_id=user_id,
            schedule_id=schedule_id,
            status=update_data.status,
            students=update_data.students,
            student_colors=update_data.student_colors,
            notes=update_data.notes,
            can_reschedule=update_data.can_reschedule
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Schedule not found"
            )
        
        return SuccessResponse(
            status="success",
            message="Daily schedule updated successfully",
            data={"id": schedule_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating daily schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update daily schedule"
        )


@router.post("/{user_id}/reschedule/{schedule_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def reschedule_class(
    user_id: str = Path(..., description="User ID"),
    schedule_id: str = Path(..., description="Schedule ID"),
    reschedule_req: RescheduleRequest = None,
    db: Session = Depends(get_db_sync)
):
    """
    Reschedule a class to a new date and time.
    
    **Path parameters:**
    - user_id: UUID of the user
    - schedule_id: UUID of the schedule
    
    **Request body:**
    - new_date: New date in format YYYY-MM-DD
    - new_start_time: New start time in format HH:MM
    - new_end_time: New end time in format HH:MM
    - reason: Reason for rescheduling (optional)
    """
    try:
        success = CalendarRepository.reschedule_class(
            db=db,
            user_id=user_id,
            schedule_id=schedule_id,
            new_date=reschedule_req.new_date,
            new_start_time=reschedule_req.new_start_time,
            new_end_time=reschedule_req.new_end_time
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Schedule not found or cannot be rescheduled"
            )
        
        return SuccessResponse(
            status="success",
            message="Class rescheduled successfully",
            data={"id": schedule_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rescheduling class: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reschedule class"
        )


@router.delete("/{user_id}/schedule/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_daily_schedule(
    user_id: str = Path(..., description="User ID"),
    schedule_id: str = Path(..., description="Schedule ID"),
    db: Session = Depends(get_db_sync)
):
    """
    Remove a daily schedule item.
    
    **Path parameters:**
    - user_id: UUID of the user
    - schedule_id: UUID of the schedule
    """
    try:
        success = CalendarRepository.remove_daily_schedule(db, user_id, schedule_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Schedule not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing daily schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove daily schedule"
        )


@router.get("/{user_id}/upcoming", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def get_upcoming_schedules(
    user_id: str = Path(..., description="User ID"),
    db: Session = Depends(get_db_sync)
):
    """
    Get all upcoming schedules for a user.
    
    **Path parameters:**
    - user_id: UUID of the user
    
    **Returns:**
    - List of upcoming schedules sorted by date and time
    """
    try:
        schedules = CalendarRepository.get_all_upcoming_schedules(db, user_id)
        
        return SuccessResponse(
            status="success",
            message="Upcoming schedules retrieved successfully",
            data={"schedules": schedules}
        )
    except Exception as e:
        logger.error(f"Error retrieving upcoming schedules: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve upcoming schedules"
        )
