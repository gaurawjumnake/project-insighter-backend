"""
Health Check Schema

Pydantic models for database connectivity health check responses.
"""

from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class HealthCheckResponse(BaseModel):
    """
    Response schema for health check endpoint.
    
    Indicates the health status of the application and database connectivity.
    
    Attributes:
        status: Overall application status ("healthy" or "unhealthy")
        database: Database connectivity status ("connected" or "disconnected")
        timestamp: ISO 8601 timestamp when health check was performed
        message: Detailed message about health status or error reason
    """
    
    status: Literal["healthy", "unhealthy"] = Field(
        ...,
        description="Overall application health status",
        examples=["healthy", "unhealthy"]
    )
    
    database: Literal["connected", "disconnected"] = Field(
        ...,
        description="Database connectivity status",
        examples=["connected", "disconnected"]
    )
    
    timestamp: datetime = Field(
        ...,
        description="ISO 8601 timestamp when health check was performed",
        example="2026-05-07T14:30:00Z"
    )
    
    message: str = Field(
        ...,
        description="Detailed message about health status or error reason",
        examples=[
            "Database connectivity OK",
            "Failed to connect to database: connection timeout"
        ]
    )
    
    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "examples": [
                {
                    "status": "healthy",
                    "database": "connected",
                    "timestamp": "2026-05-07T14:30:00Z",
                    "message": "Database connectivity OK"
                },
                {
                    "status": "unhealthy",
                    "database": "disconnected",
                    "timestamp": "2026-05-07T14:30:05Z",
                    "message": "Failed to connect to database: connection timeout"
                }
            ]
        }
