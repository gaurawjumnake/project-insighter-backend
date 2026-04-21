"""
API Endpoints for Generalized Analysis (Researcher, Analyzer, Summarizer)

This module provides REST endpoints for sales and finance analysis using
the generalized three-agent architecture.

Endpoints:
- POST /api/v1/analysis/sales/{account_id}
- POST /api/v1/analysis/finance/{project_id}
- POST /api/v1/analysis/batch/sales
- POST /api/v1/analysis/batch/finance
- GET /api/v1/analysis/status/{analysis_id}
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from uuid import UUID, uuid4
import json
from backend.doc_insighter.core.generalized_crew import (
    GeneralizedAnalysisCrew,
    create_sales_analysis_crew,
    create_finance_analysis_crew
)
from backend.doc_insighter.tools.app_logger import Logger
from datetime import datetime

log = Logger()

router = APIRouter()

# ============================================================================
# MODELS FOR REQUEST/RESPONSE
# ============================================================================

class SalesAnalysisRequest(BaseModel):
    """Request model for sales account analysis"""
    account_id: str = Field(..., description="UUID of the account to analyze")
    
    class Config:
        schema_extra = {
            "example": {
                "account_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class FinanceAnalysisRequest(BaseModel):
    """Request model for finance project analysis"""
    project_id: str = Field(..., description="UUID of the project to analyze")
    
    class Config:
        schema_extra = {
            "example": {
                "project_id": "660e8400-e29b-41d4-a716-446655440000"
            }
        }


class BatchAnalysisRequest(BaseModel):
    """Request model for batch analysis"""
    ids: List[str] = Field(..., description="List of UUIDs to analyze")
    
    class Config:
        schema_extra = {
            "example": {
                "ids": [
                    "550e8400-e29b-41d4-a716-446655440000",
                    "550e8400-e29b-41d4-a716-446655440001"
                ]
            }
        }


class AnalysisResponse(BaseModel):
    """Response model for successful analysis"""
    status: str = Field("success", description="Status of the analysis")
    analysis_type: str = Field(..., description="Type of analysis: 'sales' or 'finance'")
    entity_id: str = Field(..., description="UUID of the analyzed entity")
    timestamp: str = Field(..., description="ISO format timestamp of analysis")
    insights: Dict[str, Any] = Field(..., description="Analysis insights and findings")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "analysis_type": "sales",
                "entity_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2026-04-20T10:30:00",
                "insights": {
                    "key_findings": [],
                    "account_health": 78,
                    "growth_opportunities": []
                }
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors"""
    status: str = Field("error", description="Status indicating error")
    error_type: str = Field(..., description="Type of error")
    message: str = Field(..., description="Error message")
    entity_id: Optional[str] = Field(None, description="UUID of the entity (if applicable)")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "error_type": "entity_not_found",
                "message": "Account with ID 550e8400-e29b-41d4-a716-446655440000 not found",
                "entity_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class BatchAnalysisResponse(BaseModel):
    """Response model for batch analysis"""
    status: str = Field("success", description="Overall status")
    analysis_type: str = Field(..., description="Type of analysis performed")
    total: int = Field(..., description="Total number of entities analyzed")
    successful: int = Field(..., description="Number of successful analyses")
    failed: int = Field(..., description="Number of failed analyses")
    timestamp: str = Field(..., description="ISO format timestamp")
    results: Dict[str, Any] = Field(..., description="Results for each entity")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "analysis_type": "sales",
                "total": 2,
                "successful": 2,
                "failed": 0,
                "timestamp": "2026-04-20T10:30:00",
                "results": {
                    "550e8400-e29b-41d4-a716-446655440000": {
                        "status": "success",
                        "insights": {}
                    }
                }
            }
        }


# ============================================================================
# ANALYSIS STORAGE (In-memory for demo, can be replaced with database)
# ============================================================================

ANALYSIS_CACHE: Dict[str, Dict[str, Any]] = {}


def store_analysis(analysis_id: str, data: Dict[str, Any]) -> None:
    """Store analysis result in cache"""
    ANALYSIS_CACHE[analysis_id] = data


