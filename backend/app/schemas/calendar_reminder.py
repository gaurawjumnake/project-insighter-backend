from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime, date, time

class CalendarReminderBase(BaseModel):
    project_id: Optional[UUID] = None
    reminder_date: Optional[date] = None
    reminder_time: Optional[time] = None
    reminder_title: Optional[str] = None
    notes: Optional[str] = None

class CalendarReminderCreate(CalendarReminderBase):
    pass

class CalendarReminderUpdate(CalendarReminderBase):
    pass

class CalendarReminderResponse(CalendarReminderBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)