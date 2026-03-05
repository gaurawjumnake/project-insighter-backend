import uuid
from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.db.base import Base

class CalendarReminderUsers(Base):
    __tablename__ = "calendar_reminder_users"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    
    # Note: DB column is 'remainder_id' (typo in DB schema), but we map it cleanly here
    reminder_id = Column("remainder_id", UUID(as_uuid=True), ForeignKey("calendar_reminder.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)

    # Relationship back to Reminder
    reminder = relationship("CalendarReminder", back_populates="reminder_users")