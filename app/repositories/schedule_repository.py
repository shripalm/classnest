from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import uuid4
from typing import List, Dict, Any, Optional
from app.models.schedule import TutorAvailability, TimeSlot, AvailableDate
from app.models.calendar import DailySchedule, CalendarEvent
from datetime import datetime


class ScheduleRepository:
    """Repository for tutor availability schedule operations."""

    @staticmethod
    def get_tutor_availability(db: Session, tutor_id: str, month: str) -> Optional[TutorAvailability]:
        """Get tutor availability for a specific month."""
        return db.query(TutorAvailability).filter(
            and_(
                TutorAvailability.tutor_id == tutor_id,
                TutorAvailability.month == month
            )
        ).first()

    @staticmethod
    def create_or_update_availability(
        db: Session,
        tutor_id: str,
        timezone: str,
        duration_minutes: int,
        month: str,
        available_dates: List[Dict[str, Any]],
        time_slots: Dict[str, List[Dict[str, Any]]]
    ) -> TutorAvailability:
        """Create or update tutor availability."""
        availability = db.query(TutorAvailability).filter(
            and_(
                TutorAvailability.tutor_id == tutor_id,
                TutorAvailability.month == month
            )
        ).first()

        if availability:
            availability.timezone = timezone
            availability.duration_minutes = duration_minutes
            availability.available_dates = available_dates
            availability.time_slots = time_slots
            availability.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(availability)
            return availability

        availability = TutorAvailability(
            id=uuid4(),
            tutor_id=tutor_id,
            timezone=timezone,
            duration_minutes=duration_minutes,
            month=month,
            available_dates=available_dates,
            time_slots=time_slots,
            selected_slots={
                "morning": {"key": ""},
                "afternoon": {"key": ""},
                "night": {"key": ""}
            }
        )
        db.add(availability)
        db.commit()
        db.refresh(availability)
        return availability

    @staticmethod
    def format_availability_response(availability: TutorAvailability, tutor_id: str) -> Dict[str, Any]:
        """Format TutorAvailability into API response format."""
        return {
            "id": str(tutor_id),
            "timeZone": availability.timezone,
            "duration": f"{availability.duration_minutes} min",
            "month": availability.month,
            "today": "today",
            "dates": availability.available_dates,
            "slots": availability.time_slots,
            "params": {
                "selectedDateKey": availability.selected_date_key or "",
                "slots": availability.selected_slots
            }
        }

    @staticmethod
    def get_all_tutors_schedule(db: Session, month: str) -> List[Dict[str, Any]]:
        """Get schedule for all tutors in a month."""
        availabilities = db.query(TutorAvailability).filter(
            TutorAvailability.month == month
        ).all()

        result = []
        for availability in availabilities:
            result.append(
                ScheduleRepository.format_availability_response(
                    availability,
                    str(availability.tutor_id)
                )
            )
        return result

    @staticmethod
    def select_date(
        db: Session,
        tutor_id: str,
        month: str,
        date_key: str
    ) -> bool:
        """Select a date in the tutor's availability."""
        availability = db.query(TutorAvailability).filter(
            and_(
                TutorAvailability.tutor_id == tutor_id,
                TutorAvailability.month == month
            )
        ).first()

        if not availability:
            return False

        availability.selected_date_key = date_key
        availability.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def select_time_slot(
        db: Session,
        tutor_id: str,
        month: str,
        period: str,
        time_key: str
    ) -> bool:
        """Select a time slot in the tutor's availability."""
        availability = db.query(TutorAvailability).filter(
            and_(
                TutorAvailability.tutor_id == tutor_id,
                TutorAvailability.month == month
            )
        ).first()

        if not availability:
            return False

        # Update selected slots
        if availability.selected_slots is None:
            availability.selected_slots = {
                "morning": {"key": ""},
                "afternoon": {"key": ""},
                "night": {"key": ""}
            }

        if period in availability.selected_slots:
            availability.selected_slots[period] = {"key": time_key}

        availability.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def add_time_slot(
        db: Session,
        tutor_availability_id: str,
        tutor_id: str,
        slot_id: str,
        time: str,
        period: str,
        is_available: bool,
        available_dates: List[str] = None
    ) -> TimeSlot:
        """Add a time slot to tutor availability."""
        time_slot = TimeSlot(
            id=uuid4(),
            tutor_availability_id=tutor_availability_id,
            tutor_id=tutor_id,
            slot_id=slot_id,
            time=time,
            period=period,
            is_available=is_available,
            available_dates=available_dates or []
        )
        db.add(time_slot)
        db.commit()
        db.refresh(time_slot)
        return time_slot

    @staticmethod
    def update_slot_availability(
        db: Session,
        tutor_id: str,
        period: str,
        time: str,
        is_available: bool
    ) -> bool:
        """Update availability status of a time slot."""
        slot = db.query(TimeSlot).filter(
            and_(
                TimeSlot.tutor_id == tutor_id,
                TimeSlot.period == period,
                TimeSlot.time == time
            )
        ).first()

        if not slot:
            return False

        slot.is_available = is_available
        slot.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def add_available_date(
        db: Session,
        tutor_availability_id: str,
        tutor_id: str,
        day: str,
        date: int,
        date_key: str,
        is_today: bool = False
    ) -> AvailableDate:
        """Add an available date to tutor's schedule."""
        available_date = AvailableDate(
            id=uuid4(),
            tutor_availability_id=tutor_availability_id,
            tutor_id=tutor_id,
            day=day,
            date=date,
            date_key=date_key,
            is_today=is_today
        )
        db.add(available_date)
        db.commit()
        db.refresh(available_date)
        return available_date

    @staticmethod
    def get_available_dates(
        db: Session,
        tutor_id: str,
        month: str
    ) -> List[Dict[str, Any]]:
        """Get all available dates for a tutor in a month."""
        availability = db.query(TutorAvailability).filter(
            and_(
                TutorAvailability.tutor_id == tutor_id,
                TutorAvailability.month == month
            )
        ).first()

        if not availability:
            return []

        dates = db.query(AvailableDate).filter(
            AvailableDate.tutor_availability_id == availability.id
        ).all()

        result = []
        for date in dates:
            result.append({
                "day": date.day,
                "date": date.date,
                "key": date.date_key,
                "isToday": date.is_today
            })
        return result

    @staticmethod
    def get_period_slots(
        db: Session,
        tutor_id: str,
        period: str,
        month: str
    ) -> List[Dict[str, Any]]:
        """Get time slots for a specific period."""
        availability = db.query(TutorAvailability).filter(
            and_(
                TutorAvailability.tutor_id == tutor_id,
                TutorAvailability.month == month
            )
        ).first()

        if not availability or not availability.time_slots.get(period):
            return []

        return availability.time_slots[period]

    @staticmethod
    def check_slot_availability(
        db: Session,
        tutor_id: str,
        period: str,
        time: str
    ) -> bool:
        """Check if a specific time slot is available."""
        slot = db.query(TimeSlot).filter(
            and_(
                TimeSlot.tutor_id == tutor_id,
                TimeSlot.period == period,
                TimeSlot.time == time
            )
        ).first()

        if not slot:
            return False

        return slot.is_available

    @staticmethod
    def get_available_times_for_date(
        db: Session,
        tutor_id: str,
        date_key: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get all available time slots for a specific date."""
        slots = db.query(TimeSlot).filter(
            TimeSlot.tutor_id == tutor_id
        ).all()

        result = {
            "morning": [],
            "afternoon": [],
            "night": []
        }

        for slot in slots:
            if date_key in slot.available_dates and slot.is_available:
                result[slot.period].append({
                    "id": slot.slot_id,
                    "time": slot.time,
                    "key": slot.time,
                    "is_available": slot.is_available,
                    "is_selected": slot.is_selected
                })

        return result

    @staticmethod
    def deactivate_availability(
        db: Session,
        tutor_id: str,
        month: str
    ) -> bool:
        """Deactivate tutor availability for a month."""
        availability = db.query(TutorAvailability).filter(
            and_(
                TutorAvailability.tutor_id == tutor_id,
                TutorAvailability.month == month
            )
        ).first()

        if not availability:
            return False

        availability.is_active = False
        availability.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def clear_selections(
        db: Session,
        tutor_id: str,
        month: str
    ) -> bool:
        """Clear all selections for a tutor's availability."""
        availability = db.query(TutorAvailability).filter(
            and_(
                TutorAvailability.tutor_id == tutor_id,
                TutorAvailability.month == month
            )
        ).first()

        if not availability:
            return False

        availability.selected_date_key = None
        availability.selected_slots = {
            "morning": {"key": ""},
            "afternoon": {"key": ""},
            "night": {"key": ""}
        }
        availability.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def sync_availability_to_calendar(
        db: Session,
        tutor_id: str,
        availability: TutorAvailability,
        tutor_name: str,
        color: str = "0xFF7ED957"
    ) -> bool:
        """Sync tutor availability to calendar as quick view events."""
        try:
            # Clear existing calendar events for this tutor
            db.query(CalendarEvent).filter(
                and_(
                    CalendarEvent.event_id == str(tutor_id),
                    CalendarEvent.event_date.ilike(f"{availability.month.split()[1]}%")
                )
            ).delete()

            # Add calendar events for each available date
            for date_info in availability.available_dates:
                calendar_event = CalendarEvent(
                    id=uuid4(),
                    user_id=tutor_id,  # Store tutor as event creator
                    event_date=date_info.get("key"),
                    event_id=str(tutor_id),
                    title=tutor_name,
                    color=color
                )
                db.add(calendar_event)

            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def book_and_schedule(
        db: Session,
        tutor_id: str,
        user_id: str,
        date_key: str,
        time: str,
        period: str,
        title: str,
        student_name: str,
        tutor_name: str,
        duration_minutes: int = 50,
        color: str = "0xFF7ED957"
    ) -> Optional[Dict[str, Any]]:
        """Book a time slot and create corresponding calendar entry."""
        try:
            # Verify slot is available
            slot = db.query(TimeSlot).filter(
                and_(
                    TimeSlot.tutor_id == tutor_id,
                    TimeSlot.period == period,
                    TimeSlot.time == time
                )
            ).first()

            if not slot or not slot.is_available:
                return None

            # Calculate end time
            start_hour, start_min = map(int, time.split(':'))
            end_minutes = start_min + duration_minutes
            end_hour = start_hour + (end_minutes // 60)
            end_min = end_minutes % 60
            end_time = f"{end_hour:02d}:{end_min:02d}"

            # Create daily schedule entry
            daily_schedule = DailySchedule(
                id=uuid4(),
                user_id=user_id,
                schedule_date=date_key,
                class_id=str(tutor_id),
                start_time=time,
                end_time=end_time,
                title=title,
                students=[student_name],
                student_colors=[color],
                status="upcoming",
                can_reschedule=True
            )
            db.add(daily_schedule)

            # Mark slot as selected
            slot.is_selected = True
            slot.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(daily_schedule)

            return {
                "booking_id": str(daily_schedule.id),
                "date": date_key,
                "time": time,
                "end_time": end_time,
                "title": title,
                "student": student_name,
                "tutor": tutor_name,
                "status": "confirmed"
            }
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def get_schedule_with_calendar(
        db: Session,
        user_id: str,
        tutor_id: str,
        date_key: str
    ) -> Optional[Dict[str, Any]]:
        """Get schedule and calendar data for a user-tutor-date combination."""
        try:
            # Get daily schedule
            daily_schedule = db.query(DailySchedule).filter(
                and_(
                    DailySchedule.user_id == user_id,
                    DailySchedule.class_id == str(tutor_id),
                    DailySchedule.schedule_date == date_key
                )
            ).first()

            # Get calendar event
            calendar_event = db.query(CalendarEvent).filter(
                and_(
                    CalendarEvent.event_date == date_key,
                    CalendarEvent.event_id == str(tutor_id)
                )
            ).first()

            if not daily_schedule:
                return None

            return {
                "schedule": {
                    "id": str(daily_schedule.id),
                    "date": daily_schedule.schedule_date,
                    "time": {
                        "start": daily_schedule.start_time,
                        "end": daily_schedule.end_time
                    },
                    "title": daily_schedule.title,
                    "students": daily_schedule.students,
                    "status": daily_schedule.status,
                    "can_reschedule": daily_schedule.can_reschedule
                },
                "calendar": {
                    "id": str(calendar_event.id) if calendar_event else None,
                    "title": calendar_event.title if calendar_event else None,
                    "color": calendar_event.color if calendar_event else None,
                    "date": date_key
                } if calendar_event else None
            }
        except Exception as e:
            raise e

    @staticmethod
    def update_booking_status(
        db: Session,
        user_id: str,
        schedule_id: str,
        new_status: str,
        tutor_id: Optional[str] = None
    ) -> bool:
        """Update booking status and sync to calendar."""
        try:
            daily_schedule = db.query(DailySchedule).filter(
                and_(
                    DailySchedule.id == schedule_id,
                    DailySchedule.user_id == user_id
                )
            ).first()

            if not daily_schedule:
                return False

            daily_schedule.status = new_status
            daily_schedule.updated_at = datetime.utcnow()
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
