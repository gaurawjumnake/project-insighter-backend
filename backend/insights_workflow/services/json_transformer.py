"""
JSON Transformer for Finance Insights

Converts raw database objects and aggregated data into stable JSON structures
for S3 staging and crew analysis.

Handles:
1. Transformation to S3-ready JSON
2. Warning generation for missing/partial data
3. Schema validation
4. Timestamp management
"""

import json
from typing import Dict, Any, List, Tuple
from datetime import datetime
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()


class JsonTransformer:
    """Transforms finance data to S3-ready JSON with warnings."""
    
    # S3 filename format
    S3_FILENAME_TEMPLATE = "temp/{entity_type}_{entity_id}_{timestamp}.json"
    
    @staticmethod
    def generate_s3_filename(entity_type: str, entity_id: str) -> str:
        """
        Generate S3 filename with timestamp.
        
        Format: temp/project_<id>_<date>.json or temp/account_<id>_<date>.json
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"temp/{entity_type}_{entity_id}_{timestamp}.json"
    
    @staticmethod
    def transform_data_for_s3(
        entity_data: Dict[str, Any],
        warnings: List[str]
    ) -> Tuple[Dict[str, Any], str]:
        """
        Transform aggregated entity data to S3-ready JSON format.
        
        Args:
            entity_data: Raw aggregated data from FinanceAggregationService
            warnings: List of warnings from aggregation
        
        Returns:
            Tuple of (s3_json_dict, s3_filename)
        """
        entity_type = entity_data.get("entity_type", "unknown")
        entity_id = entity_data.get("entity_id", "unknown")
        
        # Generate filename
        s3_filename = JsonTransformer.generate_s3_filename(entity_type, entity_id)
        
        # Build S3 payload with metadata
        s3_payload = {
            # Metadata for crew reference
            "metadata": {
                "entity_type": entity_type,
                "entity_id": entity_id,
                "entity_name": entity_data.get("entity_name", "Unknown"),
                "hierarchy_level": entity_data.get("hierarchy_level", entity_type),
                "generated_at": entity_data.get("generated_at", datetime.utcnow().isoformat()),
                "s3_filename": s3_filename
            },
            
            # Warnings for processing
            "data_quality": {
                "has_warnings": len(warnings) > 0,
                "warnings": warnings,
                "warning_count": len(warnings)
            },
            
            # Full entity data
            "entity_data": entity_data,
            
            # Processing hints for crew
            "processing_hints": JsonTransformer._generate_processing_hints(entity_data, warnings),
            
            # Timestamp
            "payload_created_at": datetime.utcnow().isoformat()
        }
        
        return s3_payload, s3_filename
    
    @staticmethod
    def _generate_processing_hints(entity_data: Dict[str, Any], warnings: List[str]) -> Dict[str, Any]:
        """
        Generate processing hints for the crew based on data quality.
        
        Tells the crew what to expect and how to handle partial data.
        """
        entity_type = entity_data.get("entity_type", "unknown")
        hints = {
            "partial_data": len(warnings) > 0,
            "entity_type": entity_type,
            "analysis_focus": [],
            "data_availability": {}
        }
        
        if entity_type == "project":
            hints["analysis_focus"] = [
                "profitability_analysis",
                "revenue_variance",
                "cost_efficiency",
                "financial_risks"
            ]
            
            financials = entity_data.get("financials", {})
            hints["data_availability"] = {
                "revenue_data": financials.get("revenue_records_count", 0) > 0,
                "documents": entity_data.get("documents", {}).get("has_documents", False),
                "variance_available": True
            }
        
        elif entity_type == "account":
            hints["analysis_focus"] = [
                "portfolio_assessment",
                "shortfall_analysis",
                "project_aggregation",
                "revenue_optimization"
            ]
            
            hints["data_availability"] = {
                "projects": entity_data.get("projects", {}).get("total_count", 0) > 0,
                "project_insights": entity_data.get("projects", {}).get("with_insights_count", 0) > 0,
                "financial_targets": entity_data.get("data_quality", {}).get("has_target_revenue", False),
                "shortfall_analysis": True
            }
        
        elif entity_type == "private_equity":
            hints["analysis_focus"] = [
                "portfolio_alignment",
                "account_aggregation",
                "capability_assessment",
                "investment_opportunity"
            ]
            
            hints["data_availability"] = {
                "accounts": entity_data.get("accounts", {}).get("total_count", 0) > 0,
                "account_insights": entity_data.get("accounts", {}).get("with_insights_count", 0) > 0,
                "documents": entity_data.get("documents", {}).get("total_count", 0) > 0,
                "company_capabilities": entity_data.get("data_quality", {}).get("has_company_capabilities", False)
            }
        
        return hints
    
    @staticmethod
    def validate_s3_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate S3 payload structure.
        
        Returns:
            Tuple of (is_valid, error_list)
        """
        errors = []
        
        # Check required top-level keys
        required_keys = ["metadata", "data_quality", "entity_data"]
        for key in required_keys:
            if key not in payload:
                errors.append(f"Missing required key: {key}")
        
        # Check metadata
        metadata = payload.get("metadata", {})
        required_meta = ["entity_type", "entity_id", "entity_name"]
        for key in required_meta:
            if key not in metadata:
                errors.append(f"Missing required metadata key: {key}")
        
        # Check entity_data
        entity_data = payload.get("entity_data", {})
        if "entity_type" not in entity_data:
            errors.append("Missing entity_type in entity_data")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def add_warnings_to_payload(payload: Dict[str, Any], new_warnings: List[str]) -> Dict[str, Any]:
        """Add additional warnings to existing payload."""
        if "data_quality" not in payload:
            payload["data_quality"] = {}
        
        existing_warnings = payload["data_quality"].get("warnings", [])
        all_warnings = existing_warnings + new_warnings
        
        payload["data_quality"]["warnings"] = all_warnings
        payload["data_quality"]["warning_count"] = len(all_warnings)
        payload["data_quality"]["has_warnings"] = len(all_warnings) > 0
        
        return payload
