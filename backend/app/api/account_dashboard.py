from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from backend.app.db.session import get_db
from backend.app.schemas.account_dashboard import (
    AccountDashboardCreate,
    AccountDashboardUpdate,
    AccountDashboardResponse
)
from backend.app.services.account_dashboard_service import AccountDashboardService
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()
router = APIRouter()

@router.post("/", response_model=AccountDashboardResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_in: AccountDashboardCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new account dashboard entry.
    """
    log.log_info(
        f"API: creating account dashboard entry | payload={account_in.model_dump()}"
    )

    try:
        account = AccountDashboardService.create(db=db, account_data=account_in)
        log.log_info(
            f"API: account dashboard created successfully | account_id={account.account_id}"
        )
        return account

    except Exception as e:
        log.log_error(f"API: failed to create account dashboard | error={e}")
        # Re-raise so FastAPI returns 500 or handles it globally
        raise

@router.get("/{account_id}", response_model=AccountDashboardResponse)
def read_account(
    account_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a specific account by ID.
    """
    log.log_info(f"API: fetching account dashboard | account_id={account_id}")

    account = AccountDashboardService.get_by_id(db=db, account_id=account_id)
    if not account:
        log.log_warning(f"API: account dashboard not found | account_id={account_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    log.log_info(f"API: account dashboard retrieved | account_id={account_id}")
    return account

@router.get("/", response_model=List[AccountDashboardResponse])
def read_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all accounts with pagination.
    """
    log.log_info(f"API: fetching account dashboards | skip={skip}, limit={limit}")

    accounts = AccountDashboardService.get_all(db=db, skip=skip, limit=limit)

    log.log_info(f"API: account dashboards retrieved | count={len(accounts)}")
    return accounts

@router.put("/{account_id}", response_model=AccountDashboardResponse)
def update_account(
    account_id: UUID,
    account_in: AccountDashboardUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an account.
    """
    # Use model_dump(exclude_unset=True) to only log what is actually being changed
    log.log_info(
        f"API: updating account dashboard | "
        f"account_id={account_id}, payload={account_in.model_dump(exclude_unset=True)}"
    )

    account = AccountDashboardService.update(
        db=db,
        account_id=account_id,
        account_data=account_in
    )

    if not account:
        log.log_warning(f"API: account dashboard not found for update | account_id={account_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    log.log_info(f"API: account dashboard updated successfully | account_id={account_id}")
    return account

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Delete an account.
    """
    log.log_info(f"API: deleting account dashboard | account_id={account_id}")

    success = AccountDashboardService.delete(db=db, account_id=account_id)
    if not success:
        log.log_warning(f"API: account dashboard not found for deletion | account_id={account_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    log.log_info(f"API: account dashboard deleted successfully | account_id={account_id}")
    return None