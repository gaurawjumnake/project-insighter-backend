# Schemas module - imports all Pydantic schemas
from backend.sales.app.schemas.account_dashboard import (
    AccountDashboardBase,
    AccountDashboardCreate,
    AccountDashboardUpdate,
    AccountDashboardResponse,
)
from backend.sales.app.schemas.stakeholder_details import (
    StakeholderDetailsBase,
    StakeholderDetailsCreate,
    StakeholderDetailsUpdate,
    StakeholderDetailsResponse,
)

__all__ = [
    # Account Dashboard schemas
    "AccountDashboardBase",
    "AccountDashboardCreate",
    "AccountDashboardUpdate",
    "AccountDashboardResponse",
    # Stakeholder Details schemas
    "StakeholderDetailsBase",
    "StakeholderDetailsCreate",
    "StakeholderDetailsUpdate",
    "StakeholderDetailsResponse",
]
