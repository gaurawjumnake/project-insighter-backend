from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, Float, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.db.base import Base
from datetime import datetime
import pytz

# Helper function to get IST time
def get_ist_time():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

class AccountDashboard(Base):
    """Account Dashboard model for storing account information."""
    
    __tablename__ = "account_dashboard"
    
    # Primary Key
    account_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    
    # Basic Information
    account_name = Column(String, nullable=False)
    domain = Column(String, nullable=True)
    company_revenue = Column(Float, nullable=True)
    know_customer_value_chain = Column(Boolean, default=False, nullable=True)
    account_focus = Column(String, nullable=True)  # Platinum/Gold/Silver
    
    # Removed: delivery_unit
    
    delivery_owner = Column(String, nullable=True)
    client_partner = Column(String, nullable=True)
    where_we_fit_in_value_chain = Column(Text, nullable=True)
    
    # Engagement Metrics
    engagement_age = Column(Integer, nullable=True)
    last_year_business_done = Column(Float, nullable=True)
    target_projection_2026_accounts = Column(Float, nullable=True)
    target_projection_2026_delivery = Column(Float, nullable=True)
    current_pipeline_value = Column(Float, nullable=True)
    revenue_attrition_possibility = Column(Text, nullable=True)
    current_engagement_areas = Column(Text, nullable=True)
    team_size = Column(Integer, nullable=True)
    engagement_models = Column(Text, nullable=True)
    current_rate_card_health = Column(String, nullable=True)
    number_of_active_projects = Column(Integer, nullable=True)
    overall_delivery_health = Column(String, nullable=True)
    current_nps = Column(Float, nullable=True)
    
    # Champion Information
    champion_customer_side = Column(String, nullable=True)
    champion_profile = Column(Text, nullable=True)
    connect_with_decision_maker = Column(Boolean, default=False, nullable=True)
    total_active_connects = Column(Integer, nullable=True)
    
    # Strategic Planning
    visibility_client_roadmap_2026 = Column(Text, nullable=True)
    identified_areas_cross_up_selling = Column(Text, nullable=True)
    nitor_executive_connect_frequency = Column(String, nullable=True)
    growth_action_plan_30days_ready = Column(Boolean, default=False, nullable=True)
    account_research_link = Column(String, nullable=True) # Renamed from miro_board_link
    
    # Timestamps (IST)
    created_at = Column(DateTime(timezone=True), default=get_ist_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=get_ist_time, onupdate=get_ist_time, nullable=False)

    # Relationships
    stakeholder_details = relationship(
        "StakeholderDetails", 
        back_populates="account", 
        cascade="all, delete-orphan"
    )