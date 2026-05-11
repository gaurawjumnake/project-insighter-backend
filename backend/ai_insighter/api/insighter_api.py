"""
Insights API Router
───────────────────
Endpoints:
    POST /api/v1/insights/project/{project_id}   — generate project insights
    GET  /api/v1/insights/project/{project_id}   — retrieve project insights
    POST /api/v1/insights/account/{account_id}   — generate account insights
    GET  /api/v1/insights/account/{account_id}   — retrieve account insights
    POST /api/v1/insights/pe/{pe_id}             — generate PE insights
    GET  /api/v1/insights/pe/{pe_id}             — retrieve PE insights
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timezone

from backend.db.session import get_db
from backend.finance.app.models.project import Project
from backend.finance.app.models.account import Account
from backend.finance.app.models.private_equity import PrivateEquity
from backend.doc_insighter.tools.app_logger import Logger
from backend.utitlites.llm_models import llm

from backend.ai_insighter.services.project_insighter import analyse as ProjectService
from backend.ai_insighter.services.accounts_insighter import analyse as AccountService
from backend.ai_insighter.services.pe_insighter import analyse as PEService

log = Logger()

router = APIRouter(prefix="/api/v1/insights", tags=["Insights"])


# # - Response models ---------------------------------------------------

class InsightGenerationResponse(BaseModel):
    status: str
    entity_type: str
    entity_id: str
    entity_name: Optional[str] = None
    insights: Optional[Dict[str, Any]] = None
    generated_at: Optional[str] = None
    error: Optional[str] = None


class InsightRetrievalResponse(BaseModel):
    status: str
    entity_type: str
    entity_id: str
    entity_name: Optional[str] = None
    insights: Optional[Dict[str, Any]] = None
    insights_generated_at: Optional[str] = None
    has_insights: bool


def _validate_uuid(raw_id: str, label: str) -> UUID:
    try:
        return UUID(raw_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {label} format. Must be a valid UUID. Got: {raw_id}"
        )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# # - Project endpoints --------------------------------------------

@router.post(
    "/project/{project_id}",
    response_model=InsightGenerationResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def generate_project_insights(
    project_id: str,
    db: Session = Depends(get_db),
) -> InsightGenerationResponse:
    """
    Generate project-level insights.
    Fetches project data from DB, runs CrewAI analysis,
    persists result to projects.overall_insights.
    """
    _validate_uuid(project_id, "project ID")

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project not found: {project_id}")

    log.log_info(f"Generating insights for project: {project_id} ({project.name})")

    try:
        # Assemble data — no DB calls inside the pipeline
        data = {
            "project_id":        str(project.id),
            "project_name":      project.name,
            "account_id":        str(project.account_id),
            "status":            project.status,
            "from_date":         str(project.from_date) if project.from_date is not None else None,
            "to_date":           str(project.to_date) if project.to_date is not None else None,
            "revenue":           getattr(project, 'revenue_data', None) or [],
            "documents":         getattr(project, 'documents', None) or [],
            "ai_direct_hours":   project.ai_direct_hours,
            "ai_assist_hours":   project.ai_assist_hours,
            "code_coverage_pct": project.code_coverage_pct,
        }

        insights = ProjectService(project_data=data)

        # Persist
        project.overall_insights = insights  # type: ignore
        project.overall_insights_generated_at = datetime.now(timezone.utc)  # type: ignore
        db.commit()

        return InsightGenerationResponse(
            status="success",
            entity_type="project",
            entity_id=project_id,
            entity_name=str(project.name) if project.name is not None else None,
            insights=insights,
            generated_at=_now(),
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log.log_error(f"Error generating project insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project/{project_id}", response_model=InsightRetrievalResponse)
def retrieve_project_insights(
    project_id: str,
    db: Session = Depends(get_db),
) -> InsightRetrievalResponse:
    """Retrieve stored project insights."""
    _validate_uuid(project_id, "project ID")

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project not found: {project_id}")

    return InsightRetrievalResponse(
        status="success",
        entity_type="project",
        entity_id=project_id,
        entity_name=str(project.name) if project.name is not None else None,
        insights=dict(project.overall_insights) if project.overall_insights is not None else None,  # type: ignore
        insights_generated_at=(
            project.overall_insights_generated_at.isoformat()
            if project.overall_insights_generated_at is not None else None
        ),
        has_insights=project.overall_insights is not None,
    )


# # - Account endpoints -------------------------------------------------

@router.post(
    "/account/{account_id}",
    response_model=InsightGenerationResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def generate_account_insights(
    account_id: str,
    db: Session = Depends(get_db),
) -> InsightGenerationResponse:
    """
    Generate account-level insights.
    Reads pre-generated project insights from DB — never re-analyses projects.
    Persists result to accounts.account_insights.
    """
    _validate_uuid(account_id, "account ID")

    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail=f"Account not found: {account_id}")

    log.log_info(f"Generating insights for account: {account_id} ({account.name})")

    try:
        # Account-level data
        account_data = {
            "account_id":   str(account.id),
            "account_name": account.name,
            "industry":     getattr(account, 'industry', None) or '',
            "region":       getattr(account, 'region', None) or '',
            "revenue":      getattr(account, 'revenue_data', None) or [],
        }

        # Pull pre-generated project insights — compact, never raw data
        project_insights = [
            {
                "project_id":   str(p.id),
                "project_name": p.name,
                "status":       p.status,
                "insight":      p.overall_insights,
            }
            for p in account.projects
            if p.overall_insights is not None
        ]

        # Delivery unit data if available
        delivery_unit_data = getattr(account, 'delivery_unit_data', None)

        insights = AccountService(
            account_data       = account_data,
            project_insights   = project_insights,
            delivery_unit_data = delivery_unit_data,
        )

        # Persist
        account.account_insights = insights  # type: ignore
        account.account_insights_generated_at = datetime.now(timezone.utc)  # type: ignore
        db.commit()

        return InsightGenerationResponse(
            status="success",
            entity_type="account",
            entity_id=account_id,
            entity_name=str(account.name) if account.name is not None else None,
            insights=insights,
            generated_at=_now(),
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log.log_error(f"Error generating account insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/account/{account_id}", response_model=InsightRetrievalResponse)
def retrieve_account_insights(
    account_id: str,
    db: Session = Depends(get_db),
) -> InsightRetrievalResponse:
    """Retrieve stored account insights."""
    _validate_uuid(account_id, "account ID")

    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail=f"Account not found: {account_id}")

    return InsightRetrievalResponse(
        status="success",
        entity_type="account",
        entity_id=account_id,
        entity_name=str(account.name) if account.name is not None else None,
        insights=dict(account.account_insights) if account.account_insights is not None else None,  # type: ignore
        insights_generated_at=(
            account.account_insights_generated_at.isoformat()
            if account.account_insights_generated_at is not None else None
        ),
        has_insights=account.account_insights is not None,
    )


# # - PE endpoints -------------------------------------------------------

@router.post(
    "/pe/{pe_id}",
    response_model=InsightGenerationResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def generate_pe_insights(
    pe_id: str,
    db: Session = Depends(get_db),
) -> InsightGenerationResponse:
    """
    Generate PE-level portfolio insights.
    Reads pre-generated account insights from DB.
    Persists result to private_equity.pe_insights.
    """
    _validate_uuid(pe_id, "PE ID")

    pe = db.query(PrivateEquity).filter(PrivateEquity.id == pe_id).first()
    if not pe:
        raise HTTPException(status_code=404, detail=f"PE entity not found: {pe_id}")

    log.log_info(f"Generating insights for PE: {pe_id} ({pe.name})")

    try:
        # Pull pre-generated account insights
        account_insights = [
            {
                "account_id":   str(a.id),
                "account_name": a.name,
                "insight":      a.account_insights,
            }
            for a in pe.accounts
            if a.account_insights is not None
        ]

        company_capabilities = dict(getattr(pe, 'company_capabilities', None) or {})
        pe_research_document = pe.documents or {}

        insights = PEService(
            company_capabilities = company_capabilities,
            account_insights     = account_insights,
            pe_research_document = pe_research_document,
        )

        # Persist
        pe.pe_insights = insights  # type: ignore
        pe.pe_insights_generated_at = datetime.now(timezone.utc)  # type: ignore
        db.commit()

        return InsightGenerationResponse(
            status="success",
            entity_type="private_equity",
            entity_id=pe_id,
            entity_name=str(pe.name) if pe.name is not None else None,
            insights=insights,
            generated_at=_now(),
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log.log_error(f"Error generating PE insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pe/{pe_id}", response_model=InsightRetrievalResponse)
def retrieve_pe_insights(
    pe_id: str,
    db: Session = Depends(get_db),
) -> InsightRetrievalResponse:
    """Retrieve stored PE insights."""
    _validate_uuid(pe_id, "PE ID")

    pe = db.query(PrivateEquity).filter(PrivateEquity.id == pe_id).first()
    if not pe:
        raise HTTPException(status_code=404, detail=f"PE entity not found: {pe_id}")

    return InsightRetrievalResponse(
        status="success",
        entity_type="private_equity",
        entity_id=pe_id,
        entity_name=str(pe.name) if pe.name is not None else None,
        insights=dict(pe.pe_insights) if pe.pe_insights is not None else None,  # type: ignore
        insights_generated_at=(
            pe.pe_insights_generated_at.isoformat()
            if pe.pe_insights_generated_at is not None else None
        ),
        has_insights=pe.pe_insights is not None,
    )