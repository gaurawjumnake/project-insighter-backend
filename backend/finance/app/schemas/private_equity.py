from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List, Any
from datetime import datetime

class PrivateEquityBase(BaseModel):
    name: str = Field(..., description="The name of the Private Equity firm.")
    overview: Optional[str] = Field(None, description="Overview of the Private Equity firm.")
    ai_insights: Optional[Any] = Field(None, description="AI generated insights (overall stats).")
    generated_pitch: Optional[str] = Field(None, description="Generated product pitch.")

class PrivateEquityCreate(PrivateEquityBase):
    pass

class PrivateEquityUpdate(BaseModel):
    name: Optional[str] = None
    overview: Optional[str] = None
    ai_insights: Optional[Any] = None
    generated_pitch: Optional[str] = None

class PrivateEquityOut(PrivateEquityBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
