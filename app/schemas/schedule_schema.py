from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class DateInfo(BaseModel):
    """Schema for date information in schedule."""
    day: str  # "Mon", "Tue", etc.
    date: int  # Day of month
    key: str  # "2026-01-19" format
    is_today: bool = False


class TimeSlotInfo(BaseModel):
    """Schema for individual time slot."""
    id: str  # "m_0700", "a_1400", etc.
    time: str  # "HH:MM" format
    key: str  # Same as time
    is_available: bool
    is_selected: bool = False


class SlotPeriods(BaseModel):
    """Schema for time slots organized by period."""
    morning: List[TimeSlotInfo]
    afternoon: List[TimeSlotInfo]
    night: List[TimeSlotInfo]


class SelectedSlot(BaseModel):
    """Schema for selected time slot in a period."""
    key: str = ""  # Time key or empty


class SelectedSlots(BaseModel):
    """Schema for all selected slots by period."""
    morning: SelectedSlot = Field(default_factory=SelectedSlot)
    afternoon: SelectedSlot = Field(default_factory=SelectedSlot)
    night: SelectedSlot = Field(default_factory=SelectedSlot)


class ScheduleParams(BaseModel):
    """Schema for schedule selection parameters."""
    selected_date_key: str = ""
    slots: SelectedSlots = Field(default_factory=SelectedSlots)


class TutorScheduleData(BaseModel):
    """Schema for individual tutor's schedule."""
    id: str  # Tutor ID
    time_zone: str = Field(alias="timeZone")
    duration: str  # "50 min"
    month: str  # "Jan 2026"
    today: str = "today"
    dates: List[DateInfo]
    slots: SlotPeriods
    params: ScheduleParams

    class Config:
        populate_by_name = True


class TutorScheduleResponse(BaseModel):
    """Schema for tutor availability API response."""
    status: str = "success"
    data: List[TutorScheduleData]


# Request/Update Schemas

class SelectDateRequest(BaseModel):
    """Schema for selecting a date in the schedule."""
    tutor_id: str
    date_key: str  # "2026-01-19" format


class SelectTimeSlotRequest(BaseModel):
    """Schema for selecting a time slot."""
    tutor_id: str
    date_key: str
    period: str  # "morning", "afternoon", "night"
    time_key: str  # "07:00", "14:00", etc.


class UpdateAvailabilityRequest(BaseModel):
    """Schema for updating tutor availability."""
    tutor_id: str
    month: str
    timezone: str
    duration_minutes: int
    available_dates: List[DateInfo]
    slots: SlotPeriods


class AvailabilityStatusRequest(BaseModel):
    """Schema for updating availability status of a slot."""
    tutor_id: str
    period: str
    time: str
    is_available: bool


class BookingRequest(BaseModel):
    """Schema for booking a time slot."""
    tutor_id: str
    date_key: str  # "2026-01-19"
    time: str  # "14:00"
    period: str  # "morning", "afternoon", "night"
    student_id: Optional[str] = None
    notes: Optional[str] = None
