from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Index, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class TutorAvailability(Base):
    """TutorAvailability model for storing tutor availability schedule."""
    __tablename__ = "tutor_availabilities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutors.id"), nullable=False, index=True)
    timezone = Column(String(100), default="Asia/Singapore (GMT +8:00)", nullable=False)
    duration_minutes = Column(Integer, default=50, nullable=False)
    month = Column(String(20), nullable=False)  # e.g., "Jan 2026"
    
    # JSON fields for flexible storage
    available_dates = Column(JSON, default=[], nullable=False)  # Array of date objects
    time_slots = Column(JSON, default={}, nullable=False)  # { "morning": [...], "afternoon": [...], "night": [...] }
    
    # Track selected preferences
    selected_date_key = Column(String(20), nullable=True)  # YYYY-MM-DD
    selected_slots = Column(JSON, default={}, nullable=False)  # { "morning": {...}, "afternoon": {...}, "night": {...} }
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_tutor_availabilities_tutor_id', 'tutor_id'),
        Index('idx_tutor_availabilities_month', 'month'),
    )

    def __repr__(self):
        return f"<TutorAvailability(id={self.id}, tutor_id={self.tutor_id}, month={self.month})>"


class TimeSlot(Base):
    """TimeSlot model for storing individual time slot availability."""
    __tablename__ = "time_slots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    tutor_availability_id = Column(UUID(as_uuid=True), ForeignKey("tutor_availabilities.id"), nullable=False, index=True)
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutors.id"), nullable=False, index=True)
    
    # Time slot information
    slot_id = Column(String(50), nullable=False)  # e.g., "m_0700", "a_1400"
    time = Column(String(5), nullable=False)      # HH:MM format
    period = Column(String(20), nullable=False)   # "morning", "afternoon", "night"
    
    # Availability status
    is_available = Column(Boolean, default=True, nullable=False)
    is_selected = Column(Boolean, default=False, nullable=False)
    
    # Associated dates
    available_dates = Column(JSON, default=[], nullable=False)  # Array of date keys
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_time_slots_tutor_availability_id', 'tutor_availability_id'),
        Index('idx_time_slots_tutor_id', 'tutor_id'),
        Index('idx_time_slots_period', 'period'),
    )

    def __repr__(self):
        return f"<TimeSlot(id={self.id}, slot_id={self.slot_id}, time={self.time})>"


class AvailableDate(Base):
    """AvailableDate model for storing available dates in tutor schedule."""
    __tablename__ = "available_dates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    tutor_availability_id = Column(UUID(as_uuid=True), ForeignKey("tutor_availabilities.id"), nullable=False, index=True)
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutors.id"), nullable=False, index=True)
    
    # Date information
    day = Column(String(3), nullable=False)        # "Mon", "Tue", etc.
    date = Column(Integer, nullable=False)         # Day of month (1-31)
    date_key = Column(String(10), nullable=False)  # YYYY-MM-DD format
    is_today = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_available_dates_tutor_availability_id', 'tutor_availability_id'),
        Index('idx_available_dates_tutor_id', 'tutor_id'),
        Index('idx_available_dates_date_key', 'date_key'),
    )

    def __repr__(self):
        return f"<AvailableDate(id={self.id}, date_key={self.date_key}, day={self.day})>"
