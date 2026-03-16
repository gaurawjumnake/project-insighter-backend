import os
from uuid import UUID
from pathlib import Path
from typing import Dict, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dotenv import load_dotenv
from backend.doc_insighter.core.insight_agents import ProjectScopeCrew
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

load_dotenv()

PROJECT_DOCUMENT_DIR_ENV = os.getenv("PROJECT_DOCUMENT_DIR")
if not PROJECT_DOCUMENT_DIR_ENV:
    raise ValueError("PROJECT_DOCUMENT_DIR environment variable is not set")

PROJECT_DOCUMENT_DIR = Path(PROJECT_DOCUMENT_DIR_ENV)

class InsightService:
    def __init__(self):
        pass

    def generate_team_allocation(self, project_id: UUID, db: Session) -> Dict[str, str]:
        """
        Locates SOW and WSR files in the project directory based on filename keywords
        and runs the Agentic Workflow.
        """
        try:
            # 1. Construct the specific project directory path
            project_dir = PROJECT_DOCUMENT_DIR / str(project_id)

            # 2. Validate directory exists
            if not project_dir.exists() or not project_dir.is_dir():
                raise HTTPException(
                    status_code=404, 
                    detail=f"Project directory not found at: {project_dir}. Has any document been uploaded?"
                )

            # 3. Find files dynamically
            sow_path, wsr_path = self._find_project_files(project_dir)

            # 4. Validate files found
            if not sow_path:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No file containing 'sow' found in {project_dir}"
                )
            
            if not wsr_path:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No file containing 'wsr' found in {project_dir}"
                )

            log.log_info(f"Starting analysis for Project {project_id}")
            log.log_info(f"Identified SOW: {sow_path.name}")
            log.log_info(f"Identified WSR: {wsr_path.name}")

            # 5. Execute AI Agents
            crew = ProjectScopeCrew()
            result_json = crew.run(sow_path=str(sow_path), wsr_path=str(wsr_path))

            return result_json

        except HTTPException as he:
            raise he
        except Exception as e:
            log.log_error(f"Error in InsightService: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")

    def _find_project_files(self, project_dir: Path) -> Tuple[Optional[Path], Optional[Path]]:
        """
        Scans the directory for files containing 'sow' and 'wsr' (case-insensitive).
        Returns the full paths.
        """
        sow_file = None
        wsr_file = None

        # Get all files in directory (ignore subdirectories)
        try:
            files_in_dir = [f for f in os.listdir(project_dir) if os.path.isfile(project_dir / f)]
        except Exception as e:
            log.log_error(f"Error reading directory {project_dir}: {e}")
            return None, None

        for filename in files_in_dir:
            fname_lower = filename.lower()
            
            if not sow_file and "sow" in fname_lower:
                sow_file = project_dir / filename
            
            if not wsr_file and "wsr" in fname_lower:
                wsr_file = project_dir / filename

            if sow_file and wsr_file:
                break
        
        return sow_file, wsr_file

# Factory
def get_insight_service():
    return InsightService()