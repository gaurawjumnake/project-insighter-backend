from sqlalchemy import Column, String, DateTime, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.db.base import Base 
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

class AccountDocument(Base):
    __tablename__ = "account_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=text("gen_random_uuid()"))
    
    # CHANGED: Foreign key now points to account_dashboard.account_id
    account_id = Column(UUID(as_uuid=True), ForeignKey("account_dashboard.account_id", ondelete="CASCADE"), nullable=False)
    
    content = Column(String, index=True, nullable=True)
    document_type = Column(String, index=True, nullable=True)
    created_at = Column(DateTime(timezone=False), default=lambda: datetime.now(IST).replace(tzinfo=None))
    
    # CHANGED: Relationship now links to AccountDashboard
    account = relationship("AccountDashboard", back_populates="documents")