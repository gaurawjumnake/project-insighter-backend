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
    log.log_info(
        f"API: creating stakeholder details | payload={stakeholder_in.dict()}"
    )

    try:
        details = StakeholderDetailsService.create(
            db=db,
            stakeholder_data=stakeholder_in
        )
        log.log_info(
            f"API: stakeholder details created successfully | stakeholder_id={details.id}"
        )
        return details

    except Exception as e:
        log.log_error(
            f"API: failed to create stakeholder details | error={e}"
        )
        raise


@router.get("/{stakeholder_id}", response_model=StakeholderDetailsResponse)
def read_stakeholder_details(
    stakeholder_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get specific stakeholder details by ID.
    """
    log.log_info(
        f"API: fetching stakeholder details | stakeholder_id={stakeholder_id}"
    )

    details = StakeholderDetailsService.get_by_id(
        db=db,
        stakeholder_id=stakeholder_id
    )

    if not details:
        log.log_warning(
            f"API: stakeholder details not found | stakeholder_id={stakeholder_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stakeholder details not found"
        )

    log.log_info(
        f"API: stakeholder details retrieved | stakeholder_id={stakeholder_id}"
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
    log.log_info(
        f"API: fetching all stakeholder details | skip={skip}, limit={limit}"
    )

    details_list = StakeholderDetailsService.get_all(
        db=db,
        skip=skip,
        limit=limit
    )

    log.log_info(
        f"API: stakeholder details retrieved | count={len(details_list)}"
    )
    return details_list


@router.get("/account/{account_id}", response_model=List[StakeholderDetailsResponse])
def read_stakeholder_details_by_account(
    account_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get all stakeholder details linked to a specific Account ID.
    """
    log.log_info(
        f"API: fetching stakeholder details by account | account_id={account_id}"
    )

    details_list = StakeholderDetailsService.get_by_account_id(
        db=db,
        account_id=account_id
    )

    log.log_info(
        f"API: stakeholder details retrieved for account | "
        f"account_id={account_id}, count={len(details_list)}"
    )
    return details_list


@router.put("/{stakeholder_id}", response_model=StakeholderDetailsResponse)
def update_stakeholder_details(
    stakeholder_id: UUID,
    stakeholder_in: StakeholderDetailsUpdate,
    db: Session = Depends(get_db)
):
    """
    Update stakeholder details.
    """
    log.log_info(
        f"API: updating stakeholder details | "
        f"stakeholder_id={stakeholder_id}, payload={stakeholder_in.dict(exclude_unset=True)}"
    )

    details = StakeholderDetailsService.update(
        db=db,
        stakeholder_id=stakeholder_id,
        stakeholder_data=stakeholder_in
    )

    if not details:
        log.log_warning(
            f"API: stakeholder details not found for update | stakeholder_id={stakeholder_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stakeholder details not found"
        )

    log.log_info(
        f"API: stakeholder details updated successfully | stakeholder_id={stakeholder_id}"
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
    log.log_info(
        f"API: deleting stakeholder details | stakeholder_id={stakeholder_id}"
    )

    success = StakeholderDetailsService.delete(
        db=db,
        stakeholder_id=stakeholder_id
    )

    if not success:
        log.log_warning(
            f"API: stakeholder details not found for deletion | stakeholder_id={stakeholder_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stakeholder details not found"
        )

    log.log_info(
        f"API: stakeholder details deleted successfully | stakeholder_id={stakeholder_id}"
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
    log.log_info(
        f"API: searching stakeholder details by incumbency strength | strength={strength}"
    )

    details_list = StakeholderDetailsService.search_by_incumbency_strength(
        db=db,
        incumbency_strength=strength
    )

    log.log_info(
        f"API: incumbency strength search completed | "
        f"strength={strength}, count={len(details_list)}"
    )
    return details_list