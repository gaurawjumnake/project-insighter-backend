"""
Finance Insights API Routes

Provides REST endpoints for generating and retrieving finance insights at different hierarchy levels:
- POST /api/v1/insights/project/{project_id} - Generate project-level insights
- GET /api/v1/insights/project/{project_id} - Retrieve stored project insights
- POST /api/v1/insights/account/{account_id} - Generate account-level insights
- GET /api/v1/insights/account/{account_id} - Retrieve stored account insights
- POST /api/v1/insights/pe/{pe_id} - Generate PE-level insights
- GET /api/v1/insights/pe/{pe_id} - Retrieve stored PE insights
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from backend.db.session import get_db
from backend.insights_workflow.services.finance_insights_service import FinanceInsightsService
from backend.finance.app.models.project import Project
from backend.finance.app.models.account import Account
from backend.finance.app.models.private_equity import PrivateEquity
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

# ============================================================================
# PYDANTIC MODELS FOR RESPONSES
# ============================================================================

class InsightGenerationResponse(BaseModel):
    """Response model for insight generation requests."""
    status: str = Field(..., description="'success' or 'error'")
    entity_type: str = Field(..., description="'project', 'account', or 'private_equity'")
    entity_id: str = Field(..., description="UUID of the entity")
    entity_name: Optional[str] = Field(None, description="Name of the entity")
    s3_key: Optional[str] = Field(None, description="S3 key where JSON was staged")
    insights: Optional[Dict[str, Any]] = Field(None, description="Generated insights JSON")
    persisted_at: Optional[str] = Field(None, description="ISO datetime when persisted to DB")
    warnings: Optional[list] = Field(None, description="Data quality warnings")
    error: Optional[str] = Field(None, description="Error message if status is 'error'")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "entity_type": "project",
                "entity_id": "550e8400-e29b-41d4-a716-446655440000",
                "entity_name": "Project Alpha",
                "s3_key": "temp/project_550e8400-e29b-41d4-a716-446655440000_20240101_120000.json",
                "insights": {
                    "level": "project",
                    "entity_id": "550e8400-e29b-41d4-a716-446655440000",
                    "entity_name": "Project Alpha",
                    "generated_at": "2024-01-01T12:00:00",
                    "executive_summary": "...",
                    "kpis": {},
                    "risks": [],
                    "opportunities": [],
                    "recommended_actions": [],
                    "confidence_score": 0.85,
                    "evidence_summary": "..."
                },
                "persisted_at": "2024-01-01T12:00:00",
                "warnings": ["No project documents found"]
            }
        }


class InsightRetrievalResponse(BaseModel):
    """Response model for retrieving stored insights."""
    status: str = Field(..., description="'success' or 'error'")
    entity_type: str = Field(...)
    entity_id: str = Field(...)
    entity_name: Optional[str] = Field(None)
    insights: Optional[Dict[str, Any]] = Field(None, description="Stored insights from DB")
    insights_generated_at: Optional[str] = Field(None, description="When insights were generated")
    has_insights: bool = Field(..., description="Whether entity has stored insights")
    error: Optional[str] = Field(None)


# ============================================================================
# API ROUTER
# ============================================================================

router = APIRouter(
    prefix="/api/v1/insights",
    tags=["Insights"],
)


# =================================
# PROJECT INSIGHTS ENDPOINTS
# =================================

@router.post("/project/{project_id}", response_model=InsightGenerationResponse, status_code=status.HTTP_202_ACCEPTED)
def generate_project_insights(
    project_id: str,
    db: Session = Depends(get_db)
) -> InsightGenerationResponse:
    """
    Generate comprehensive project-level financial insights.
    
    This endpoint:
    1. Validates the project exists
    2. Fetches project data from DB
    3. Stages JSON to S3
    4. Runs CrewAI analysis
    5. Persists insights to projects.overall_insights
    
    **Status Codes:**
    - 202 Accepted: Insights generation initiated and completed
    - 400 Bad Request: Invalid project ID format
    - 404 Not Found: Project does not exist
    - 500 Internal Server Error: Unexpected error during generation
    """
    # Validate UUID format
    try:
        project_uuid = UUID(project_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid project ID format. Must be a valid UUID. Provided: {project_id}"
        )
    
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_uuid).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project not found: {project_id}"
        )
    
    log.log_info(f"Generating insights for project: {project_id} ({project.name})")
    
    try:
        # Call service to generate insights
        result = FinanceInsightsService.generate_project_insights(project_id)
        
        if result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate insights: {result.get('error')}"
            )
        
        return InsightGenerationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        log.log_error(f"Unexpected error generating project insights: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get("/project/{project_id}", response_model=InsightRetrievalResponse)
def retrieve_project_insights(
    project_id: str,
    db: Session = Depends(get_db)
) -> InsightRetrievalResponse:
    """
    Retrieve stored project insights from database.
    
    Returns the most recently generated insights for the project,
    or indicates if no insights have been generated yet.
    
    **Status Codes:**
    - 200 OK: Retrieved successfully (may have empty insights)
    - 400 Bad Request: Invalid project ID format
    - 404 Not Found: Project does not exist
    """
    # Validate UUID format
    try:
        project_uuid = UUID(project_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid project ID format. Must be a valid UUID. Provided: {project_id}"
        )
    
    # Fetch project
    project = db.query(Project).filter(Project.id == project_uuid).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project not found: {project_id}"
        )
    
    return InsightRetrievalResponse(
        status="success",
        entity_type="project",
        entity_id=project_id,
        entity_name=project.name,
        insights=project.overall_insights,
        insights_generated_at=project.overall_insights_generated_at.isoformat() if project.overall_insights_generated_at else None,
        has_insights=project.overall_insights is not None
    )


# =================================
# ACCOUNT INSIGHTS ENDPOINTS
# =================================

@router.post("/account/{account_id}", response_model=InsightGenerationResponse, status_code=status.HTTP_202_ACCEPTED)
def generate_account_insights(
    account_id: str,
    db: Session = Depends(get_db)
) -> InsightGenerationResponse:
    """
    Generate comprehensive account-level insights.
    
    This endpoint:
    1. Validates the account exists
    2. Fetches account data with all projects and their insights
    3. Stages aggregated JSON to S3
    4. Runs CrewAI analysis
    5. Persists insights to accounts.account_insights
    
    Account insights include:
    - Portfolio performance across all projects
    - Shortfall analysis (target - forecast)
    - Project-level insights aggregation
    - Strategic recommendations
    
    **Status Codes:**
    - 202 Accepted: Insights generation initiated and completed
    - 400 Bad Request: Invalid account ID format
    - 404 Not Found: Account does not exist
    - 500 Internal Server Error: Unexpected error during generation
    """
    # Validate UUID format
    try:
        account_uuid = UUID(account_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid account ID format. Must be a valid UUID. Provided: {account_id}"
        )
    
    # Verify account exists
    account = db.query(Account).filter(Account.id == account_uuid).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account not found: {account_id}"
        )
    
    log.log_info(f"Generating insights for account: {account_id} ({account.name})")
    
    try:
        # Call service to generate insights
        result = FinanceInsightsService.generate_account_insights(account_id)
        
        if result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate insights: {result.get('error')}"
            )
        
        return InsightGenerationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        log.log_error(f"Unexpected error generating account insights: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get("/account/{account_id}", response_model=InsightRetrievalResponse)
def retrieve_account_insights(
    account_id: str,
    db: Session = Depends(get_db)
) -> InsightRetrievalResponse:
    """
    Retrieve stored account insights from database.
    
    Returns the most recently generated insights for the account,
    or indicates if no insights have been generated yet.
    
    **Status Codes:**
    - 200 OK: Retrieved successfully (may have empty insights)
    - 400 Bad Request: Invalid account ID format
    - 404 Not Found: Account does not exist
    """
    # Validate UUID format
    try:
        account_uuid = UUID(account_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid account ID format. Must be a valid UUID. Provided: {account_id}"
        )
    
    # Fetch account
    account = db.query(Account).filter(Account.id == account_uuid).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account not found: {account_id}"
        )
    
    return InsightRetrievalResponse(
        status="success",
        entity_type="account",
        entity_id=account_id,
        entity_name=account.name,
        insights=account.account_insights,
        insights_generated_at=account.account_insights_generated_at.isoformat() if account.account_insights_generated_at else None,
        has_insights=account.account_insights is not None
    )


# =================================
# PRIVATE EQUITY INSIGHTS ENDPOINTS
# =================================

@router.post("/pe/{pe_id}", response_model=InsightGenerationResponse, status_code=status.HTTP_202_ACCEPTED)
def generate_pe_insights(
    pe_id: str,
    db: Session = Depends(get_db)
) -> InsightGenerationResponse:
    """
    Generate comprehensive PE-level portfolio insights.
    
    This endpoint:
    1. Validates the PE entity exists
    2. Fetches PE data with all accounts and their insights
    3. Stages aggregated JSON to S3
    4. Runs CrewAI analysis
    5. Persists insights to private_equity.pe_insights
    
    PE insights include:
    - Portfolio-wide performance
    - Account-level insights aggregation
    - Company capabilities alignment
    - Investment opportunity assessment
    
    **Status Codes:**
    - 202 Accepted: Insights generation initiated and completed
    - 400 Bad Request: Invalid PE ID format
    - 404 Not Found: PE entity does not exist
    - 500 Internal Server Error: Unexpected error during generation
    """
    # Validate UUID format
    try:
        pe_uuid = UUID(pe_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid PE ID format. Must be a valid UUID. Provided: {pe_id}"
        )
    
    # Verify PE exists
    pe = db.query(PrivateEquity).filter(PrivateEquity.id == pe_uuid).first()
    if not pe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Private Equity entity not found: {pe_id}"
        )
    
    log.log_info(f"Generating insights for PE: {pe_id} ({pe.name})")
    
    try:
        # Call service to generate insights
        result = FinanceInsightsService.generate_pe_insights(pe_id)
        
        if result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate insights: {result.get('error')}"
            )
        
        return InsightGenerationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        log.log_error(f"Unexpected error generating PE insights: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get("/pe/{pe_id}", response_model=InsightRetrievalResponse)
def retrieve_pe_insights(
    pe_id: str,
    db: Session = Depends(get_db)
) -> InsightRetrievalResponse:
    """
    Retrieve stored PE insights from database.
    
    Returns the most recently generated insights for the PE entity,
    or indicates if no insights have been generated yet.
    
    **Status Codes:**
    - 200 OK: Retrieved successfully (may have empty insights)
    - 400 Bad Request: Invalid PE ID format
    - 404 Not Found: PE entity does not exist
    """
    # Validate UUID format
    try:
        pe_uuid = UUID(pe_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid PE ID format. Must be a valid UUID. Provided: {pe_id}"
        )
    
    # Fetch PE
    pe = db.query(PrivateEquity).filter(PrivateEquity.id == pe_uuid).first()
    if not pe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Private Equity entity not found: {pe_id}"
        )
    
    return InsightRetrievalResponse(
        status="success",
        entity_type="private_equity",
        entity_id=pe_id,
        entity_name=pe.name,
        insights=pe.pe_insights,
        insights_generated_at=pe.pe_insights_generated_at.isoformat() if pe.pe_insights_generated_at else None,
        has_insights=pe.pe_insights is not None
    )
