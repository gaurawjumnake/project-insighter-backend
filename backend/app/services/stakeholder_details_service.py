from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError # Import this
from typing import List, Optional
from uuid import UUID

from backend.app.models.stakeholder_details import StakeholderDetails
from backend.app.schemas.stakeholder_details import (
    StakeholderDetailsCreate,
    StakeholderDetailsUpdate
)
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

class StakeholderDetailsService:
    """Service class for StakeholderDetails CRUD operations."""

    @staticmethod
    def create(db: Session, stakeholder_data: StakeholderDetailsCreate) -> StakeholderDetails:
        """Create a new stakeholder details entry."""
        log.log_info(
            f"Service: creating stakeholder details | payload={stakeholder_data.model_dump()}"
        )

        try:
            db_stakeholder = StakeholderDetails(**stakeholder_data.model_dump())
            db.add(db_stakeholder)
            db.commit()
            db.refresh(db_stakeholder)

            log.log_info(
                f"Service: stakeholder details created | id={db_stakeholder.id}"
            )
            return db_stakeholder

        except IntegrityError as e:
            # This catches cases where account_id does not exist in account_dashboard
            db.rollback()
            log.log_error(f"Service: Foreign Key violation (Account likely missing) | error={e}")
            raise ValueError("The provided Account ID does not exist.")
            
        except Exception as e:
            db.rollback()
            log.log_error(f"Service: failed to create stakeholder details | error={e}")
            raise

    @staticmethod
    def get_by_id(db: Session, stakeholder_id: UUID) -> Optional[StakeholderDetails]:
        """Get stakeholder details by ID."""
        log.log_info(f"Service: fetching stakeholder details | id={stakeholder_id}")
        return db.query(StakeholderDetails).filter(StakeholderDetails.id == stakeholder_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[StakeholderDetails]:
        """Get all stakeholder details with pagination."""
        log.log_info(f"Service: fetching all stakeholder details | skip={skip}, limit={limit}")
        return db.query(StakeholderDetails).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_account_id(db: Session, account_id: UUID) -> List[StakeholderDetails]:
        """Get all stakeholder details for a specific account."""
        log.log_info(f"Service: fetching details for account | account_id={account_id}")
        return db.query(StakeholderDetails).filter(StakeholderDetails.account_id == account_id).all()

    @staticmethod
    def update(
        db: Session,
        stakeholder_id: UUID,
        stakeholder_data: StakeholderDetailsUpdate
    ) -> Optional[StakeholderDetails]:
        """Update existing stakeholder details."""
        log.log_info(
            f"Service: updating details | id={stakeholder_id}, payload={stakeholder_data.model_dump(exclude_unset=True)}"
        )

        db_stakeholder = db.query(StakeholderDetails).filter(StakeholderDetails.id == stakeholder_id).first()

        if not db_stakeholder:
            log.log_warning(f"Service: details not found for update | id={stakeholder_id}")
            return None

        try:
            update_data = stakeholder_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_stakeholder, field, value)

            db.commit()
            db.refresh(db_stakeholder)
            return db_stakeholder

        except Exception as e:
            db.rollback()
            log.log_error(f"Service: failed to update details | error={e}")
            raise

    @staticmethod
    def delete(db: Session, stakeholder_id: UUID) -> bool:
        """Delete stakeholder details."""
        log.log_info(f"Service: deleting details | id={stakeholder_id}")

        db_stakeholder = db.query(StakeholderDetails).filter(StakeholderDetails.id == stakeholder_id).first()

        if not db_stakeholder:
            log.log_warning(f"Service: details not found for deletion | id={stakeholder_id}")
            return False

        try:
            db.delete(db_stakeholder)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            log.log_error(f"Service: failed to delete details | error={e}")
            raise

    @staticmethod
    def search_by_incumbency_strength(db: Session, incumbency_strength: str) -> List[StakeholderDetails]:
        """Search stakeholder details by incumbency strength."""
        return db.query(StakeholderDetails).filter(
            StakeholderDetails.incumbency_strength == incumbency_strength
        ).all()