from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from backend.app.models.calendar_task import CalendarTask
from backend.app.models.calendar_event import CalendarEvents
from backend.app.schemas.calendar_task import CalendarTaskCreate, CalendarTaskUpdate
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

class CalendarTaskService:
    @staticmethod
    def create(db: Session, task_data: CalendarTaskCreate, user_id: UUID) -> CalendarTask:
        try:
            # 1. Create the Task
            db_task = CalendarTask(**task_data.model_dump())
            db.add(db_task)
            
            # 2. FLUSH to generate the db_task.id without committing
            db.flush() 

            # 3. Create the Event using the Task ID
            event = CalendarEvents(
                user_id=user_id,
                event_type="TASK",      # Hardcode type
                event_id=db_task.id     # <--- Link to the Task
            )
            db.add(event)

            # 4. Commit both
            db.commit()
            db.refresh(db_task)
            return db_task
        except Exception as e:
            db.rollback()
            log.log_error(f"Task Service: Create failed | {e}")
            raise

    @staticmethod
    def update(db: Session, task_id: UUID, task_data: CalendarTaskUpdate) -> Optional[CalendarTask]:
        db_task = db.query(CalendarTask).filter(CalendarTask.id == task_id).first()
        if not db_task:
            return None
        
        try:
            for k, v in task_data.model_dump(exclude_unset=True).items():
                setattr(db_task, k, v)
            db.commit()
            db.refresh(db_task)
            return db_task
        except Exception as e:
            db.rollback()
            log.log_error(f"Task Service: Update failed | {e}")
            raise

    @staticmethod
    def delete(db: Session, task_id: UUID) -> bool:
        try:
            # 1. Delete the associated Event
            db.query(CalendarEvents).filter(
                CalendarEvents.event_id == task_id,
                CalendarEvents.event_type == "TASK"
            ).delete()
            
            # 2. Delete the Task
            res = db.query(CalendarTask).filter(CalendarTask.id == task_id).delete()
            
            db.commit()
            return res > 0
        except Exception as e:
            db.rollback()
            # log.log_error(f"Task Service: Delete failed | {e}")
            raise