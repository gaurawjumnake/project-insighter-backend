from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from backend.app.models.calendar_reminder import CalendarReminder
from backend.app.models.calendar_event import CalendarEvents
from backend.app.schemas.calendar_reminder import CalendarReminderCreate, CalendarReminderUpdate
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

class CalendarReminderService:
    @staticmethod
    def create(db: Session, reminder_data: CalendarReminderCreate, user_id: UUID) -> CalendarReminder:
        try:
            # 1. Create Reminder
            db_reminder = CalendarReminder(**reminder_data.model_dump())
            db.add(db_reminder)
            db.flush() # Get ID

            # 2. Create Event using Reminder ID
            event = CalendarEvents(
                user_id=user_id,
                event_type="REMINDER",
                event_id=db_reminder.id # <--- Link to Reminder
            )
            db.add(event)

            db.commit()
            db.refresh(db_reminder)
            return db_reminder
        except Exception as e:
            db.rollback()
            raise

    @staticmethod
    def update(db: Session, reminder_id: UUID, data: CalendarReminderUpdate) -> Optional[CalendarReminder]:
        db_obj = db.query(CalendarReminder).filter(CalendarReminder.id == reminder_id).first()
        if not db_obj: return None
        
        try:
            for k, v in data.model_dump(exclude_unset=True).items():
                setattr(db_obj, k, v)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, reminder_id: UUID) -> bool:
        try:
            # 1. Delete the associated Event first
            # We look for event_id (generic) and ensure type is REMINDER
            db.query(CalendarEvents).filter(
                CalendarEvents.event_id == reminder_id,
                CalendarEvents.event_type == "REMINDER"
            ).delete()
            
            # 2. Delete the Reminder
            res = db.query(CalendarReminder).filter(CalendarReminder.id == reminder_id).delete()
            
            db.commit()
            return res > 0
        except Exception as e:
            db.rollback()
            # log.log_error(f"Reminder Service: Delete failed | {e}")
            raise