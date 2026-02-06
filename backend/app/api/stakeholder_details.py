from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from backend.app.db.session import get_db
from backend.app.schemas.stakeholder_details import (
    StakeholderDetailsCreate, 
    StakeholderDetailsUpdate, 
    StakeholderDetailsResponse
)
from backend.app.services.stakeholder_details_service import StakeholderDetailsService

router = APIRouter()

@router.post("/", response_model=StakeholderDetailsResponse, status_code=status.HTTP_201_CREATED)
def create_stakeholder_details(
    stakeholder_in: StakeholderDetailsCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new stakeholder details entry.
    """
    return StakeholderDetailsService.create(db=db, stakeholder_data=stakeholder_in)

@router.get("/{stakeholder_id}", response_model=StakeholderDetailsResponse)
def read_stakeholder_details(
    stakeholder_id: UUID, 
    db: Session = Depends(get_db)
):
    """
    Get specific stakeholder details by ID.
    """
    details = StakeholderDetailsService.get_by_id(db=db, stakeholder_id=stakeholder_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Stakeholder details not found"
        )
    return details

@router.get("/", response_model=List[StakeholderDetailsResponse])
def read_all_stakeholder_details(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Retrieve all stakeholder details with pagination.
    """
    return StakeholderDetailsService.get_all(db=db, skip=skip, limit=limit)

@router.get("/account/{account_id}", response_model=List[StakeholderDetailsResponse])
def read_stakeholder_details_by_account(
    account_id: UUID, 
    db: Session = Depends(get_db)
):
    """
    Get all stakeholder details linked to a specific Account ID.
    """
    return StakeholderDetailsService.get_by_account_id(db=db, account_id=account_id)

@router.put("/{stakeholder_id}", response_model=StakeholderDetailsResponse)
def update_stakeholder_details(
    stakeholder_id: UUID, 
    stakeholder_in: StakeholderDetailsUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update stakeholder details.
    """
    details = StakeholderDetailsService.update(
        db=db, 
        stakeholder_id=stakeholder_id, 
        stakeholder_data=stakeholder_in
    )
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Stakeholder details not found"
        )
    return details

@router.delete("/{stakeholder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stakeholder_details(
    stakeholder_id: UUID, 
    db: Session = Depends(get_db)
):
    """
    Delete stakeholder details.
    """
    success = StakeholderDetailsService.delete(db=db, stakeholder_id=stakeholder_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Stakeholder details not found"
        )
    return None

@router.get("/search/incumbency/{strength}", response_model=List[StakeholderDetailsResponse])
def search_by_incumbency(
    strength: str, 
    db: Session = Depends(get_db)
):
    """
    Search by incumbency strength (e.g., High, Medium, Low).
    """
    return StakeholderDetailsService.search_by_incumbency_strength(db=db, incumbency_strength=strength)