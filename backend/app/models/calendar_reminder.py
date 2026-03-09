import uuid
from sqlalchemy import Column, String, Date, Time, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.db.base import Base
from datetime import datetime

class CalendarReminder(Base):
    __tablename__ = "calendar_reminder"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.now)

    account_id = Column(UUID(as_uuid=True), nullable=True)
    project_id = Column(UUID(as_uuid=True), nullable=True)
    reminder_date = Column(Date, nullable=True)
    reminder_time = Column(Time, nullable=True)
    reminder_title = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    # Relationship to Events and Reminder Users
    reminder_users = relationship("CalendarReminderUsers", back_populates="reminder")