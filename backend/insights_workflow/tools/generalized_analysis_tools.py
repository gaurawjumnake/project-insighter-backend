"""
Tools for Generalized Analysis Agents

Provides standalone tool functions for the researcher, analyzer, and summarizer agents.
"""

from crewai.tools import tool
from uuid import UUID
import json
from backend.insights_workflow.tools.db_tools import DataFetcher
from backend.doc_insighter.tools.app_logger import Logger
from backend.insights_workflow.tools.s3_data_reader_tool import S3DataReaderTool

log = Logger()


@tool("Fetch Entity Data")
def fetch_entity_data(entity_id: str, entity_type: str) -> str:
    """
    Fetch comprehensive data from the database for the given entity.
    
    Use this tool to retrieve all relevant metrics and insights for either
    a Sales Account or Finance Project.
    
    Args:
        entity_id: UUID of the Account or Project
        entity_type: Either 'sales' or 'finance'
    
    Returns:
        JSON string containing all relevant metrics and insights
    
    For Sales (Account):
        - Data from account_dashboard table
        - Data from account_documents table
        - Aggregated revenue metrics
    
    For Finance (Project):
        - Data from projects table
        - Data from project_documents table
        - Data from revenue_master table (actual vs expected revenue)
    """
    try:
        log.log_info(f"Fetching data for {entity_type} entity: {entity_id}")
        
        # Validate entity_id format
        try:
            entity_uuid = UUID(entity_id)
        except ValueError:
            error_response = {
                "error": f"Invalid UUID format: {entity_id}",
                "status": "failed",
                "entity_type": entity_type
            }
            log.log_error(f"Invalid UUID format: {entity_id}")
            return json.dumps(error_response, indent=2)
        
        # Validate entity_type
        if entity_type.lower() not in ['sales', 'finance', 'account', 'project']:
            error_response = {
                "error": f"Invalid entity_type: {entity_type}. Must be 'sales' or 'finance'",
                "status": "failed",
                "entity_id": entity_id
            }
            log.log_error(f"Invalid entity_type: {entity_type}")
            return json.dumps(error_response, indent=2)
        
        # Fetch metrics data
        metrics = None
        insights = None
        metrics_error = None
        insights_error = None
        
        try:
            metrics_json = DataFetcher.get_financial_metrics(entity_uuid, entity_type)
            # Check if response is a plain string error message
            if "not found" in metrics_json.lower() or metrics_json == "Invalid entity type.":
                metrics_error = metrics_json
                metrics = {"error": metrics_json}
            else:
                try:
                    metrics = json.loads(metrics_json)
                except:
                    metrics = {"raw_response": metrics_json}
        except Exception as e:
            error_msg = f"Failed to fetch metrics: {str(e)}"
            log.log_error(error_msg)
            metrics_error = error_msg
            metrics = {"error": error_msg}
        
        # Fetch document insights
        try:
            insights_json = DataFetcher.get_document_insights(entity_uuid, entity_type)
            # Check if response indicates no documents found
            if "not found" in insights_json.lower() or "no uploaded" in insights_json.lower():
                insights_error = insights_json
                insights = {"message": insights_json}
            else:
                try:
                    insights = json.loads(insights_json)
                except:
                    insights = {"raw_response": insights_json}
        except Exception as e:
            error_msg = f"Failed to fetch insights: {str(e)}"
            log.log_error(error_msg)
            insights_error = error_msg
            insights = {"error": error_msg}
        
        # Build response
        combined = {
            "entity_id": entity_id,
            "entity_type": entity_type.lower(),
            "status": "success" if not metrics_error else "partial",
            "metrics": metrics,
            "document_insights": insights
        }
        
        # Add warnings if there were any errors
        if metrics_error or insights_error:
            combined["warnings"] = []
            if metrics_error:
                combined["warnings"].append(f"Metrics fetch: {metrics_error}")
            if insights_error:
                combined["warnings"].append(f"Insights fetch: {insights_error}")
        
        log.log_info(f"Successfully fetched data for {entity_type} entity: {entity_id}")
        return json.dumps(combined, indent=2)
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "status": "failed",
            "entity_id": entity_id,
            "entity_type": entity_type
        }
        log.log_error(f"Unexpected error in fetch_entity_data: {str(e)}")
        return json.dumps(error_response, indent=2)


@tool("Fetch and Upload to S3")
def fetch_and_upload_to_s3(entity_id: str, entity_type: str) -> str:
    """
    Fetch comprehensive data from database and upload to S3 for scalable processing.
    
    This tool orchestrates the complete data extraction and S3 upload flow:
    1. Fetch data from database (metrics and insights)
    2. Combine into single JSON structure
    3. Upload to S3
    4. Return S3 key for downstream processing
    
    This approach enables:
    - Immediate release of database connections (prevents connection pool exhaustion)
    - Scalable concurrent processing (multiple crews can process from S3 simultaneously)
    - Efficient resource utilization (separate DB extraction from agent processing)
    
    Args:
        entity_id: UUID of the Account or Project
        entity_type: Either 'sales', 'finance', 'account', or 'project'
    
    Returns:
        JSON string with S3 key and metadata:
        {
            "s3_key": "temp/account_<id>_<date>.json",
            "entity_id": "<uuid>",
            "entity_type": "account|project",
            "bucket": "nit-project-insighter",
            "status": "success"
        }
    
    This S3 key is then used by downstream agents to download and analyze data.
    """
    try:
        log.log_info(f"Uploading {entity_type} entity data to S3: {entity_id}")
        
        # Validate entity_id format
        try:
            entity_uuid = UUID(entity_id)
        except ValueError:
            error_response = {
                "error": f"Invalid UUID format: {entity_id}",
                "status": "failed",
                "entity_type": entity_type
            }
            log.log_error(f"Invalid UUID format: {entity_id}")
            return json.dumps(error_response, indent=2)
        
        # Validate entity_type
        if entity_type.lower() not in ['sales', 'finance', 'account', 'project']:
            error_response = {
                "error": f"Invalid entity_type: {entity_type}. Must be 'sales', 'finance', 'account', or 'project'",
                "status": "failed",
                "entity_id": entity_id
            }
            log.log_error(f"Invalid entity_type: {entity_type}")
            return json.dumps(error_response, indent=2)
        
        # Normalize entity_type to match database fetcher expectations
        normalized_type = 'account' if entity_type.lower() == 'sales' else 'project' if entity_type.lower() == 'finance' else entity_type.lower()
        
        # Use DataFetcher's S3 upload method
        result = DataFetcher.fetch_and_upload_data_to_s3(entity_uuid, normalized_type)
        
        if result.get("status") == "success":
            log.log_info(f"Successfully uploaded {entity_type} data to S3: {result.get('s3_key')}")
        else:
            log.log_error(f"Failed to upload {entity_type} data to S3: {result.get('error')}")
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        error_response = {
            "error": f"Unexpected error in S3 upload: {str(e)}",
            "status": "failed",
            "entity_id": entity_id,
            "entity_type": entity_type
        }
        log.log_error(f"Unexpected error in fetch_and_upload_to_s3: {str(e)}")
        return json.dumps(error_response, indent=2)


# Instantiate S3 reader tool for use by agents
s3_reader_tool = S3DataReaderTool()
