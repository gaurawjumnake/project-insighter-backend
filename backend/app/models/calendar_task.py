import uuid
import enum
from sqlalchemy import Column, String, Float, DateTime, Enum, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.db.base import Base
from datetime import datetime
from zoneinfo import ZoneInfo

class TaskPriorityEnum(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class TaskStatusEnum(str, enum.Enum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class CalendarTask(Base):
    __tablename__ = "calendar_task"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.now)

    account_id = Column(UUID(as_uuid=True), nullable=True)
    priority = Column(Enum(TaskPriorityEnum, name="task_priority_enum"), server_default="MEDIUM", nullable=True)
    status = Column(Enum(TaskStatusEnum, name="task_status_enum"), server_default="TO_DO", nullable=True)
    
    start_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    estimated_hours = Column(Float, server_default="0", default=0.0)
    task_title = Column(String, nullable=True)
    description = Column(String, nullable=True)

    