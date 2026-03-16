from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Dict, Any
from backend.app.db.session import get_db
from backend.doc_insighter.services.insight_service import get_insight_service, InsightService
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

router = APIRouter(prefix="/insights", tags=["Project-Insights"])

@router.post("/circle-allocation/{project_id}")
async def get_circle_allocation_insights(
    project_id: UUID,
    db: Session = Depends(get_db),
    service: InsightService = Depends(get_insight_service)
) -> Dict[str, Any]:
    """
    Analyzes the *already uploaded* SOW and WSR documents.
    Returns JSON deciding circle/team involvement.
    """
    try:
        log.log_info(f"Received insight request for Project: {project_id}")
        
        result = service.generate_team_allocation(project_id, db)
        
        if not isinstance(result, dict):
             return {"result": str(result)}
             
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        log.log_error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))