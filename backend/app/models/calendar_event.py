import uuid
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from backend.app.db.base import Base
from datetime import datetime

class CalendarEvents(Base):
    __tablename__ = "calendar_events"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    
    # User ID is nullable as per your lead's request
    user_id = Column("user-id", UUID(as_uuid=True), nullable=True)
    
    # --- NEW POLYMORPHIC COLUMNS ---
    # event_type will hold strings: "TASK", "MILESTONE", "REMINDER"
    event_type = Column(String, nullable=True)
    
    # event_id will hold the UUID of the specific Task/Milestone/Reminder
    # Note: No ForeignKey constraint here because it points to different tables
    event_id = Column(UUID(as_uuid=True), nullable=True)