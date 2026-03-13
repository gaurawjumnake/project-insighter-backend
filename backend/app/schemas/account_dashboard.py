from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class AccountDashboardBase(BaseModel):
    """Base schema for Account Dashboard."""
    account_name: str
    domain: Optional[str] = None
    company_revenue: Optional[str] = None
    know_customer_value_chain: Optional[bool] = False
    account_focus: Optional[str] = None
    delivery_owner: Optional[str] = None
    client_partner: Optional[str] = None
    where_we_fit_in_value_chain: Optional[str] = None
    engagement_age: Optional[str] = None
    last_year_business_done: Optional[str] = None
    target_projection_2026_accounts: Optional[str] = None
    target_projection_2026_delivery: Optional[str] = None
    current_pipeline_value: Optional[str] = None
    revenue_attrition_possibility: Optional[str] = None
    current_engagement_areas: Optional[str] = None
    team_size: Optional[str] = None
    engagement_models: Optional[str] = None
    current_rate_card_health: Optional[str] = None
    number_of_active_projects: Optional[str] = None
    overall_delivery_health: Optional[str] = None
    current_nps: Optional[str] = None
    champion_customer_side: Optional[str] = None
    champion_profile: Optional[str] = None
    connect_with_decision_maker: Optional[bool] = False
    total_active_connects: Optional[str] = None
    visibility_client_roadmap_2026: Optional[str] = None
    identified_areas_cross_up_selling: Optional[str] = None
    nitor_executive_connect_frequency: Optional[str] = None
    growth_action_plan_30days_ready: Optional[bool] = False
    account_research_link: Optional[str] = None

class StakeholderMixin(BaseModel):
    """Fields from the Stakeholder tab that the frontend now sends together."""
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
    qbr_happening: Optional[bool] = False
    technical_audit_frequency: Optional[str] = None

# Combine both into the Create and Update schemas
class AccountDashboardCreate(AccountDashboardBase, StakeholderMixin):
    pass

class AccountDashboardUpdate(AccountDashboardBase, StakeholderMixin):
    account_name: Optional[str] = None
    know_customer_value_chain: Optional[bool] = None
    connect_with_decision_maker: Optional[bool] = None
    growth_action_plan_30days_ready: Optional[bool] = None
    qbr_happening: Optional[bool] = None

class AccountDashboardResponse(AccountDashboardBase):
    account_id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)