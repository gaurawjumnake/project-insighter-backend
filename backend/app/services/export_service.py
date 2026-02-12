from sqlalchemy.orm import Session, contains_eager
from typing import List, Optional
from uuid import UUID

from backend.app.models.account_dashboard import AccountDashboard
from backend.app.models.stakeholder_details import StakeholderDetails
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

def get_account_dashboards(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    account_id: Optional[UUID] = None
) -> List[AccountDashboard]:
    """
    Retrieve account dashboard data for export.
    """

    query = db.query(AccountDashboard)

    if account_id:
        query = query.filter(AccountDashboard.account_id == account_id)

    result = (
        query
        .order_by(AccountDashboard.account_name)
        .offset(skip)
        .limit(limit)
        .all()
    )

    log.log_info(
        f"Account dashboard data exported successfully | count={len(result)}"
    )
    return result

def get_stakeholder_details(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    account_id: Optional[UUID] = None
) -> List[StakeholderDetails]:
    """
    Retrieve stakeholder details data for export.
    """

    query = db.query(StakeholderDetails)

    if account_id:
        query = query.filter(StakeholderDetails.account_id == account_id)

    result = (
        query
        .order_by(StakeholderDetails.account_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    log.log_info(
        f"Stakeholder details data exported successfully | count={len(result)}"
    )
    return result
