from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Any
from backend.app.models.calendar_event import CalendarEvents
from backend.app.models.calendar_task import CalendarTask
from backend.app.models.calendar_milestone import CalendarMilestone
from backend.app.models.calendar_reminder import CalendarReminder

class CalendarEventService:
    @staticmethod
    def get_user_events(db: Session, user_id: UUID) -> List[Any]:
        # 1. Get all event references
        events = db.query(CalendarEvents).filter(CalendarEvents.user_id == user_id).all()
        
        if not events:
            return []

        # 2. Separate IDs by type
        task_ids = [e.event_id for e in events if e.event_type == "TASK"]
        milestone_ids = [e.event_id for e in events if e.event_type == "MILESTONE"]
        reminder_ids = [e.event_id for e in events if e.event_type == "REMINDER"]

        # 3. Batch Fetch details
        tasks = db.query(CalendarTask).filter(CalendarTask.id.in_(task_ids)).all()
        milestones = db.query(CalendarMilestone).filter(CalendarMilestone.id.in_(milestone_ids)).all()
        reminders = db.query(CalendarReminder).filter(CalendarReminder.id.in_(reminder_ids)).all()

        # 4. Create Lookups
        tasks_map = {t.id: t for t in tasks}
        mil_map = {m.id: m for m in milestones}
        rem_map = {r.id: r for r in reminders}

        # 5. Attach details to response
        results = []
        for e in events:
            # Create a simple dict representation or use the object if schema handles it
            event_obj = e
            
            # Manually inject the details based on type
            if e.event_type == "TASK":
                # Convert SQLAlchemy model to dict for schema 'details' field
                event_obj.details = tasks_map.get(e.event_id).__dict__ if tasks_map.get(e.event_id) else None
            elif e.event_type == "MILESTONE":
                event_obj.details = mil_map.get(e.event_id).__dict__ if mil_map.get(e.event_id) else None
            elif e.event_type == "REMINDER":
                event_obj.details = rem_map.get(e.event_id).__dict__ if rem_map.get(e.event_id) else None
            
            results.append(event_obj)

        return results