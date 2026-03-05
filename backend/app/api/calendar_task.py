from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from backend.app.db.session import get_db
from backend.app.api.deps import get_current_user_id  # <--- IMPORT THIS
from backend.app.schemas.calendar_task import CalendarTaskCreate, CalendarTaskUpdate, CalendarTaskResponse
from backend.app.services.calendar_task_service import CalendarTaskService

router = APIRouter()

@router.post("/", response_model=CalendarTaskResponse)
def create_task(
    task_in: CalendarTaskCreate,
    # This automatically gets the ID from .env
    user_id: UUID = Depends(get_current_user_id), 
    db: Session = Depends(get_db)
):
    return CalendarTaskService.create(db=db, task_data=task_in, user_id=user_id)

@router.put("/{task_id}", response_model=CalendarTaskResponse)
def update_task(
    task_id: UUID, 
    task_in: CalendarTaskUpdate, 
    db: Session = Depends(get_db)
):
    updated = CalendarTaskService.update(db=db, task_id=task_id, task_data=task_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    if not CalendarTaskService.delete(db=db, task_id=task_id):
        raise HTTPException(status_code=404, detail="Task not found")