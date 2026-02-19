from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Index, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class CalendarEvent(Base):
    """CalendarEvent model for storing calendar events (quick view)."""
    __tablename__ = "calendar_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    event_date = Column(String(10), nullable=False)  # Format: YYYY-MM-DD
    event_id = Column(String(100), nullable=False)  # Reference to class/tutor id
    title = Column(String(255), nullable=False)
    color = Column(String(20), nullable=False)  # Hex color code like "0xFFF4A3A3"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_calendar_events_user_id', 'user_id'),
        Index('idx_calendar_events_event_date', 'event_date'),
        Index('idx_calendar_events_user_date', 'user_id', 'event_date'),
    )

    def __repr__(self):
        return f"<CalendarEvent(id={self.id}, title={self.title}, date={self.event_date})>"


class DailySchedule(Base):
    """DailySchedule model for storing detailed daily class schedules."""
    __tablename__ = "daily_schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    schedule_date = Column(String(10), nullable=False)  # Format: YYYY-MM-DD
    class_id = Column(String(100), nullable=False)  # Reference to class id
    start_time = Column(String(5), nullable=False)   # Format: HH:MM
    end_time = Column(String(5), nullable=False)     # Format: HH:MM
    title = Column(String(255), nullable=False)
    students = Column(JSON, default=[], nullable=False)  # Array of student names
    student_colors = Column(JSON, default=[], nullable=False)  # Array of hex colors
    status = Column(String(50), nullable=False)  # "completed", "missed", "upcoming", etc.
    can_reschedule = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_daily_schedules_user_id', 'user_id'),
        Index('idx_daily_schedules_schedule_date', 'schedule_date'),
        Index('idx_daily_schedules_user_date', 'user_id', 'schedule_date'),
    )

    def __repr__(self):
        return f"<DailySchedule(id={self.id}, title={self.title}, date={self.schedule_date})>"


class CalendarMonth(Base):
    """CalendarMonth model for storing month metadata."""
    __tablename__ = "calendar_months"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    month = Column(String(7), nullable=False)  # Format: YYYY-MM
    today = Column(String(10), nullable=False)  # Format: YYYY-MM-DD
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_calendar_months_user_id', 'user_id'),
        Index('idx_calendar_months_month', 'month'),
    )

    def __repr__(self):
        return f"<CalendarMonth(id={self.id}, month={self.month})>"
