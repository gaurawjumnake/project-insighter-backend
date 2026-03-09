import uuid
import enum
from sqlalchemy import Column, String, Integer, DateTime, Enum, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.db.base import Base
from datetime import datetime

class MilestoneImpactEnum(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class CalendarMilestone(Base):
    __tablename__ = "calendar_milestone"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.now)

    account_id = Column(UUID(as_uuid=True), nullable=True)
    project_id = Column(UUID(as_uuid=True), nullable=True)
    target_date = Column(DateTime(timezone=True), nullable=True)
    owner_id = Column(UUID(as_uuid=True), nullable=True)
    
    impact_level = Column(Enum(MilestoneImpactEnum, name="milestone_impact_enum"), server_default="MEDIUM", nullable=True)
    progress_percent = Column(Integer, server_default="0", default=0)
    
    milestone_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
