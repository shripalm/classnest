from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class CalendarEventItem(BaseModel):
    """Schema for a calendar event (quick view on calendar grid)."""
    id: str
    title: str
    color: str  # Hex color like "0xFFF4A3A3"

    class Config:
        from_attributes = True


class TimeSlot(BaseModel):
    """Schema for time slot."""
    start: str  # Format: HH:MM
    end: str    # Format: HH:MM


class DailyScheduleItem(BaseModel):
    """Schema for a daily schedule item (detailed class info)."""
    id: str
    time: TimeSlot
    title: str
    students: List[str]
    colors: Optional[List[str]] = []  # Student color indicators
    status: str  # "completed", "missed", "upcoming", "cancelled", etc.
    can_reschedule: bool = Field(alias="canReschedule")

    class Config:
        from_attributes = True
        populate_by_name = True


class DailyScheduleItemCreate(BaseModel):
    """Schema for creating a daily schedule item."""
    schedule_date: str  # Format: YYYY-MM-DD
    class_id: str
    start_time: str  # Format: HH:MM
    end_time: str    # Format: HH:MM
    title: str
    students: List[str]
    student_colors: Optional[List[str]] = []
    status: str
    can_reschedule: bool = False
    notes: Optional[str] = None


class CalendarMonthData(BaseModel):
    """Schema for calendar month data."""
    month: str  # Format: YYYY-MM
    today: str  # Format: YYYY-MM-DD
    calendar: Dict[str, List[CalendarEventItem]]  # Dict of date -> list of events
    daily_schedule: Dict[str, List[DailyScheduleItem]] = Field(alias="dailySchedule")

    class Config:
        populate_by_name = True


class CalendarResponse(BaseModel):
    """Schema for calendar API response."""
    data: List[CalendarMonthData]

    class Config:
        populate_by_name = True


class CalendarEventCreate(BaseModel):
    """Schema for creating a calendar event."""
    event_date: str  # Format: YYYY-MM-DD
    event_id: str
    title: str
    color: str


class CalendarEventUpdate(BaseModel):
    """Schema for updating a calendar event."""
    title: Optional[str] = None
    color: Optional[str] = None


class DailyScheduleUpdate(BaseModel):
    """Schema for updating daily schedule."""
    status: Optional[str] = None
    students: Optional[List[str]] = None
    student_colors: Optional[List[str]] = None
    notes: Optional[str] = None
    can_reschedule: Optional[bool] = None


class CalendarMonthCreate(BaseModel):
    """Schema for creating/updating calendar month metadata."""
    month: str  # Format: YYYY-MM
    today: str  # Format: YYYY-MM-DD


class RescheduleRequest(BaseModel):
    """Schema for rescheduling a class."""
    schedule_id: str
    new_date: str  # Format: YYYY-MM-DD
    new_start_time: str  # Format: HH:MM
    new_end_time: str    # Format: HH:MM
    reason: Optional[str] = None
