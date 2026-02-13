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
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()
router = APIRouter()

@router.post("/", response_model=StakeholderDetailsResponse, status_code=status.HTTP_201_CREATED)
def create_stakeholder_details(
    stakeholder_in: StakeholderDetailsCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new stakeholder details entry.
    """
    # Fix: Use model_dump() instead of dict()
    log.log_info(
        f"API: creating stakeholder details | payload={stakeholder_in.model_dump()}"
    )

    try:
        details = StakeholderDetailsService.create(
            db=db,
            stakeholder_data=stakeholder_in
        )
        log.log_info(
            f"API: stakeholder details created successfully | id={details.id}"
        )
        return details

    except ValueError as e:
        # Catch the "Account ID not found" error explicitly
        log.log_warning(f"API: validation error | error={e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    except Exception as e:
        log.log_error(f"API: failed to create stakeholder details | error={e}")
        # Allow FastAPI to handle the 500 error, or raise explicitly
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{stakeholder_id}", response_model=StakeholderDetailsResponse)
def read_stakeholder_details(
    stakeholder_id: UUID,
    db: Session = Depends(get_db)
):
    log.log_info(f"API: fetching stakeholder details | id={stakeholder_id}")
    details = StakeholderDetailsService.get_by_id(db=db, stakeholder_id=stakeholder_id)

    if not details:
        log.log_warning(f"API: details not found | id={stakeholder_id}")
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
    log.log_info(f"API: fetching all details | skip={skip}, limit={limit}")
    return StakeholderDetailsService.get_all(db=db, skip=skip, limit=limit)

@router.get("/account/{account_id}", response_model=List[StakeholderDetailsResponse])
def read_stakeholder_details_by_account(
    account_id: UUID,
    db: Session = Depends(get_db)
):
    log.log_info(f"API: fetching details by account | account_id={account_id}")
    return StakeholderDetailsService.get_by_account_id(db=db, account_id=account_id)

@router.put("/{stakeholder_id}", response_model=StakeholderDetailsResponse)
def update_stakeholder_details(
    stakeholder_id: UUID,
    stakeholder_in: StakeholderDetailsUpdate,
    db: Session = Depends(get_db)
):
    # Fix: Use model_dump(exclude_unset=True)
    log.log_info(
        f"API: updating details | id={stakeholder_id}, payload={stakeholder_in.model_dump(exclude_unset=True)}"
    )

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
    log.log_info(f"API: deleting details | id={stakeholder_id}")
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
    log.log_info(f"API: searching by incumbency | strength={strength}")
    return StakeholderDetailsService.search_by_incumbency_strength(db=db, incumbency_strength=strength)