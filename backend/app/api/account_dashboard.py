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

router = APIRouter()

@router.post("/", response_model=AccountDashboardResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_in: AccountDashboardCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new account dashboard entry.
    """
    return AccountDashboardService.create(db=db, account_data=account_in)

@router.get("/{account_id}", response_model=AccountDashboardResponse)
def read_account(
    account_id: UUID, 
    db: Session = Depends(get_db)
):
    """
    Get a specific account by ID.
    """
    account = AccountDashboardService.get_by_id(db=db, account_id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Account not found"
        )
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
    return AccountDashboardService.get_all(db=db, skip=skip, limit=limit)

@router.put("/{account_id}", response_model=AccountDashboardResponse)
def update_account(
    account_id: UUID, 
    account_in: AccountDashboardUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an account.
    """
    account = AccountDashboardService.update(
        db=db, 
        account_id=account_id, 
        account_data=account_in
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Account not found"
        )
    return account

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: UUID, 
    db: Session = Depends(get_db)
):
    """
    Delete an account.
    """
    success = AccountDashboardService.delete(db=db, account_id=account_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Account not found"
        )
    return None

@router.get("/search/unit/{delivery_unit}", response_model=List[AccountDashboardResponse])
def search_accounts_by_unit(
    delivery_unit: str, 
    db: Session = Depends(get_db)
):
    """
    Search accounts belonging to a specific Delivery Unit.
    """
    return AccountDashboardService.search_by_delivery_unit(db=db, delivery_unit=delivery_unit)