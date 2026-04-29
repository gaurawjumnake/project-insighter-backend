"""
Finance Data Aggregation Service

Provides methods to fetch and aggregate finance data at different hierarchy levels
(project, account, private equity) with optional lower-level insights.

This service handles:
1. Database queries with optimized joins (joinedload)
2. Aggregation logic (account ← projects, PE ← accounts)
3. Warning system for missing data
4. Structured JSON output for S3 staging
"""

from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from backend.db.session import SessionLocal
from backend.doc_insighter.tools.app_logger import Logger
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Import database models
from backend.finance.app.models.project import Project
from backend.finance.app.models.account import Account
from backend.finance.app.models.private_equity import PrivateEquity
from backend.finance.app.models.private_equity_document import PrivateEquityDocument
from backend.finance.app.models.revenue import RevenueMaster
from backend.finance.app.models.document import ProjectDocument

log = Logger()


class FinanceAggregationService:
    """Fetches and aggregates finance data at different hierarchy levels."""
    
    @staticmethod
    def get_project_data(project_id: UUID, db: Optional[Session] = None) -> Tuple[Dict[str, Any], List[str]]:
        """
        Fetch and aggregate project-level data.
        
        Returns:
            Tuple of (data_dict, warnings_list)
        """
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False
        
        warnings = []
        
        try:
            # Fetch project with joinedload for documents
            project = db.query(Project).options(
                joinedload(Project.project_documents)
            ).filter(Project.id == project_id).first()
            
            if not project:
                raise ValueError(f"Project not found: {project_id}")
            
            # Fetch revenue data
            revenue_stats = db.query(
                func.sum(RevenueMaster.total_revenue).label('actual'),
                func.sum(RevenueMaster.expected_revenue).label('expected'),
                func.count(RevenueMaster.id).label('count')
            ).filter(RevenueMaster.project_id == project_id).first()
            
            # Build project data
            project_data = {
                "entity_type": "project",
                "entity_id": str(project.id),
                "entity_name": project.name,
                "hierarchy_level": "project",
                "description": project.overview or "",
                "status": project.status or "Active",
                "project_type": project.project_type or "Standard",
                
                # Financial metrics
                "financials": {
                    "actual_revenue": float(revenue_stats.actual or 0),
                    "expected_revenue": float(revenue_stats.expected or 0),
                    "variance": float((revenue_stats.expected or 0) - (revenue_stats.actual or 0)),
                    "variance_percentage": (
                        round(((revenue_stats.expected or 1) - (revenue_stats.actual or 0)) / (revenue_stats.expected or 1) * 100, 2)
                        if revenue_stats.expected else 0
                    ),
                    "revenue_records_count": revenue_stats.count or 0
                },
                
                # Documents metadata
                "documents": {
                    "total_count": len(project.project_documents) if project.project_documents else 0,
                    "types": list(set(d.document_type for d in project.project_documents)) if project.project_documents else [],
                    "has_documents": len(project.project_documents) > 0 if project.project_documents else False
                },
                
                # Timestamps
                "generated_at": datetime.utcnow().isoformat(),
                "data_fetched_at": datetime.utcnow().isoformat()
            }
            
            # Add warnings for missing data
            if not project.project_documents or len(project.project_documents) == 0:
                warnings.append("No project documents found")
            
            if revenue_stats.count == 0:
                warnings.append("No revenue records found for project")
            
            return project_data, warnings
            
        except Exception as e:
            log.log_error(f"Error fetching project data: {str(e)}")
            raise
        finally:
            if should_close:
                db.close()
    
    @staticmethod
    def get_account_data(account_id: UUID, db: Optional[Session] = None) -> Tuple[Dict[str, Any], List[str]]:
        """
        Fetch and aggregate account-level data with project insights.
        
        Aggregates:
        - Account metadata
        - All projects under account with their overall_insights
        - Financial summary with shortfall analysis
        - Revenue data from all projects
        
        Returns:
            Tuple of (data_dict, warnings_list)
        """
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False
        
        warnings = []
        
        try:
            # Fetch account
            account = db.query(Account).filter(Account.id == account_id).first()
            
            if not account:
                raise ValueError(f"Account not found: {account_id}")
            
            # Fetch projects under the finance account. overall_insights is a JSONB
            # column, not a relationship, so it should not be eager-loaded.
            projects = db.query(Project).filter(Project.account_id == account_id).all()
            
            # Fetch revenue data for all projects
            revenue_stats = db.query(
                func.sum(RevenueMaster.total_revenue).label('actual'),
                func.sum(RevenueMaster.expected_revenue).label('expected'),
                func.count(RevenueMaster.id).label('count')
            ).join(Project, RevenueMaster.project_id == Project.id).filter(
                Project.account_id == account_id
            ).first()
            
            # Build project summaries
            project_summaries = []
            projects_with_insights = 0
            
            for proj in projects:
                proj_summary = {
                    "project_id": str(proj.id),
                    "project_name": proj.name,
                    "status": proj.status or "Active",
                    "has_overall_insights": proj.overall_insights is not None
                }
                
                if proj.overall_insights:
                    projects_with_insights += 1
                    # Include key metrics from overall_insights if available
                    if isinstance(proj.overall_insights, dict):
                        proj_summary["confidence_score"] = proj.overall_insights.get("confidence_score", 0)
                        proj_summary["executive_summary"] = proj.overall_insights.get("executive_summary", "")[:200]
                
                project_summaries.append(proj_summary)
            
            # Calculate shortfall analysis
            shortfall = (account.target_revenue or 0) - (account.forecast_revenue or 0)
            
            # Build account data
            account_data = {
                "entity_type": "account",
                "entity_id": str(account.id),
                "entity_name": account.name,
                "hierarchy_level": "account",
                "description": account.customer_overview or "",
                "status": "Active",
                
                # Financial metrics
                "financials": {
                    "target_revenue": float(account.target_revenue or 0),
                    "forecast_revenue": float(account.forecast_revenue or 0),
                    "shortfall": float(shortfall),
                    "shortfall_percentage": round(shortfall / (account.target_revenue or 1) * 100, 2) if account.target_revenue else 0,
                    "actual_revenue": float(revenue_stats.actual or 0),
                    "expected_revenue": float(revenue_stats.expected or 0),
                    "revenue_variance": float((revenue_stats.expected or 0) - (revenue_stats.actual or 0))
                },
                
                # Project aggregation
                "projects": {
                    "total_count": len(projects),
                    "with_insights_count": projects_with_insights,
                    "summaries": project_summaries
                },
                
                # Data quality
                "data_quality": {
                    "projects_count": len(projects),
                    "projects_with_insights": projects_with_insights,
                    "has_target_revenue": account.target_revenue is not None,
                    "has_forecast_revenue": account.forecast_revenue is not None
                },
                
                # Timestamps
                "generated_at": datetime.utcnow().isoformat(),
                "data_fetched_at": datetime.utcnow().isoformat()
            }
            
            # Add warnings
            if len(projects) == 0:
                warnings.append("No projects found for account")
            
            if projects_with_insights < len(projects):
                warnings.append(f"Only {projects_with_insights} of {len(projects)} projects have overall_insights")
            
            if account.target_revenue is None:
                warnings.append("Account missing target_revenue")
            
            if account.forecast_revenue is None:
                warnings.append("Account missing forecast_revenue")
            
            return account_data, warnings
            
        except Exception as e:
            log.log_error(f"Error fetching account data: {str(e)}")
            raise
        finally:
            if should_close:
                db.close()
    
    @staticmethod
    def get_pe_data(pe_id: UUID, db: Optional[Session] = None) -> Tuple[Dict[str, Any], List[str]]:
        """
        Fetch and aggregate PE-level data with account insights.
        
        Aggregates:
        - PE metadata
        - All accounts under PE with their account_insights
        - PE documents (company_capabilities, pe_details)
        - Company capabilities
        - Portfolio financial summary
        
        Returns:
            Tuple of (data_dict, warnings_list)
        """
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False
        
        warnings = []
        
        try:
            # Fetch PE with relationships
            pe = db.query(PrivateEquity).options(
                joinedload(PrivateEquity.documents)
            ).filter(PrivateEquity.id == pe_id).first()
            
            if not pe:
                raise ValueError(f"Private Equity entity not found: {pe_id}")
            
            # Fetch all accounts under PE
            accounts = db.query(Account).filter(Account.private_equity_id == pe_id).all()
            
            # Fetch all revenue for PE portfolio
            revenue_stats = db.query(
                func.sum(RevenueMaster.total_revenue).label('actual'),
                func.sum(RevenueMaster.expected_revenue).label('expected'),
                func.count(RevenueMaster.id).label('count')
            ).join(Project, RevenueMaster.project_id == Project.id).join(
                Account, Project.account_id == Account.id
            ).filter(Account.private_equity_id == pe_id).first()
            
            # Build document summaries
            doc_summaries = []
            company_capabilities_content = None
            
            if pe.documents:
                for doc in pe.documents:
                    doc_summary = {
                        "document_type": doc.document_type,
                        "file_name": doc.file_name,
                        "created_at": doc.created_at.isoformat() if doc.created_at else None
                    }
                    doc_summaries.append(doc_summary)
                    
                    # Capture company capabilities if available
                    if doc.document_type == "company_capabilities":
                        company_capabilities_content = doc.content[:500] if doc.content else None
            
            # Build account summaries
            account_summaries = []
            accounts_with_insights = 0
            
            for account in accounts:
                acc_summary = {
                    "account_id": str(account.id),
                    "account_name": account.name,
                    "status": "Active",
                    "has_account_insights": account.account_insights is not None,
                    "target_revenue": float(account.target_revenue or 0),
                    "forecast_revenue": float(account.forecast_revenue or 0)
                }
                
                if account.account_insights:
                    accounts_with_insights += 1
                    if isinstance(account.account_insights, dict):
                        acc_summary["confidence_score"] = account.account_insights.get("confidence_score", 0)
                
                account_summaries.append(acc_summary)
            
            # Build PE data
            pe_data = {
                "entity_type": "private_equity",
                "entity_id": str(pe.id),
                "entity_name": pe.name,
                "hierarchy_level": "private_equity",
                "description": pe.overview or "",
                "investment_stage": "Unknown",
                
                # Portfolio financials
                "portfolio_financials": {
                    "total_accounts": len(accounts),
                    "actual_revenue": float(revenue_stats.actual or 0),
                    "expected_revenue": float(revenue_stats.expected or 0),
                    "variance": float((revenue_stats.expected or 0) - (revenue_stats.actual or 0)),
                    "portfolio_size_metric": f"{len(accounts)} accounts"
                },
                
                # Account aggregation
                "accounts": {
                    "total_count": len(accounts),
                    "with_insights_count": accounts_with_insights,
                    "summaries": account_summaries
                },
                
                # Documents and capabilities
                "documents": {
                    "total_count": len(pe.documents) if pe.documents else 0,
                    "types": list(set(d.document_type for d in pe.documents)) if pe.documents else [],
                    "summaries": doc_summaries,
                    "has_company_capabilities": any(d.document_type == "company_capabilities" for d in (pe.documents or []))
                },
                
                "company_capabilities_summary": company_capabilities_content or "Not provided",
                
                # Data quality
                "data_quality": {
                    "accounts_count": len(accounts),
                    "accounts_with_insights": accounts_with_insights,
                    "documents_count": len(pe.documents) if pe.documents else 0,
                    "has_company_capabilities": company_capabilities_content is not None
                },
                
                # Timestamps
                "generated_at": datetime.utcnow().isoformat(),
                "data_fetched_at": datetime.utcnow().isoformat()
            }
            
            # Add warnings
            if len(accounts) == 0:
                warnings.append("No accounts found for PE entity")
            
            if accounts_with_insights < len(accounts):
                warnings.append(f"Only {accounts_with_insights} of {len(accounts)} accounts have account_insights")
            
            if not pe.documents or len(pe.documents) == 0:
                warnings.append("No PE documents found")
            
            if not company_capabilities_content:
                warnings.append("No company_capabilities document found")
            
            return pe_data, warnings
            
        except Exception as e:
            log.log_error(f"Error fetching PE data: {str(e)}")
            raise
        finally:
            if should_close:
                db.close()
