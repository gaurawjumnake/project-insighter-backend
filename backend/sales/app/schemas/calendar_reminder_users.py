from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class CalendarReminderUserBase(BaseModel):
    # Mapping Pydantic input 'remainder_id' to logic
    reminder_id: Optional[UUID] = Field(default=None, alias="remainder_id")
    user_id: Optional[UUID] = None

class CalendarReminderUserCreate(CalendarReminderUserBase):
    pass

class CalendarReminderUserUpdate(CalendarReminderUserBase):
    pass

class CalendarReminderUserResponse(CalendarReminderUserBase):
    id: UUID
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)