from sqlalchemy import Column, String, DateTime, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.db.base import Base
from datetime import datetime, timezone, timedelta
import uuid

IST = timezone(timedelta(hours=5, minutes=30))


class PrivateEquityDocument(Base):
    """
    Stores documents uploaded for Private Equity entities.
    Documents include company capabilities and PE details.
    """
    __tablename__ = "private_equity_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=text("gen_random_uuid()"))
    pe_id = Column(UUID(as_uuid=True), ForeignKey("private_equity.id"), nullable=False)
    document_type = Column(String, nullable=False)  # 'company_capabilities' or 'pe_details'
    content = Column(String, nullable=True)  # Extracted text/insights from file
    file_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=False), default=lambda: datetime.now(IST).replace(tzinfo=None))

    private_equity = relationship("PrivateEquity", back_populates="documents")
