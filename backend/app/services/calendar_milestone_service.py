from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from backend.app.models.calendar_milestone import CalendarMilestone
from backend.app.models.calendar_event import CalendarEvents
from backend.app.schemas.calendar_milestone import CalendarMilestoneCreate, CalendarMilestoneUpdate
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

class CalendarMilestoneService:
    @staticmethod
    def create(db: Session, milestone_data: CalendarMilestoneCreate, user_id: UUID) -> CalendarMilestone:
        try:
            # 1. Create Milestone
            db_milestone = CalendarMilestone(**milestone_data.model_dump())
            db.add(db_milestone)
            db.flush() # Get ID

            # 2. Create Event using Milestone ID
            event = CalendarEvents(
                user_id=user_id,
                event_type="MILESTONE",
                event_id=db_milestone.id # <--- Link to Milestone
            )
            db.add(event)

            db.commit()
            db.refresh(db_milestone)
            return db_milestone
        except Exception as e:
            db.rollback()
            raise

    @staticmethod
    def update(db: Session, milestone_id: UUID, data: CalendarMilestoneUpdate) -> Optional[CalendarMilestone]:
        db_obj = db.query(CalendarMilestone).filter(CalendarMilestone.id == milestone_id).first()
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
    def delete(db: Session, milestone_id: UUID) -> bool:
        try:
            # 1. Delete the associated Event
            db.query(CalendarEvents).filter(
                CalendarEvents.event_id == milestone_id,
                CalendarEvents.event_type == "MILESTONE"
            ).delete()
            
            # 2. Delete the Milestone
            res = db.query(CalendarMilestone).filter(CalendarMilestone.id == milestone_id).delete()
            
            db.commit()
            return res > 0
        except Exception as e:
            db.rollback()
            # log.log_error(f"Milestone Service: Delete failed | {e}")
            raise