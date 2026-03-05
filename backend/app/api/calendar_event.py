from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from backend.app.db.session import get_db
from backend.app.api.deps import get_current_user_id # <--- IMPORT THIS
from backend.app.schemas.calendar_event import CalendarEventResponse
from backend.app.services.calendar_event_service import CalendarEventService

router = APIRouter()

@router.get("/", response_model=List[CalendarEventResponse])
def get_my_calendar(
    user_id: UUID = Depends(get_current_user_id), # Auto-injected
    db: Session = Depends(get_db)
):
    """
    Get all calendar events (Tasks, Milestones, Reminders) for the System User.
    """
    return CalendarEventService.get_user_events(db=db, user_id=user_id)