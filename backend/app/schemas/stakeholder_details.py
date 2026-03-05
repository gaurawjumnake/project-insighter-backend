from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class StakeholderDetailsBase(BaseModel):
    """Base schema for Stakeholder Details."""
    account_name: str
    executive_sponsor: Optional[str] = None
    technical_decision_maker: Optional[str] = None
    influencers: Optional[str] = None
    neutral_stakeholders: Optional[str] = None
    negative_stakeholder: Optional[str] = None
    succession_risk: Optional[str] = None
    key_competitors: Optional[str] = None
    our_positioning_vs_competition: Optional[str] = None
    incumbency_strength: Optional[str] = None  # High/Medium/Low
    areas_competition_stronger: Optional[str] = None
    white_spaces_we_own: Optional[str] = None
    account_review_cadence_frequency: Optional[str] = None
    qbr_happening: Optional[bool] = False
    technical_audit_frequency: Optional[str] = None

class StakeholderDetailsCreate(StakeholderDetailsBase):
    """Schema for creating Stakeholder Details."""
    account_id: UUID

class StakeholderDetailsUpdate(BaseModel):
    """Schema for updating Stakeholder Details - all fields optional."""
    account_name: Optional[str] = None
    executive_sponsor: Optional[str] = None
    technical_decision_maker: Optional[str] = None
    influencers: Optional[str] = None
    neutral_stakeholders: Optional[str] = None
    negative_stakeholder: Optional[str] = None
    succession_risk: Optional[str] = None
    key_competitors: Optional[str] = None
    our_positioning_vs_competition: Optional[str] = None
    incumbency_strength: Optional[str] = None
    areas_competition_stronger: Optional[str] = None
    white_spaces_we_own: Optional[str] = None
    account_review_cadence_frequency: Optional[str] = None
    qbr_happening: Optional[bool] = None
    technical_audit_frequency: Optional[str] = None

class StakeholderDetailsResponse(StakeholderDetailsBase):
    """Schema for Stakeholder Details response."""
    id: UUID
    account_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)