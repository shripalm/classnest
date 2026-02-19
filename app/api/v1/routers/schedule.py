from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db_sync
from app.schemas.schedule_schema import (
    TutorScheduleResponse,
    SelectDateRequest,
    SelectTimeSlotRequest,
    UpdateAvailabilityRequest,
    AvailabilityStatusRequest,
    BookingRequest
)
from app.schemas.response import SuccessResponse
from app.repositories.schedule_repository import ScheduleRepository
from app.utils.logging import logger

router = APIRouter(prefix="/api/v1/schedule", tags=["schedule"])


@router.get("/tutor/{tutor_id}/{month}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def get_tutor_availability(
    tutor_id: str = Path(..., description="Tutor ID"),
    month: str = Path(..., description="Month in format 'Jan 2026'"),
    db: Session = Depends(get_db_sync)
):
    """
    Get tutor's availability schedule for a specific month.
    
    **Path parameters:**
    - tutor_id: UUID of the tutor
    - month: Month in format like "Jan 2026"
    
    **Returns:**
    - Tutor schedule with available dates and time slots
    """
    try:
        availability = ScheduleRepository.get_tutor_availability(db, tutor_id, month)
        
        if not availability:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Availability not found for tutor {tutor_id} in {month}"
            )
        
        schedule_data = ScheduleRepository.format_availability_response(availability, tutor_id)
        
        return SuccessResponse(
            status="success",
            message="Tutor availability retrieved successfully",
            data={
                "status": "success",
                "data": [schedule_data]
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving tutor availability: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tutor availability"
        )


@router.get("/month/{month}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def get_all_tutors_schedule(
    month: str = Path(..., description="Month in format 'Jan 2026'"),
    db: Session = Depends(get_db_sync)
):
    """
    Get schedule for all tutors in a specific month.
    
    **Path parameters:**
    - month: Month in format like "Jan 2026"
    
    **Returns:**
    - List of all tutors' schedules for the month
    """
    try:
        schedules = ScheduleRepository.get_all_tutors_schedule(db, month)
        
        return SuccessResponse(
            status="success",
            message="All tutors' schedules retrieved successfully",
            data={
                "status": "success",
                "data": schedules
            }
        )
    except Exception as e:
        logger.error(f"Error retrieving all tutors' schedules: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve schedules"
        )


@router.post("/availability", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_tutor_availability(
    request: UpdateAvailabilityRequest = None,
    db: Session = Depends(get_db_sync)
):
    """
    Create or update tutor availability schedule.
    
    **Request body:**
    - tutor_id: Tutor UUID
    - month: Month like "Jan 2026"
    - timezone: Timezone string
    - duration_minutes: Class duration in minutes
    - available_dates: List of available date objects
    - slots: Time slots organized by period
    """
    try:
        availability = ScheduleRepository.create_or_update_availability(
            db=db,
            tutor_id=request.tutor_id,
            timezone=request.timezone,
            duration_minutes=request.duration_minutes,
            month=request.month,
            available_dates=[date.dict() for date in request.available_dates],
            time_slots={
                "morning": [slot.dict() for slot in request.slots.morning],
                "afternoon": [slot.dict() for slot in request.slots.afternoon],
                "night": [slot.dict() for slot in request.slots.night]
            }
        )
        
        schedule_data = ScheduleRepository.format_availability_response(availability, request.tutor_id)
        
        return SuccessResponse(
            status="success",
            message="Tutor availability created successfully",
            data=schedule_data
        )
    except Exception as e:
        logger.error(f"Error creating tutor availability: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create tutor availability"
        )


@router.post("/select-date", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def select_date(
    request: SelectDateRequest = None,
    db: Session = Depends(get_db_sync)
):
    """
    Select a date in tutor's availability.
    
    **Request body:**
    - tutor_id: Tutor UUID
    - date_key: Date key in format "YYYY-MM-DD"
    """
    try:
        # Extract month from date_key
        month_part = request.date_key[:7]  # YYYY-MM
        month_name = f"{['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(month_part.split('-')[1])]} {month_part.split('-')[0]}"
        
        success = ScheduleRepository.select_date(
            db=db,
            tutor_id=request.tutor_id,
            month=month_name,
            date_key=request.date_key
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Availability not found"
            )
        
        return SuccessResponse(
            status="success",
            message="Date selected successfully",
            data={"date_key": request.date_key}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error selecting date: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to select date"
        )


@router.post("/select-slot", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def select_time_slot(
    request: SelectTimeSlotRequest = None,
    db: Session = Depends(get_db_sync)
):
    """
    Select a time slot in tutor's availability.
    
    **Request body:**
    - tutor_id: Tutor UUID
    - date_key: Date key in format "YYYY-MM-DD"
    - period: Period ("morning", "afternoon", "night")
    - time_key: Time in format "HH:MM"
    """
    try:
        # Extract month from date_key
        month_part = request.date_key[:7]
        month_name = f"{['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(month_part.split('-')[1])]} {month_part.split('-')[0]}"
        
        success = ScheduleRepository.select_time_slot(
            db=db,
            tutor_id=request.tutor_id,
            month=month_name,
            period=request.period,
            time_key=request.time_key
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Availability not found"
            )
        
        return SuccessResponse(
            status="success",
            message="Time slot selected successfully",
            data={
                "period": request.period,
                "time": request.time_key
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error selecting time slot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to select time slot"
        )


@router.patch("/slot-availability", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def update_slot_availability(
    request: AvailabilityStatusRequest = None,
    db: Session = Depends(get_db_sync)
):
    """
    Update availability status of a time slot.
    
    **Request body:**
    - tutor_id: Tutor UUID
    - period: Period ("morning", "afternoon", "night")
    - time: Time in format "HH:MM"
    - is_available: Whether slot is available
    """
    try:
        success = ScheduleRepository.update_slot_availability(
            db=db,
            tutor_id=request.tutor_id,
            period=request.period,
            time=request.time,
            is_available=request.is_available
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Time slot not found"
            )
        
        return SuccessResponse(
            status="success",
            message="Slot availability updated successfully",
            data={
                "period": request.period,
                "time": request.time,
                "is_available": request.is_available
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating slot availability: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update slot availability"
        )


@router.get("/{tutor_id}/available-times/{date_key}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def get_available_times(
    tutor_id: str = Path(..., description="Tutor ID"),
    date_key: str = Path(..., description="Date in format YYYY-MM-DD"),
    db: Session = Depends(get_db_sync)
):
    """
    Get available time slots for a specific date.
    
    **Path parameters:**
    - tutor_id: Tutor UUID
    - date_key: Date in format "YYYY-MM-DD"
    
    **Returns:**
    - Available time slots organized by period
    """
    try:
        available_times = ScheduleRepository.get_available_times_for_date(db, tutor_id, date_key)
        
        return SuccessResponse(
            status="success",
            message="Available times retrieved successfully",
            data=available_times
        )
    except Exception as e:
        logger.error(f"Error retrieving available times: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve available times"
        )


@router.post("/book", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def book_slot(
    request: BookingRequest = None,
    db: Session = Depends(get_db_sync)
):
    """
    Book a time slot with a tutor and create calendar entry.
    
    **Request body:**
    - tutor_id: Tutor UUID
    - date_key: Date in format "YYYY-MM-DD"
    - time: Time in format "HH:MM"
    - period: Period ("morning", "afternoon", "night")
    - student_id: Student UUID (optional)
    - notes: Booking notes (optional)
    """
    try:
        # Verify slot is available
        is_available = ScheduleRepository.check_slot_availability(
            db=db,
            tutor_id=request.tutor_id,
            period=request.period,
            time=request.time
        )
        
        if not is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected time slot is not available"
            )
        
        # Get tutor info for calendar
        from app.models.tutor import Tutor
        tutor = db.query(Tutor).filter(Tutor.id == request.tutor_id).first()
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tutor not found"
            )
        
        # Book slot and create calendar entry
        booking = ScheduleRepository.book_and_schedule(
            db=db,
            tutor_id=request.tutor_id,
            user_id=request.student_id or "",
            date_key=request.date_key,
            time=request.time,
            period=request.period,
            title=tutor.teaches or "Class",
            student_name=request.notes or "Student",
            tutor_name=tutor.name,
            duration_minutes=50,
            color="0xFF7ED957"
        )
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to book slot"
            )
        
        return SuccessResponse(
            status="success",
            message="Booking confirmed and calendar updated",
            data=booking
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error booking slot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to book slot"
        )


@router.delete("/{tutor_id}/clear-selections", status_code=status.HTTP_204_NO_CONTENT)
def clear_selections(
    tutor_id: str = Path(..., description="Tutor ID"),
    month: str = Query(..., description="Month in format 'Jan 2026'"),
    db: Session = Depends(get_db_sync)
):
    """
    Clear all date and time selections for a tutor's availability.
    
    **Path parameters:**
    - tutor_id: Tutor UUID
    
    **Query parameters:**
    - month: Month in format like "Jan 2026"
    """
    try:
        success = ScheduleRepository.clear_selections(db, tutor_id, month)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Availability not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing selections: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear selections"
        )


@router.delete("/{tutor_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_availability(
    tutor_id: str = Path(..., description="Tutor ID"),
    month: str = Query(..., description="Month in format 'Jan 2026'"),
    db: Session = Depends(get_db_sync)
):
    """
    Deactivate tutor availability for a month.
    
    **Path parameters:**
    - tutor_id: Tutor UUID
    
    **Query parameters:**
    - month: Month in format like "Jan 2026"
    """
    try:
        success = ScheduleRepository.deactivate_availability(db, tutor_id, month)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Availability not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deactivating availability: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate availability"
        )


@router.post("/sync-to-calendar/{tutor_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def sync_availability_to_calendar(
    tutor_id: str = Path(..., description="Tutor ID"),
    month: str = Query(..., description="Month in format 'Jan 2026'"),
    db: Session = Depends(get_db_sync)
):
    """
    Sync tutor availability to calendar as quick view events.
    
    **Path parameters:**
    - tutor_id: Tutor UUID
    
    **Query parameters:**
    - month: Month in format like "Jan 2026"
    """
    try:
        availability = ScheduleRepository.get_tutor_availability(db, tutor_id, month)
        
        if not availability:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Availability not found"
            )
        
        from app.models.tutor import Tutor
        tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
        tutor_name = tutor.name if tutor else "Tutor"
        
        success = ScheduleRepository.sync_availability_to_calendar(
            db=db,
            tutor_id=tutor_id,
            availability=availability,
            tutor_name=tutor_name,
            color="0xFF7ED957"
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to sync to calendar"
            )
        
        return SuccessResponse(
            status="success",
            message="Availability synced to calendar successfully",
            data={
                "tutor_id": tutor_id,
                "month": month,
                "synced": True
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error syncing to calendar: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sync to calendar"
        )


@router.get("/booking/{user_id}/{tutor_id}/{date_key}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def get_booking_details(
    user_id: str = Path(..., description="User ID"),
    tutor_id: str = Path(..., description="Tutor ID"),
    date_key: str = Path(..., description="Date in format YYYY-MM-DD"),
    db: Session = Depends(get_db_sync)
):
    """
    Get booking details with calendar information.
    
    **Path parameters:**
    - user_id: User UUID
    - tutor_id: Tutor UUID
    - date_key: Date in format "YYYY-MM-DD"
    
    **Returns:**
    - Schedule and calendar data for the booking
    """
    try:
        booking = ScheduleRepository.get_schedule_with_calendar(
            db=db,
            user_id=user_id,
            tutor_id=tutor_id,
            date_key=date_key
        )
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        return SuccessResponse(
            status="success",
            message="Booking details retrieved successfully",
            data=booking
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving booking details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve booking details"
        )


@router.patch("/booking/{user_id}/{schedule_id}/status", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def update_booking_status(
    user_id: str = Path(..., description="User ID"),
    schedule_id: str = Path(..., description="Schedule ID"),
    new_status: str = Query(..., description="New status (completed, missed, cancelled, etc.)"),
    db: Session = Depends(get_db_sync)
):
    """
    Update booking status and sync to calendar.
    
    **Path parameters:**
    - user_id: User UUID
    - schedule_id: Schedule UUID
    
    **Query parameters:**
    - new_status: Status to set (completed, missed, cancelled, rescheduled)
    """
    try:
        success = ScheduleRepository.update_booking_status(
            db=db,
            user_id=user_id,
            schedule_id=schedule_id,
            new_status=new_status
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Schedule not found"
            )
        
        return SuccessResponse(
            status="success",
            message="Booking status updated successfully",
            data={
                "schedule_id": schedule_id,
                "status": new_status
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating booking status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update booking status"
        )
