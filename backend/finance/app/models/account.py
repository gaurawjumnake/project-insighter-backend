# import uuid
# from sqlalchemy import Column, String, ForeignKey, text
# from sqlalchemy.orm import relationship
# from app.db.session import Base

# class Account(Base):
#     __tablename__ = "accounts"

#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = Column(String, nullable=False)
#     account_manager = Column(String)
#     customer_overview = Column(String)
#     ai_recommendations = Column(String)
#     delivery_unit_id = Column(String, ForeignKey("delivery_units.id"), nullable=False)
    
#     delivery_unit = relationship("DeliveryUnit")
#     projects = relationship("Project", back_populates="account")


from sqlalchemy import Column, String, DateTime, ForeignKey, text, Boolean, Integer, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from backend.db.base import Base
from datetime import datetime 
from backend.finance.app.models.private_equity import PrivateEquity

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=text("gen_random_uuid()"))
    name = Column(String, index=True, nullable=False)
    industry = Column(String, nullable=True, index=True)
    customer_overview = Column(String, nullable=True)
    delivery_unit_id = Column(UUID(as_uuid=True), ForeignKey("delivery_units.id"), nullable=False)
    private_equity_id = Column(UUID(as_uuid=True), ForeignKey("private_equity.id"), nullable=True)

    delivery_unit = relationship("DeliveryUnit", back_populates="accounts")
    private_equity = relationship("PrivateEquity", back_populates="accounts")
    
    ai_recommendations = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    account_manager = Column(String, nullable=True)
    target_revenue = Column(Float, nullable=True, default=0.0)
    forecast_revenue = Column(Float, nullable=True, default=0.0)
    shortfall = Column(Float, nullable=True, default=0.0)
    account_insights = Column(JSONB, nullable=True)
    account_insights_generated_at = Column(DateTime, nullable=True)
    is_sales = Column(Boolean, default=False, nullable=False, index=True)
    is_client = Column(Boolean, default=False, nullable=False, index=True)

    projects = relationship("Project", back_populates="account")

class AccountMetricsMV(Base):
    __tablename__ = 'account_metrics_mv'
    
    account_id = Column(UUID(as_uuid=True), primary_key=True)
    account_name = Column(String)
    delivery_unit_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime)
    project_count = Column(Integer)
    active_project_count = Column(Integer)
    inactive_project_count = Column(Integer)
    total_ai_hours = Column(Float)
    current_revenue = Column(Float)
    ai_revenue = Column(Float)
    ai_penetration_pct = Column(Float)
    has_revenue = Column(Integer)
