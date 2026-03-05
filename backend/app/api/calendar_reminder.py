from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from backend.app.db.session import get_db
from backend.app.api.deps import get_current_user_id # <--- IMPORT THIS
from backend.app.schemas.calendar_reminder import CalendarReminderCreate, CalendarReminderUpdate, CalendarReminderResponse
from backend.app.services.calendar_reminder_service import CalendarReminderService

router = APIRouter()

@router.post("/", response_model=CalendarReminderResponse)
def create_reminder(
    item_in: CalendarReminderCreate, 
    user_id: UUID = Depends(get_current_user_id), # Auto-injected
    db: Session = Depends(get_db)
):
    return CalendarReminderService.create(db=db, reminder_data=item_in, user_id=user_id)

@router.put("/{reminder_id}", response_model=CalendarReminderResponse)
def update_reminder(reminder_id: UUID, item_in: CalendarReminderUpdate, db: Session = Depends(get_db)):
    updated = CalendarReminderService.update(db=db, reminder_id=reminder_id, data=item_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return updated

@router.delete("/{reminder_id}", status_code=204)
def delete_reminder(reminder_id: UUID, db: Session = Depends(get_db)):
    if not CalendarReminderService.delete(db=db, reminder_id=reminder_id):
        raise HTTPException(status_code=404, detail="Reminder not found")