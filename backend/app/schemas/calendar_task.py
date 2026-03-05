from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from backend.app.models.calendar_task import TaskPriorityEnum, TaskStatusEnum

class CalendarTaskBase(BaseModel):
    account_id: Optional[UUID] = None
    priority: Optional[TaskPriorityEnum] = TaskPriorityEnum.MEDIUM
    status: Optional[TaskStatusEnum] = TaskStatusEnum.TO_DO
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = 0.0
    task_title: Optional[str] = None
    description: Optional[str] = None

class CalendarTaskCreate(CalendarTaskBase):
    pass

class CalendarTaskUpdate(CalendarTaskBase):
    pass

class CalendarTaskResponse(CalendarTaskBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)