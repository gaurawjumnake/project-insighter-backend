from sqlalchemy import Column, String, Text, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from backend.app.db.base import Base
from datetime import datetime,timezone

class StakeholderDetails(Base):
    """Stakeholder Details model for storing stakeholder and competitive information."""
    
    __tablename__ = "stakeholder_details"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    
    # Account Information
    account_id = Column(UUID(as_uuid=True), nullable=False)
    account_name = Column(String, nullable=False)
    
    # Stakeholder Information
    executive_sponsor = Column(String, nullable=True)
    technical_decision_maker = Column(String, nullable=True)
    influencers = Column(Text, nullable=True)  # Multiple influencers
    neutral_stakeholders = Column(Text, nullable=True)
    negative_stakeholder = Column(Text, nullable=True)
    succession_risk = Column(Text, nullable=True)  # Champion leaving?
    
    # Competitive Analysis
    key_competitors = Column(Text, nullable=True)
    our_positioning_vs_competition = Column(Text, nullable=True)  # Cost/Quality/Speed/Trust/AI/Domain/Value
    incumbency_strength = Column(String, nullable=True)  # High/Medium/Low
    areas_competition_stronger = Column(Text, nullable=True)
    white_spaces_we_own = Column(Text, nullable=True)
    
    # Account Review Metrics
    account_review_cadence_frequency = Column(String, nullable=True)
    qbr_happening = Column(Boolean, default=False, nullable=True)
    technical_audit_frequency = Column(String, nullable=True)
    
    # Timestamps
    # created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )