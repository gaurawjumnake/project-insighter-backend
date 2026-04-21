from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Union
import json
from pathlib import Path
from backend.utitlites.s3_storage import download_data_from_s3, download_data_to_local
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()


# 1. Define Input Schema
class S3DataReaderInput(BaseModel):
    s3_key: str = Field(..., description="The S3 key of the JSON file to download and read (e.g., 'temp/account_<id>_<date>.json')")
    return_as: str = Field(
        default="dict",
        description="Return format: 'dict' for parsed JSON, 'json' for JSON string, or 'local_path' to download locally"
    )


# 2. Define the Tool
class S3DataReaderTool(BaseTool):
    name: str = "S3 Data Reader"
    description: str = (
        "Download and read JSON data from S3. "
        "Use this tool to access DB-fetched data (metrics and insights) that have been uploaded to S3. "
        "Supports reading account and project data with entity-aware file naming. "
        "Returns parsed JSON data that can be directly used for analysis."
    )
    args_schema: Type[BaseModel] = S3DataReaderInput

    def _run(
        self,
        s3_key: str,
        return_as: str = "dict"
    ) -> Union[dict, str]:
        """
        Download and read JSON data from S3.
        
        Args:
            s3_key: S3 key to download
            return_as: Format to return data in ('dict', 'json', or 'local_path')
        
        Returns:
            Parsed data or file path depending on return_as parameter
        """
        try:
            log.log_info(f"S3DataReaderTool: Downloading from S3 key: {s3_key}")
            
            if return_as == "local_path":
                # Download to local filesystem
                local_path = download_data_to_local(s3_key)
                log.log_info(f"S3DataReaderTool: File downloaded to: {local_path}")
                return str(local_path)
            
            elif return_as == "json":
                # Return as JSON string
                data = download_data_from_s3(s3_key)
                json_str = json.dumps(data, indent=2, default=str)
                log.log_info(f"S3DataReaderTool: Successfully retrieved JSON data from S3")
                return json_str
            
            else:  # return_as == "dict" (default)
                # Return as parsed dictionary
                data = download_data_from_s3(s3_key)
                log.log_info(f"S3DataReaderTool: Successfully retrieved data from S3")
                
                # Extract entity info from S3 key
                filename = Path(s3_key).name
                if filename.startswith("account_"):
                    entity_type = "account"
                elif filename.startswith("project_"):
                    entity_type = "project"
                else:
                    entity_type = "unknown"
                
                # Add metadata for agent
                data["_metadata"] = {
                    "s3_key": s3_key,
                    "filename": filename,
                    "entity_type": entity_type,
                    "source": "S3"
                }
                
                return data
        
        except Exception as e:
            error_msg = f"Error reading data from S3: {str(e)}"
            log.log_error(error_msg)
            return {
                "status": "error",
                "error": error_msg,
                "s3_key": s3_key
            }
