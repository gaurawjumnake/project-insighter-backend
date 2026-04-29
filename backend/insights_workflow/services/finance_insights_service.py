"""
Finance Insights Service

Orchestrates the complete end-to-end workflow for generating finance insights:
1. Fetch data from DB and aggregate at each hierarchy level
2. Transform aggregated data to stable JSON
3. Upload JSON to S3
4. Run domain-neutral crew analysis
5. Persist results to database

This service provides three main methods:
- generate_project_insights(project_id)
- generate_account_insights(account_id)  
- generate_pe_insights(pe_id)

Each method follows: Fetch → Transform → S3 Upload → S3 Fetch → Crew Analysis → DB Persist
"""

from uuid import UUID
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from backend.db.session import SessionLocal
from backend.doc_insighter.tools.app_logger import Logger
from backend.utitlites.s3_storage import upload_data_to_s3, download_data_from_s3
from backend.insights_workflow.services.finance_aggregation_service import FinanceAggregationService
from backend.insights_workflow.services.json_transformer import JsonTransformer
from backend.insights_workflow.core.generalized_crew import DomainNeutralAnalysisCrew

# Database models for persistence
from backend.finance.app.models.project import Project
from backend.finance.app.models.account import Account
from backend.finance.app.models.private_equity import PrivateEquity

log = Logger()


