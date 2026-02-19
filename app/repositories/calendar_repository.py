from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import uuid4
from typing import List, Dict, Any, Optional
from app.models.calendar import CalendarEvent, DailySchedule, CalendarMonth
from datetime import datetime


class CalendarRepository:
    """Repository for calendar operations."""

    @staticmethod
    def get_calendar_month(db: Session, user_id: str, month: str) -> Optional[Dict[str, Any]]:
        """
        Get calendar data for a specific month including events and daily schedule.
        
        Args:
            db: Database session
            user_id: User ID
            month: Month in format YYYY-MM
            
        Returns:
            Dict with month, today, calendar, and dailySchedule
        """
        # Get calendar month metadata
        calendar_month = db.query(CalendarMonth).filter(
            and_(
                CalendarMonth.user_id == user_id,
                CalendarMonth.month == month
            )
        ).first()
        
        if not calendar_month:
            return None

        # Get calendar events for this month
        calendar_events = db.query(CalendarEvent).filter(
            and_(
                CalendarEvent.user_id == user_id,
                CalendarEvent.event_date.ilike(f"{month}%")
            )
        ).all()

        # Get daily schedules for this month
        daily_schedules = db.query(DailySchedule).filter(
            and_(
                DailySchedule.user_id == user_id,
                DailySchedule.schedule_date.ilike(f"{month}%")
            )
        ).all()

        # Format calendar events by date
        calendar_dict = {}
        for event in calendar_events:
            date = event.event_date
            if date not in calendar_dict:
                calendar_dict[date] = []
            calendar_dict[date].append({
                "id": event.id,
                "title": event.title,
                "color": event.color
            })

        # Format daily schedules by date
        daily_schedule_dict = {}
        for schedule in daily_schedules:
            date = schedule.schedule_date
            if date not in daily_schedule_dict:
                daily_schedule_dict[date] = []
            daily_schedule_dict[date].append({
                "id": schedule.id,
                "time": {
                    "start": schedule.start_time,
                    "end": schedule.end_time
                },
                "title": schedule.title,
                "students": schedule.students,
                "colors": schedule.student_colors,
                "status": schedule.status,
                "canReschedule": schedule.can_reschedule
            })

        return {
            "month": calendar_month.month,
            "today": calendar_month.today,
            "calendar": calendar_dict,
            "dailySchedule": daily_schedule_dict
        }

    @staticmethod
    def create_calendar_month(db: Session, user_id: str, month: str, today: str) -> CalendarMonth:
        """Create or update calendar month metadata."""
        existing_month = db.query(CalendarMonth).filter(
            and_(
                CalendarMonth.user_id == user_id,
                CalendarMonth.month == month
            )
        ).first()

        if existing_month:
            existing_month.today = today
            existing_month.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing_month)
            return existing_month

        calendar_month = CalendarMonth(
            id=uuid4(),
            user_id=user_id,
            month=month,
            today=today
        )
        db.add(calendar_month)
        db.commit()
        db.refresh(calendar_month)
        return calendar_month

    @staticmethod
    def add_calendar_event(
        db: Session,
        user_id: str,
        event_date: str,
        event_id: str,
        title: str,
        color: str
    ) -> CalendarEvent:
        """Add a calendar event."""
        # Check if event already exists
        existing_event = db.query(CalendarEvent).filter(
            and_(
                CalendarEvent.user_id == user_id,
                CalendarEvent.event_date == event_date,
                CalendarEvent.event_id == event_id,
                CalendarEvent.title == title
            )
        ).first()

        if existing_event:
            return existing_event

        calendar_event = CalendarEvent(
            id=uuid4(),
            user_id=user_id,
            event_date=event_date,
            event_id=event_id,
            title=title,
            color=color
        )
        db.add(calendar_event)
        db.commit()
        db.refresh(calendar_event)
        return calendar_event

    @staticmethod
    def remove_calendar_event(db: Session, user_id: str, event_id: str) -> bool:
        """Remove a calendar event."""
        event = db.query(CalendarEvent).filter(
            and_(
                CalendarEvent.user_id == user_id,
                CalendarEvent.id == event_id
            )
        ).first()

        if not event:
            return False

        db.delete(event)
        db.commit()
        return True

    @staticmethod
    def update_calendar_event(
        db: Session,
        user_id: str,
        event_id: str,
        title: Optional[str] = None,
        color: Optional[str] = None
    ) -> bool:
        """Update a calendar event."""
        event = db.query(CalendarEvent).filter(
            and_(
                CalendarEvent.user_id == user_id,
                CalendarEvent.id == event_id
            )
        ).first()

        if not event:
            return False

        if title:
            event.title = title
        if color:
            event.color = color
        event.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def add_daily_schedule(
        db: Session,
        user_id: str,
        schedule_date: str,
        class_id: str,
        start_time: str,
        end_time: str,
        title: str,
        students: List[str],
        student_colors: List[str],
        status: str,
        can_reschedule: bool = False,
        notes: Optional[str] = None
    ) -> DailySchedule:
        """Add a daily schedule item."""
        daily_schedule = DailySchedule(
            id=uuid4(),
            user_id=user_id,
            schedule_date=schedule_date,
            class_id=class_id,
            start_time=start_time,
            end_time=end_time,
            title=title,
            students=students,
            student_colors=student_colors,
            status=status,
            can_reschedule=can_reschedule,
            notes=notes
        )
        db.add(daily_schedule)
        db.commit()
        db.refresh(daily_schedule)
        return daily_schedule

    @staticmethod
    def get_daily_schedule(db: Session, user_id: str, schedule_date: str) -> List[Dict[str, Any]]:
        """Get all schedules for a specific date."""
        schedules = db.query(DailySchedule).filter(
            and_(
                DailySchedule.user_id == user_id,
                DailySchedule.schedule_date == schedule_date
            )
        ).order_by(DailySchedule.start_time).all()

        result = []
        for schedule in schedules:
            result.append({
                "id": schedule.id,
                "time": {
                    "start": schedule.start_time,
                    "end": schedule.end_time
                },
                "title": schedule.title,
                "students": schedule.students,
                "colors": schedule.student_colors,
                "status": schedule.status,
                "canReschedule": schedule.can_reschedule
            })
        return result

    @staticmethod
    def update_daily_schedule(
        db: Session,
        user_id: str,
        schedule_id: str,
        status: Optional[str] = None,
        students: Optional[List[str]] = None,
        student_colors: Optional[List[str]] = None,
        notes: Optional[str] = None,
        can_reschedule: Optional[bool] = None
    ) -> bool:
        """Update a daily schedule item."""
        schedule = db.query(DailySchedule).filter(
            and_(
                DailySchedule.user_id == user_id,
                DailySchedule.id == schedule_id
            )
        ).first()

        if not schedule:
            return False

        if status:
            schedule.status = status
        if students is not None:
            schedule.students = students
        if student_colors is not None:
            schedule.student_colors = student_colors
        if notes:
            schedule.notes = notes
        if can_reschedule is not None:
            schedule.can_reschedule = can_reschedule
        schedule.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def reschedule_class(
        db: Session,
        user_id: str,
        schedule_id: str,
        new_date: str,
        new_start_time: str,
        new_end_time: str
    ) -> bool:
        """Reschedule a class to a new date/time."""
        schedule = db.query(DailySchedule).filter(
            and_(
                DailySchedule.user_id == user_id,
                DailySchedule.id == schedule_id
            )
        ).first()

        if not schedule or not schedule.can_reschedule:
            return False

        schedule.schedule_date = new_date
        schedule.start_time = new_start_time
        schedule.end_time = new_end_time
        schedule.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def remove_daily_schedule(db: Session, user_id: str, schedule_id: str) -> bool:
        """Remove a daily schedule item."""
        schedule = db.query(DailySchedule).filter(
            and_(
                DailySchedule.user_id == user_id,
                DailySchedule.id == schedule_id
            )
        ).first()

        if not schedule:
            return False

        db.delete(schedule)
        db.commit()
        return True

    @staticmethod
    def clear_month_events(db: Session, user_id: str, month: str) -> bool:
        """Clear all calendar events for a month."""
        db.query(CalendarEvent).filter(
            and_(
                CalendarEvent.user_id == user_id,
                CalendarEvent.event_date.ilike(f"{month}%")
            )
        ).delete()
        db.commit()
        return True

    @staticmethod
    def get_all_upcoming_schedules(db: Session, user_id: str) -> List[Dict[str, Any]]:
        """Get all upcoming schedules for a user."""
        schedules = db.query(DailySchedule).filter(
            and_(
                DailySchedule.user_id == user_id,
                DailySchedule.status.in_(["upcoming"])
            )
        ).order_by(DailySchedule.schedule_date, DailySchedule.start_time).all()

        result = []
        for schedule in schedules:
            result.append({
                "id": schedule.id,
                "date": schedule.schedule_date,
                "time": {
                    "start": schedule.start_time,
                    "end": schedule.end_time
                },
                "title": schedule.title,
                "students": schedule.students,
                "status": schedule.status
            })
        return result
