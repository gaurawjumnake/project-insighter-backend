from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from backend.app.db.session import get_db
from backend.app.api.deps import get_current_user_id # <--- IMPORT THIS
from backend.app.schemas.calendar_milestone import CalendarMilestoneCreate, CalendarMilestoneUpdate, CalendarMilestoneResponse
from backend.app.services.calendar_milestone_service import CalendarMilestoneService

router = APIRouter()

@router.post("/", response_model=CalendarMilestoneResponse)
def create_milestone(
    item_in: CalendarMilestoneCreate, 
    user_id: UUID = Depends(get_current_user_id), # Auto-injected
    db: Session = Depends(get_db)
):
    return CalendarMilestoneService.create(db=db, milestone_data=item_in, user_id=user_id)

@router.put("/{milestone_id}", response_model=CalendarMilestoneResponse)
def update_milestone(milestone_id: UUID, item_in: CalendarMilestoneUpdate, db: Session = Depends(get_db)):
    updated = CalendarMilestoneService.update(db=db, milestone_id=milestone_id, data=item_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return updated

@router.delete("/{milestone_id}", status_code=204)
def delete_milestone(milestone_id: UUID, db: Session = Depends(get_db)):
    if not CalendarMilestoneService.delete(db=db, milestone_id=milestone_id):
        raise HTTPException(status_code=404, detail="Milestone not found")