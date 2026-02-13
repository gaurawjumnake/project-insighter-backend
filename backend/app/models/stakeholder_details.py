from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.db.base import Base
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid # <--- Import this

def get_ist_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

class StakeholderDetails(Base):
    __tablename__ = "stakeholder_details"
    
    # --- FIX IS HERE ---
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    account_id = Column(UUID(as_uuid=True), ForeignKey("account_dashboard.account_id"), nullable=False)
    account_name = Column(String, nullable=False)
    
    # ... rest of your columns ...
    executive_sponsor = Column(String, nullable=True)
    technical_decision_maker = Column(String, nullable=True)
    influencers = Column(Text, nullable=True)
    neutral_stakeholders = Column(Text, nullable=True)
    negative_stakeholder = Column(Text, nullable=True)
    succession_risk = Column(Text, nullable=True)
    key_competitors = Column(Text, nullable=True)
    our_positioning_vs_competition = Column(Text, nullable=True)
    incumbency_strength = Column(String, nullable=True)
    areas_competition_stronger = Column(Text, nullable=True)
    white_spaces_we_own = Column(Text, nullable=True)
    account_review_cadence_frequency = Column(String, nullable=True)
    qbr_happening = Column(Boolean, default=False, nullable=True)
    technical_audit_frequency = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=get_ist_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=get_ist_time, onupdate=get_ist_time, nullable=False)

    account = relationship("AccountDashboard", back_populates="stakeholder_details")