from sqlalchemy import Column, String, Text, Numeric, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.app.db.base import Base
from datetime import datetime


class AccountDashboard(Base):
    """Account Dashboard model for storing account information."""
    
    __tablename__ = "account_dashboard"
    
    # Primary Key
    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic Information
    account_name = Column(String(255), nullable=False)
    account_leader = Column(String(255), nullable=True)

    domain = Column(String(255), nullable=True)
    company_revenue = Column(Numeric(15, 2), nullable=True)
    know_customer_value_chain = Column(Boolean, default=False, nullable=True)
    account_focus = Column(String(50), nullable=True)  # Platinum/Gold/Silver
    delivery_unit = Column(String(255), nullable=True)
    delivery_owner = Column(String(255), nullable=True)
    client_partner = Column(String(255), nullable=True)
    where_we_fit_in_value_chain = Column(Text, nullable=True)
    
    # Engagement Metrics
    engagement_age = Column(Integer, nullable=True)  # In months as of Jan 2026
    last_year_business_done = Column(Numeric(15, 2), nullable=True)  # USD Jan 25-Dec 25
    
    # New Financials
    target_2026 = Column(Numeric(15, 2), nullable=True)
    current_revenue = Column(Numeric(15, 2), nullable=True)
    forecast_revenue = Column(Numeric(15, 2), nullable=True)
    shortfall = Column(Numeric(15, 2), nullable=True)
    account_health_score = Column(Numeric(5, 2), nullable=True)

    target_projection_2026_accounts = Column(Numeric(15, 2), nullable=True)
    target_projection_2026_delivery = Column(Numeric(15, 2), nullable=True)
    current_pipeline_value = Column(Numeric(15, 2), nullable=True)  # Next 6-12 months
    revenue_attrition_possibility = Column(Text, nullable=True)
    current_engagement_areas = Column(Text, nullable=True)
    team_size = Column(Integer, nullable=True)
    engagement_models = Column(Text, nullable=True)
    current_rate_card_health = Column(String(50), nullable=True)  # Above/At/Below
    number_of_active_projects = Column(Integer, nullable=True)
    overall_delivery_health = Column(String(50), nullable=True)
    current_nps = Column(Numeric(5, 2), nullable=True)
    
    # Champion Information
    champion_customer_side = Column(String(255), nullable=True)
    champion_profile = Column(Text, nullable=True)
    connect_with_decision_maker = Column(Boolean, default=False, nullable=True)
    total_active_connects = Column(Integer, nullable=True)
    
    # Strategic Planning
    visibility_client_roadmap_2026 = Column(Text, nullable=True)
    identified_areas_cross_up_selling = Column(Text, nullable=True)
    nitor_executive_connect_frequency = Column(String(100), nullable=True)  # CEO/VP
    growth_action_plan_30days_ready = Column(Boolean, default=False, nullable=True)
    miro_board_link = Column(String(500), nullable=True)
    
    # Timestamps
    # created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
