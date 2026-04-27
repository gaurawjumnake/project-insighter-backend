from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List, Any
from datetime import datetime

class PrivateEquityBase(BaseModel):
    name: str = Field(..., description="The name of the Private Equity firm.")
    overview: Optional[str] = Field(None, description="Overview of the Private Equity firm.")
    pe_insights: Optional[Any] = Field(None, description="AI generated insights.")
    pe_insights_generated_at: Optional[datetime] = None
    company_capabilities: Optional[str] = None
    generated_pitch: Optional[str] = Field(None, description="Generated product pitch.")

class PrivateEquityCreate(PrivateEquityBase):
    pass

class PrivateEquityUpdate(BaseModel):
    name: Optional[str] = None
    overview: Optional[str] = None
    pe_insights: Optional[Any] = None
    pe_insights_generated_at: Optional[datetime] = None
    company_capabilities: Optional[str] = None
    generated_pitch: Optional[str] = None

class PrivateEquityOut(PrivateEquityBase):
    id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
