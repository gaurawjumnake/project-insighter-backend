from sqlalchemy import Column, String, Text, Numeric, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.app.db.base import Base
from datetime import datetime
import pytz # Import pytz 

# 1. Create a helper function to get IST time
def get_ist_time():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

class AccountDashboard(Base):
    """Account Dashboard model for storing account information."""
    
    __tablename__ = "account_dashboard"
    
    # Primary Key
    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # ... (Keep all your other columns exactly the same) ...
    account_name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=True)
    company_revenue = Column(Numeric(15, 2), nullable=True)
    know_customer_value_chain = Column(Boolean, default=False, nullable=True)
    account_focus = Column(String(50), nullable=True)
    delivery_unit = Column(String(255), nullable=True)
    delivery_owner = Column(String(255), nullable=True)
    client_partner = Column(String(255), nullable=True)
    where_we_fit_in_value_chain = Column(Text, nullable=True)
    engagement_age = Column(Integer, nullable=True)
    last_year_business_done = Column(Numeric(15, 2), nullable=True)
    target_projection_2026_accounts = Column(Numeric(15, 2), nullable=True)
    target_projection_2026_delivery = Column(Numeric(15, 2), nullable=True)
    current_pipeline_value = Column(Numeric(15, 2), nullable=True)
    revenue_attrition_possibility = Column(Text, nullable=True)
    current_engagement_areas = Column(Text, nullable=True)
    team_size = Column(Integer, nullable=True)
    engagement_models = Column(Text, nullable=True)
    current_rate_card_health = Column(String(50), nullable=True)
    number_of_active_projects = Column(Integer, nullable=True)
    overall_delivery_health = Column(String(50), nullable=True)
    current_nps = Column(Numeric(5, 2), nullable=True)
    champion_customer_side = Column(String(255), nullable=True)
    champion_profile = Column(Text, nullable=True)
    connect_with_decision_maker = Column(Boolean, default=False, nullable=True)
    total_active_connects = Column(Integer, nullable=True)
    visibility_client_roadmap_2026 = Column(Text, nullable=True)
    identified_areas_cross_up_selling = Column(Text, nullable=True)
    nitor_executive_connect_frequency = Column(String(100), nullable=True)
    growth_action_plan_30days_ready = Column(Boolean, default=False, nullable=True)
    miro_board_link = Column(String(500), nullable=True)
    
    # 2. Update Timestamps to use timezone=True and the IST function
    created_at = Column(DateTime(timezone=True), default=get_ist_time, nullable=False)
    
    updated_at = Column(
        DateTime(timezone=True), 
        default=get_ist_time, 
        onupdate=get_ist_time, 
        nullable=False
    )