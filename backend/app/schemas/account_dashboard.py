from pydantic import BaseModel, ConfigDict, field_serializer
from typing import Optional
from uuid import UUID
from datetime import datetime
from zoneinfo import ZoneInfo


IST = ZoneInfo("Asia/Kolkata")

class AccountDashboardBase(BaseModel):
    """Base schema for Account Dashboard."""
    account_name: str
    domain: Optional[str] = None
    company_revenue: Optional[float] = None
    know_customer_value_chain: Optional[bool] = False
    account_focus: Optional[str] = None
    delivery_unit: Optional[str] = None
    delivery_owner: Optional[str] = None
    client_partner: Optional[str] = None
    where_we_fit_in_value_chain: Optional[str] = None
    engagement_age: Optional[int] = None
    last_year_business_done: Optional[float] = None
    target_projection_2026_accounts: Optional[float] = None
    target_projection_2026_delivery: Optional[float] = None
    current_pipeline_value: Optional[float] = None
    revenue_attrition_possibility: Optional[str] = None
    current_engagement_areas: Optional[str] = None
    team_size: Optional[int] = None
    engagement_models: Optional[str] = None
    current_rate_card_health: Optional[str] = None
    number_of_active_projects: Optional[int] = None
    overall_delivery_health: Optional[str] = None
    current_nps: Optional[float] = None
    champion_customer_side: Optional[str] = None
    champion_profile: Optional[str] = None
    connect_with_decision_maker: Optional[bool] = False
    total_active_connects: Optional[int] = None
    visibility_client_roadmap_2026: Optional[str] = None
    identified_areas_cross_up_selling: Optional[str] = None
    nitor_executive_connect_frequency: Optional[str] = None
    growth_action_plan_30days_ready: Optional[bool] = False
    miro_board_link: Optional[str] = None

class AccountDashboardCreate(AccountDashboardBase):
    pass

class AccountDashboardUpdate(BaseModel):
    """All fields optional for partial updates."""
    account_name: Optional[str] = None
    domain: Optional[str] = None
    company_revenue: Optional[float] = None
    know_customer_value_chain: Optional[bool] = None
    account_focus: Optional[str] = None
    delivery_unit: Optional[str] = None
    delivery_owner: Optional[str] = None
    client_partner: Optional[str] = None
    where_we_fit_in_value_chain: Optional[str] = None
    engagement_age: Optional[int] = None
    last_year_business_done: Optional[float] = None
    target_projection_2026_accounts: Optional[float] = None
    target_projection_2026_delivery: Optional[float] = None
    current_pipeline_value: Optional[float] = None
    revenue_attrition_possibility: Optional[str] = None
    current_engagement_areas: Optional[str] = None
    team_size: Optional[int] = None
    engagement_models: Optional[str] = None
    current_rate_card_health: Optional[str] = None
    number_of_active_projects: Optional[int] = None
    overall_delivery_health: Optional[str] = None
    current_nps: Optional[float] = None
    champion_customer_side: Optional[str] = None
    champion_profile: Optional[str] = None
    connect_with_decision_maker: Optional[bool] = None
    total_active_connects: Optional[int] = None
    visibility_client_roadmap_2026: Optional[str] = None
    identified_areas_cross_up_selling: Optional[str] = None
    nitor_executive_connect_frequency: Optional[str] = None
    growth_action_plan_30days_ready: Optional[bool] = None
    miro_board_link: Optional[str] = None

class AccountDashboardResponse(AccountDashboardBase):
    account_id: UUID
    created_at: datetime
    updated_at: datetime
    
    @field_serializer("created_at", "updated_at")
    def convert_to_ist(self, value: datetime):
        return value.astimezone(IST)
    
    model_config = ConfigDict(from_attributes=True)