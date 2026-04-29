import json
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.db.session import SessionLocal
from backend.utitlites.s3_storage import upload_data_to_s3, download_data_from_s3
from backend.doc_insighter.tools.app_logger import Logger

# Database Models
from backend.finance.app.models.project import Project
from backend.finance.app.models.revenue import RevenueMaster
from backend.finance.app.models.account import Account
from backend.finance.app.models.document import ProjectDocument

log = Logger()

class DataFetcher:
    """Fetches specialized data for either Sales (Account-wise) or Finance (Project-wise)."""

    @staticmethod
    def _json_or_message(value: str, message_key: str = "message") -> dict:
        """Parse JSON tool output, preserving plain-text partial-data messages."""
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return {message_key: value}
    
    @staticmethod
    def get_financial_metrics(entity_id: UUID, entity_type: str) -> str:
        db = SessionLocal()
        try:
            # --- FINANCE ACCOUNT PATH ---
            if entity_type.lower() == 'account':
                account = db.query(Account).filter(Account.id == entity_id).first()
                
                if not account: return "Finance Account not found."
                
                projects = db.query(Project).filter(Project.account_id == entity_id).all()
                rev_summary = db.query(func.sum(RevenueMaster.total_revenue))\
                                .join(Project, Project.id == RevenueMaster.project_id)\
                                .filter(Project.account_id == entity_id).scalar() or 0
                expected_summary = db.query(func.sum(RevenueMaster.expected_revenue))\
                                .join(Project, Project.id == RevenueMaster.project_id)\
                                .filter(Project.account_id == entity_id).scalar() or 0

                project_summaries = []
                projects_with_insights = 0
                for project in projects:
                    if project.overall_insights:
                        projects_with_insights += 1

                    project_summaries.append({
                        "project_id": str(project.id),
                        "project_name": project.name,
                        "status": project.status,
                        "project_type": project.project_type,
                        "has_overall_insights": project.overall_insights is not None,
                        "overall_insights": project.overall_insights
                    })

                return json.dumps({
                    "context": "Finance Account Analysis",
                    "account_id": str(account.id),
                    "account_name": account.name,
                    "customer_overview": account.customer_overview,
                    "target_revenue": float(account.target_revenue or 0),
                    "forecast_revenue": float(account.forecast_revenue or 0),
                    "shortfall": float(account.shortfall or ((account.target_revenue or 0) - (account.forecast_revenue or 0))),
                    "total_revenue_across_projects": float(rev_summary or 0),
                    "expected_revenue_across_projects": float(expected_summary or 0),
                    "projects_count": len(projects),
                    "projects_with_insights": projects_with_insights,
                    "projects": project_summaries,
                    "status": "Active Finance Account"
                }, indent=2)

            # --- LEGACY SALES PATH ---
            elif entity_type.lower() == 'sales':
                return "Sales analysis is disabled for this generalized finance workflow."

            # --- FINANCE PATH (Project-wise) ---
            elif entity_type.lower() in ['finance', 'project']:
                project = db.query(Project).filter(Project.id == entity_id).first()
                # Fetching fields from revenue_master and projects table
                revenue = db.query(
                    func.sum(RevenueMaster.total_revenue).label('actual'),
                    func.sum(RevenueMaster.expected_revenue).label('expected')
                ).filter(RevenueMaster.project_id == entity_id).first()

                if not project: return "Finance Project not found."

                return json.dumps({
                    "context": "Finance Project Analysis",
                    "project_name": project.name,
                    "project_status": project.status,
                    "project_type": project.project_type,
                    "financials": {
                        "actual_revenue": float(revenue.actual or 0),
                        "expected_revenue": float(revenue.expected or 0),
                        "variance": float((revenue.expected or 0) - (revenue.actual or 0))
                    }
                }, indent=2)
            
            return "Invalid entity type."
        finally:
            db.close()

    @staticmethod
    def get_document_insights(entity_id: UUID, entity_type: str) -> str:
        db = SessionLocal()
        try:
            if entity_type.lower() in ['finance', 'project']:
                documents = db.query(ProjectDocument).filter(ProjectDocument.project_id == entity_id).all()
            elif entity_type.lower() == 'account':
                documents = db.query(ProjectDocument)\
                    .join(Project, Project.id == ProjectDocument.project_id)\
                    .filter(Project.account_id == entity_id)\
                    .all()
            else:
                return f"No document insights fetcher configured for entity type: {entity_type}"

            if not documents: return "No uploaded document insights found."

            combined_insights = {}
            for doc in documents:
                # doc.content contains the JSON generated by the individual doc agents
                try:
                    combined_insights[doc.document_type] = json.loads(doc.content)
                except:
                    combined_insights[doc.document_type] = doc.content
            
            return json.dumps(combined_insights, indent=2)
        finally:
            db.close()

    @staticmethod
    def fetch_and_upload_data_to_s3(entity_id: UUID, entity_type: str) -> dict:
        """
        Fetch data from DB and upload to S3.
        
        This orchestrates the complete flow:
        1. Fetch data from database
        2. Upload JSON to S3 with entity-aware naming
        3. Return S3 key for agents to use
        
        Args:
            entity_id: Account ID or Project ID (UUID)
            entity_type: 'account' or 'project'
        
        Returns:
            Dictionary with S3 key and entity info:
            {
                "s3_key": "temp/account_<id>_<date>.json",
                "entity_id": "<id>",
                "entity_type": "account",
                "bucket": "bucket-name"
            }
        """
        try:
            log.log_info(f"Starting data fetch and S3 upload for {entity_type} {entity_id}")
            
            # Fetch data from database
            metrics_json = DataFetcher.get_financial_metrics(entity_id, entity_type)
            metrics_data = DataFetcher._json_or_message(metrics_json, "error")
            
            insights_json = DataFetcher.get_document_insights(entity_id, entity_type)
            insights_data = DataFetcher._json_or_message(insights_json, "message")

            warnings = []
            if "error" in metrics_data:
                warnings.append(f"Metrics fetch: {metrics_data['error']}")
            if "message" in insights_data:
                warnings.append(f"Document insights: {insights_data['message']}")
            
            # Combine all data
            combined_data = {
                "entity_id": str(entity_id),
                "entity_type": entity_type.lower(),
                "metrics": metrics_data,
                "insights": insights_data,
                "warnings": warnings,
                "timestamp": {"generated_at": str(__import__('datetime').datetime.now())}
            }
            
            # Upload to S3
            s3_key = upload_data_to_s3(combined_data, entity_id, entity_type)
            
            result = {
                "s3_key": s3_key,
                "entity_id": str(entity_id),
                "entity_type": entity_type.lower(),
                "bucket": "nit-project-insighter",
                "status": "success"
            }
            
            log.log_info(f"Successfully uploaded {entity_type} data to S3: {s3_key}")
            return result
            
        except Exception as e:
            error_msg = f"Error fetching and uploading data: {str(e)}"
            log.log_error(error_msg)
            return {
                "status": "error",
                "error": error_msg,
                "entity_id": str(entity_id),
                "entity_type": entity_type.lower()
            }