class FinanceInsightsService:
    """Service for generating and persisting finance insights at all hierarchy levels."""
    
    # Analysis goals for each hierarchy level
    ANALYSIS_GOALS = {
        'project': 'Generate comprehensive project-level financial insights including profitability, revenue analysis, and optimization opportunities',
        'account': 'Generate account-level financial insights including portfolio performance, shortfall analysis, and strategic recommendations',
        'private_equity': 'Generate PE-level portfolio insights including company capabilities alignment and investment opportunity assessment'
    }
    
    @staticmethod
    def generate_project_insights(project_id: str) -> Dict[str, Any]:
        """
        Generate and persist insights for a project.
        
        Workflow:
        1. Fetch project data from DB
        2. Transform to S3 JSON
        3. Upload to S3
        4. Run crew analysis
        5. Persist to projects.overall_insights
        
        Returns:
            Result dict with status, s3_key, insights, and persisted_at timestamp
        """
        db = SessionLocal()
        try:
            project_uuid = UUID(project_id)
        except ValueError:
            return {
                "status": "error",
                "error": f"Invalid UUID format: {project_id}",
                "entity_type": "project"
            }
        
        try:
            # ===== STAGE 1: FETCH DATA =====
            log.log_info(f"[PROJECT {project_id}] Stage 1: Fetching project data...")
            project_data, warnings = FinanceAggregationService.get_project_data(project_uuid, db)
            project_name = project_data.get("entity_name", "Unknown")
            log.log_info(f"[PROJECT {project_id}] Fetched project data: {project_name}")
            
            # ===== STAGE 2: TRANSFORM TO JSON =====
            log.log_info(f"[PROJECT {project_id}] Stage 2: Transforming to S3 JSON...")
            s3_payload, s3_filename = JsonTransformer.transform_data_for_s3(project_data, warnings)
            is_valid, validation_errors = JsonTransformer.validate_s3_payload(s3_payload)
            if not is_valid:
                log.log_error(f"[PROJECT {project_id}] Validation errors: {validation_errors}")
                return {
                    "status": "error",
                    "error": f"S3 payload validation failed: {validation_errors}",
                    "entity_type": "project"
                }
            log.log_info(f"[PROJECT {project_id}] Payload validation passed")
            
            # ===== STAGE 3: UPLOAD TO S3 =====
            log.log_info(f"[PROJECT {project_id}] Stage 3: Uploading to S3...")
            s3_key = upload_data_to_s3(s3_payload, project_uuid, "project")
            log.log_info(f"[PROJECT {project_id}] Uploaded to S3: {s3_key}")
            
            # ===== STAGE 4: RUN CREW ANALYSIS =====
            log.log_info(f"[PROJECT {project_id}] Stage 4: Running crew analysis...")
            analysis_goal = FinanceInsightsService.ANALYSIS_GOALS.get(
                'project',
                'Generate comprehensive financial insights'
            )
            crew = DomainNeutralAnalysisCrew(
                entity_type='project',
                s3_key=s3_key,
                analysis_goal=analysis_goal,
                entity_id=project_id,
                entity_name=project_name
            )
            crew_result = crew.analyze()
            
            if crew_result.get("status") != "success":
                log.log_error(f"[PROJECT {project_id}] Crew analysis failed: {crew_result.get('error')}")
                return {
                    "status": "error",
                    "error": f"Crew analysis failed: {crew_result.get('error')}",
                    "entity_type": "project",
                    "s3_key": s3_key
                }
            
            insights = crew_result.get("insights", {})
            log.log_info(f"[PROJECT {project_id}] Crew analysis completed")
            
            # ===== STAGE 5: PERSIST TO DB =====
            log.log_info(f"[PROJECT {project_id}] Stage 5: Persisting insights to DB...")
            persisted_at = FinanceInsightsService._persist_project_insights(
                project_uuid, insights, db
            )
            log.log_info(f"[PROJECT {project_id}] Persisted to DB at {persisted_at}")
            
            return {
                "status": "success",
                "entity_type": "project",
                "entity_id": project_id,
                "entity_name": project_name,
                "s3_key": s3_key,
                "insights": insights,
                "persisted_at": persisted_at.isoformat(),
                "warnings": warnings
            }
            
        except Exception as e:
            log.log_error(f"[PROJECT {project_id}] Error generating insights: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "entity_type": "project",
                "entity_id": project_id
            }
        finally:
            db.close()
    
    @staticmethod
    def generate_account_insights(account_id: str) -> Dict[str, Any]:
        """
        Generate and persist insights for an account.
        
        Workflow:
        1. Fetch account data (with projects and project insights)
        2. Transform to S3 JSON
        3. Upload to S3
        4. Run crew analysis
        5. Persist to accounts.account_insights
        
        Returns:
            Result dict with status, s3_key, insights, and persisted_at timestamp
        """
        db = SessionLocal()
        try:
            account_uuid = UUID(account_id)
        except ValueError:
            return {
                "status": "error",
                "error": f"Invalid UUID format: {account_id}",
                "entity_type": "account"
            }
        
        try:
            # ===== STAGE 1: FETCH DATA =====
            log.log_info(f"[ACCOUNT {account_id}] Stage 1: Fetching account data...")
            account_data, warnings = FinanceAggregationService.get_account_data(account_uuid, db)
            account_name = account_data.get("entity_name", "Unknown")
            log.log_info(f"[ACCOUNT {account_id}] Fetched account data: {account_name}")
            
            # ===== STAGE 2: TRANSFORM TO JSON =====
            log.log_info(f"[ACCOUNT {account_id}] Stage 2: Transforming to S3 JSON...")
            s3_payload, s3_filename = JsonTransformer.transform_data_for_s3(account_data, warnings)
            is_valid, validation_errors = JsonTransformer.validate_s3_payload(s3_payload)
            if not is_valid:
                log.log_error(f"[ACCOUNT {account_id}] Validation errors: {validation_errors}")
                return {
                    "status": "error",
                    "error": f"S3 payload validation failed: {validation_errors}",
                    "entity_type": "account"
                }
            log.log_info(f"[ACCOUNT {account_id}] Payload validation passed")
            
            # ===== STAGE 3: UPLOAD TO S3 =====
            log.log_info(f"[ACCOUNT {account_id}] Stage 3: Uploading to S3...")
            s3_key = upload_data_to_s3(s3_payload, account_uuid, "account")
            log.log_info(f"[ACCOUNT {account_id}] Uploaded to S3: {s3_key}")
            
            # ===== STAGE 4: RUN CREW ANALYSIS =====
            log.log_info(f"[ACCOUNT {account_id}] Stage 4: Running crew analysis...")
            analysis_goal = FinanceInsightsService.ANALYSIS_GOALS.get(
                'account',
                'Generate comprehensive account insights'
            )
            crew = DomainNeutralAnalysisCrew(
                entity_type='account',
                s3_key=s3_key,
                analysis_goal=analysis_goal,
                entity_id=account_id,
                entity_name=account_name
            )
            crew_result = crew.analyze()
            
            if crew_result.get("status") != "success":
                log.log_error(f"[ACCOUNT {account_id}] Crew analysis failed: {crew_result.get('error')}")
                return {
                    "status": "error",
                    "error": f"Crew analysis failed: {crew_result.get('error')}",
                    "entity_type": "account",
                    "s3_key": s3_key
                }
            
            insights = crew_result.get("insights", {})
            log.log_info(f"[ACCOUNT {account_id}] Crew analysis completed")
            
            # ===== STAGE 5: PERSIST TO DB =====
            log.log_info(f"[ACCOUNT {account_id}] Stage 5: Persisting insights to DB...")
            persisted_at = FinanceInsightsService._persist_account_insights(
                account_uuid, insights, db
            )
            log.log_info(f"[ACCOUNT {account_id}] Persisted to DB at {persisted_at}")
            
            return {
                "status": "success",
                "entity_type": "account",
                "entity_id": account_id,
                "entity_name": account_name,
                "s3_key": s3_key,
                "insights": insights,
                "persisted_at": persisted_at.isoformat(),
                "warnings": warnings
            }
            
        except Exception as e:
            log.log_error(f"[ACCOUNT {account_id}] Error generating insights: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "entity_type": "account",
                "entity_id": account_id
            }
        finally:
            db.close()
    
    @staticmethod
    def generate_pe_insights(pe_id: str) -> Dict[str, Any]:
        """
        Generate and persist insights for a Private Equity entity.
        
        Workflow:
        1. Fetch PE data (with accounts and account insights)
        2. Transform to S3 JSON
        3. Upload to S3
        4. Run crew analysis
        5. Persist to private_equity.pe_insights
        
        Returns:
            Result dict with status, s3_key, insights, and persisted_at timestamp
        """
        db = SessionLocal()
        try:
            pe_uuid = UUID(pe_id)
        except ValueError:
            return {
                "status": "error",
                "error": f"Invalid UUID format: {pe_id}",
                "entity_type": "private_equity"
            }
        
        try:
            # ===== STAGE 1: FETCH DATA =====
            log.log_info(f"[PE {pe_id}] Stage 1: Fetching PE data...")
            pe_data, warnings = FinanceAggregationService.get_pe_data(pe_uuid, db)
            pe_name = pe_data.get("entity_name", "Unknown")
            log.log_info(f"[PE {pe_id}] Fetched PE data: {pe_name}")
            
            # ===== STAGE 2: TRANSFORM TO JSON =====
            log.log_info(f"[PE {pe_id}] Stage 2: Transforming to S3 JSON...")
            s3_payload, s3_filename = JsonTransformer.transform_data_for_s3(pe_data, warnings)
            is_valid, validation_errors = JsonTransformer.validate_s3_payload(s3_payload)
            if not is_valid:
                log.log_error(f"[PE {pe_id}] Validation errors: {validation_errors}")
                return {
                    "status": "error",
                    "error": f"S3 payload validation failed: {validation_errors}",
                    "entity_type": "private_equity"
                }
            log.log_info(f"[PE {pe_id}] Payload validation passed")
            
            # ===== STAGE 3: UPLOAD TO S3 =====
            log.log_info(f"[PE {pe_id}] Stage 3: Uploading to S3...")
            s3_key = upload_data_to_s3(s3_payload, pe_uuid, "private_equity")
            log.log_info(f"[PE {pe_id}] Uploaded to S3: {s3_key}")
            
            # ===== STAGE 4: RUN CREW ANALYSIS =====
            log.log_info(f"[PE {pe_id}] Stage 4: Running crew analysis...")
            analysis_goal = FinanceInsightsService.ANALYSIS_GOALS.get(
                'private_equity',
                'Generate comprehensive PE insights'
            )
            crew = DomainNeutralAnalysisCrew(
                entity_type='private_equity',
                s3_key=s3_key,
                analysis_goal=analysis_goal,
                entity_id=pe_id,
                entity_name=pe_name
            )
            crew_result = crew.analyze()
            
            if crew_result.get("status") != "success":
                log.log_error(f"[PE {pe_id}] Crew analysis failed: {crew_result.get('error')}")
                return {
                    "status": "error",
                    "error": f"Crew analysis failed: {crew_result.get('error')}",
                    "entity_type": "private_equity",
                    "s3_key": s3_key
                }
            
            insights = crew_result.get("insights", {})
            log.log_info(f"[PE {pe_id}] Crew analysis completed")
            
            # ===== STAGE 5: PERSIST TO DB =====
            log.log_info(f"[PE {pe_id}] Stage 5: Persisting insights to DB...")
            persisted_at = FinanceInsightsService._persist_pe_insights(
                pe_uuid, insights, db
            )
            log.log_info(f"[PE {pe_id}] Persisted to DB at {persisted_at}")
            
            return {
                "status": "success",
                "entity_type": "private_equity",
                "entity_id": pe_id,
                "entity_name": pe_name,
                "s3_key": s3_key,
                "insights": insights,
                "persisted_at": persisted_at.isoformat(),
                "warnings": warnings
            }
            
        except Exception as e:
            log.log_error(f"[PE {pe_id}] Error generating insights: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "entity_type": "private_equity",
                "entity_id": pe_id
            }
        finally:
            db.close()
    
    # =========================================================================
    # PERSISTENCE HELPER METHODS
    # =========================================================================
    
    @staticmethod
    def _persist_project_insights(project_id: UUID, insights: Dict[str, Any], db: Session) -> datetime:
        """
        Persist project insights to database.
        
        Updates: projects.overall_insights and projects.overall_insights_generated_at
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError(f"Project not found: {project_id}")
        
        now = datetime.utcnow()
        project.overall_insights = insights
        project.overall_insights_generated_at = now
        db.commit()
        
        log.log_info(f"Persisted project insights for {project_id}")
        return now
    
    @staticmethod
    def _persist_account_insights(account_id: UUID, insights: Dict[str, Any], db: Session) -> datetime:
        """
        Persist account insights to database.
        
        Updates: accounts.account_insights and accounts.account_insights_generated_at
        """
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise ValueError(f"Account not found: {account_id}")
        
        now = datetime.utcnow()
        account.account_insights = insights
        account.account_insights_generated_at = now
        db.commit()
        
        log.log_info(f"Persisted account insights for {account_id}")
        return now
    
    @staticmethod
    def _persist_pe_insights(pe_id: UUID, insights: Dict[str, Any], db: Session) -> datetime:
        """
        Persist PE insights to database.
        
        Updates: private_equity.pe_insights and private_equity.pe_insights_generated_at
        """
        pe = db.query(PrivateEquity).filter(PrivateEquity.id == pe_id).first()
        if not pe:
            raise ValueError(f"Private Equity entity not found: {pe_id}")
        
        now = datetime.utcnow()
        pe.pe_insights = insights
        pe.pe_insights_generated_at = now
        db.commit()
        
        log.log_info(f"Persisted PE insights for {pe_id}")
        return now