def get_analysis(analysis_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve analysis result from cache"""
    return ANALYSIS_CACHE.get(analysis_id)


# ============================================================================
# SALES ANALYSIS ENDPOINTS
# ============================================================================

@router.post(
    "/sales/{account_id}",
    response_model=AnalysisResponse,
    summary="Analyze Sales Account",
    description="Generate comprehensive sales insights for an account using the generalized analysis flow"
)
async def analyze_sales_account(
    account_id: str,
    background_tasks: BackgroundTasks
) -> AnalysisResponse:
    """
    Analyze a sales account.
    
    This endpoint uses the generalized three-agent workflow:
    1. Researcher: Fetches account_dashboard and account_documents
    2. Analyzer: Performs sales-focused analysis
    3. Summarizer: Creates sales-specific insights
    
    Args:
        account_id: UUID of the account to analyze
    
    Returns:
        AnalysisResponse containing insights formatted for sales context
    
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Validate UUID format
        try:
            UUID(account_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid UUID format: {account_id}"
            )
        
        log.log_info(f"Starting sales analysis for account: {account_id}")
        
        # Create and execute crew
        crew = create_sales_analysis_crew(account_id)
        insights = crew.analyze()
        
        response = AnalysisResponse(
            status="success",
            analysis_type="sales",
            entity_id=account_id,
            timestamp=datetime.utcnow().isoformat(),
            insights=insights if isinstance(insights, dict) else {"raw_analysis": str(insights)}
        )
        
        log.log_info(f"Sales analysis completed for account: {account_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        log.log_error(f"Error during sales analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


# ============================================================================
# FINANCE ANALYSIS ENDPOINTS
# ============================================================================

@router.post(
    "/finance/{project_id}",
    response_model=AnalysisResponse,
    summary="Analyze Finance Project",
    description="Generate comprehensive financial insights for a project using the generalized analysis flow"
)
async def analyze_finance_project(
    project_id: str,
    background_tasks: BackgroundTasks
) -> AnalysisResponse:
    """
    Analyze a finance project.
    
    This endpoint uses the generalized three-agent workflow:
    1. Researcher: Fetches projects, project_documents, and revenue_master tables
    2. Analyzer: Performs finance-focused analysis
    3. Summarizer: Creates finance-specific insights
    
    Args:
        project_id: UUID of the project to analyze
    
    Returns:
        AnalysisResponse containing insights formatted for finance context
    
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Validate UUID format
        try:
            UUID(project_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid UUID format: {project_id}"
            )
        
        log.log_info(f"Starting finance analysis for project: {project_id}")
        
        # Create and execute crew
        crew = create_finance_analysis_crew(project_id)
        insights = crew.analyze()
        
        response = AnalysisResponse(
            status="success",
            analysis_type="finance",
            entity_id=project_id,
            timestamp=datetime.utcnow().isoformat(),
            insights=insights if isinstance(insights, dict) else {"raw_analysis": str(insights)}
        )
        
        log.log_info(f"Finance analysis completed for project: {project_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        log.log_error(f"Error during finance analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


# ============================================================================
# BATCH ANALYSIS ENDPOINTS
# ============================================================================

@router.post(
    "/batch/sales",
    response_model=BatchAnalysisResponse,
    summary="Batch Analyze Sales Accounts",
    description="Analyze multiple sales accounts in parallel"
)
async def batch_analyze_sales(request: BatchAnalysisRequest) -> BatchAnalysisResponse:
    """
    Analyze multiple sales accounts.
    
    Args:
        request: BatchAnalysisRequest with list of account IDs
    
    Returns:
        BatchAnalysisResponse containing results for each account
    """
    try:
        log.log_info(f"Starting batch sales analysis for {len(request.ids)} accounts")
        
        results = {}
        successful = 0
        failed = 0
        
        for account_id in request.ids:
            try:
                # Validate UUID format
                try:
                    UUID(account_id)
                except ValueError:
                    results[account_id] = {
                        "status": "error",
                        "error": f"Invalid UUID format: {account_id}"
                    }
                    failed += 1
                    continue
                
                crew = create_sales_analysis_crew(account_id)
                insights = crew.analyze()
                
                results[account_id] = {
                    "status": "success",
                    "insights": insights if isinstance(insights, dict) else {"raw_analysis": str(insights)}
                }
                successful += 1
                
            except Exception as e:
                log.log_error(f"Error analyzing account {account_id}: {str(e)}")
                results[account_id] = {
                    "status": "error",
                    "error": str(e)
                }
                failed += 1
        
        response = BatchAnalysisResponse(
            status="success" if failed == 0 else "partial",
            analysis_type="sales",
            total=len(request.ids),
            successful=successful,
            failed=failed,
            timestamp=datetime.utcnow().isoformat(),
            results=results
        )
        
        log.log_info(f"Batch sales analysis completed: {successful} successful, {failed} failed")
        return response
        
    except Exception as e:
        log.log_error(f"Error during batch sales analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch analysis failed: {str(e)}"
        )


@router.post(
    "/batch/finance",
    response_model=BatchAnalysisResponse,
    summary="Batch Analyze Finance Projects",
    description="Analyze multiple finance projects in parallel"
)
async def batch_analyze_finance(request: BatchAnalysisRequest) -> BatchAnalysisResponse:
    """
    Analyze multiple finance projects.
    
    Args:
        request: BatchAnalysisRequest with list of project IDs
    
    Returns:
        BatchAnalysisResponse containing results for each project
    """
    try:
        log.log_info(f"Starting batch finance analysis for {len(request.ids)} projects")
        
        results = {}
        successful = 0
        failed = 0
        
        for project_id in request.ids:
            try:
                # Validate UUID format
                try:
                    UUID(project_id)
                except ValueError:
                    results[project_id] = {
                        "status": "error",
                        "error": f"Invalid UUID format: {project_id}"
                    }
                    failed += 1
                    continue
                
                crew = create_finance_analysis_crew(project_id)
                insights = crew.analyze()
                
                results[project_id] = {
                    "status": "success",
                    "insights": insights if isinstance(insights, dict) else {"raw_analysis": str(insights)}
                }
                successful += 1
                
            except Exception as e:
                log.log_error(f"Error analyzing project {project_id}: {str(e)}")
                results[project_id] = {
                    "status": "error",
                    "error": str(e)
                }
                failed += 1
        
        response = BatchAnalysisResponse(
            status="success" if failed == 0 else "partial",
            analysis_type="finance",
            total=len(request.ids),
            successful=successful,
            failed=failed,
            timestamp=datetime.utcnow().isoformat(),
            results=results
        )
        
        log.log_info(f"Batch finance analysis completed: {successful} successful, {failed} failed")
        return response
        
    except Exception as e:
        log.log_error(f"Error during batch finance analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch analysis failed: {str(e)}"
        )


# ============================================================================
# HEALTH ENDPOINTS
# ============================================================================

@router.get(
    "/health",
    summary="Health Check",
    description="Check if the analysis service is running"
)
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for the analysis service.
    
    Returns:
        Dictionary with service status
    """
    return {
        "status": "healthy",
        "service": "Generalized Analysis API",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# INFORMATION ENDPOINTS
# ============================================================================

@router.get(
    "/info",
    summary="Service Information",
    description="Get information about the analysis service"
)
async def service_info() -> Dict[str, Any]:
    """
    Get information about the analysis service.
    
    Returns:
        Dictionary with service information
    """
    return {
        "service": "Generalized Analysis API",
        "version": "1.0.0",
        "description": "Unified analysis workflow for Sales and Finance",
        "agents": [
            {
                "name": "Researcher Agent",
                "purpose": "Fetches and organizes data from database",
                "tools": ["fetch_entity_data"]
            },
            {
                "name": "Analyzer Agent",
                "purpose": "Performs deep analysis on prepared data",
                "tools": []
            },
            {
                "name": "Summarizer Agent",
                "purpose": "Creates context-specific executive insights",
                "contexts": ["sales", "finance"]
            }
        ],
        "endpoints": {
            "sales": {
                "single": "POST /api/v1/analysis/sales/{account_id}",
                "batch": "POST /api/v1/analysis/batch/sales"
            },
            "finance": {
                "single": "POST /api/v1/analysis/finance/{project_id}",
                "batch": "POST /api/v1/analysis/batch/finance"
            }
        },
        "data_sources": {
            "sales": [
                "account_dashboard",
                "account_documents"
            ],
            "finance": [
                "projects",
                "project_documents",
                "revenue_master"
            ]
        }
    }
