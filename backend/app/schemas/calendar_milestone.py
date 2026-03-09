from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from backend.app.models.calendar_milestone import MilestoneImpactEnum

class CalendarMilestoneBase(BaseModel):
    account_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    target_date: Optional[datetime] = None
    owner_id: Optional[UUID] = None
    impact_level: Optional[MilestoneImpactEnum] = MilestoneImpactEnum.MEDIUM
    progress_percent: Optional[int] = 0
    milestone_name: Optional[str] = None
    description: Optional[str] = None

class CalendarMilestoneCreate(CalendarMilestoneBase):
    pass

class CalendarMilestoneUpdate(CalendarMilestoneBase):
    pass

class CalendarMilestoneResponse(CalendarMilestoneBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)