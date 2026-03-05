from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime

class CalendarEventBase(BaseModel):
    user_id: Optional[UUID] = Field(default=None, alias="user-id")
    event_type: Optional[str] = None
    event_id: Optional[UUID] = None

class CalendarEventCreate(CalendarEventBase):
    pass

class CalendarEventUpdate(CalendarEventBase):
    pass

class CalendarEventResponse(CalendarEventBase):
    id: UUID
    created_at: Optional[datetime] = None
    
    # This field will hold the actual Task/Milestone/Reminder object
    details: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)