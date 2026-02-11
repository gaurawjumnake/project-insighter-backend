# backend/app/api/export.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from backend.app.db.session import get_db
from backend.app.models.account_dashboard import AccountDashboard
from backend.app.models.stakeholder_details import StakeholderDetails
from backend.app.services.export_service import (
    get_account_dashboards,
    get_stakeholder_details,
)
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()
router = APIRouter(prefix="/export", tags=["Export"])

@router.get(
    "/account-dashboard",
    response_model=List[AccountDashboard]
)
def export_account_dashboard(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    account_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Export account dashboard data.
    """
    log.log_info(
        f"API: exporting account dashboard | skip={skip}, limit={limit}, account_id={account_id}"
    )

    return get_account_dashboards(
        db=db,
        skip=skip,
        limit=limit,
        account_id=account_id,
    )
@router.get(
    "/stakeholder-details",
    response_model=List[StakeholderDetails]
)
def export_stakeholder_details(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    account_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Export stakeholder details data.
    """
    log.log_info(
        f"API: exporting stakeholder details | skip={skip}, limit={limit}, account_id={account_id}"
    )

    return get_stakeholder_details(
        db=db,
        skip=skip,
        limit=limit,
        account_id=account_id,
    )