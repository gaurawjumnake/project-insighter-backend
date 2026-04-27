import uuid
from sqlalchemy import Column, String, Text, DateTime, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from backend.db.base import Base
from datetime import datetime

class PrivateEquity(Base):
    __tablename__ = "private_equity"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=text("gen_random_uuid()"))
    name = Column(String, index=True, nullable=False)
    overview = Column(Text, nullable=True)
    pe_insights = Column(JSONB, nullable=True)
    pe_insights_generated_at = Column(DateTime, nullable=True)
    company_capabilities = Column(Text, nullable=True)
    generated_pitch = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    accounts = relationship("Account", back_populates="private_equity")
    documents = relationship("PrivateEquityDocument", back_populates="private_equity", cascade="all, delete-orphan")
