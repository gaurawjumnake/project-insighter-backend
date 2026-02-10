from sqlalchemy.orm import Session
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
    def create(
        db: Session,
        stakeholder_data: StakeholderDetailsCreate
    ) -> StakeholderDetails:
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
                f"Service: stakeholder details created | stakeholder_id={db_stakeholder.id}"
            )
            return db_stakeholder

        except Exception as e:
            db.rollback()
            log.log_error(
                f"Service: failed to create stakeholder details | error={e}"
            )
            raise

    @staticmethod
    def get_by_id(
        db: Session,
        stakeholder_id: UUID
    ) -> Optional[StakeholderDetails]:
        """Get stakeholder details by ID."""
        log.log_info(
            f"Service: fetching stakeholder details by id | stakeholder_id={stakeholder_id}"
        )

        stakeholder = (
            db.query(StakeholderDetails)
            .filter(StakeholderDetails.id == stakeholder_id)
            .first()
        )

        if not stakeholder:
            log.log_warning(
                f"Service: stakeholder details not found | stakeholder_id={stakeholder_id}"
            )

        return stakeholder

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[StakeholderDetails]:
        """Get all stakeholder details with pagination."""
        log.log_info(
            f"Service: fetching all stakeholder details | skip={skip}, limit={limit}"
        )

        results = db.query(StakeholderDetails).offset(skip).limit(limit).all()

        log.log_info(
            f"Service: stakeholder details fetched | count={len(results)}"
        )
        return results

    @staticmethod
    def get_by_account_id(
        db: Session,
        account_id: UUID
    ) -> List[StakeholderDetails]:
        """Get all stakeholder details for a specific account."""
        log.log_info(
            f"Service: fetching stakeholder details by account | account_id={account_id}"
        )

        results = (
            db.query(StakeholderDetails)
            .filter(StakeholderDetails.account_id == account_id)
            .all()
        )

        log.log_info(
            f"Service: stakeholder details fetched for account | "
            f"account_id={account_id}, count={len(results)}"
        )
        return results

    @staticmethod
    def update(
        db: Session,
        stakeholder_id: UUID,
        stakeholder_data: StakeholderDetailsUpdate
    ) -> Optional[StakeholderDetails]:
        """Update existing stakeholder details."""
        log.log_info(
            f"Service: updating stakeholder details | "
            f"stakeholder_id={stakeholder_id}, payload={stakeholder_data.model_dump(exclude_unset=True)}"
        )

        db_stakeholder = (
            db.query(StakeholderDetails)
            .filter(StakeholderDetails.id == stakeholder_id)
            .first()
        )

        if not db_stakeholder:
            log.log_warning(
                f"Service: stakeholder details not found for update | stakeholder_id={stakeholder_id}"
            )
            return None

        try:
            update_data = stakeholder_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_stakeholder, field, value)

            db.commit()
            db.refresh(db_stakeholder)

            log.log_info(
                f"Service: stakeholder details updated | stakeholder_id={stakeholder_id}"
            )
            return db_stakeholder

        except Exception as e:
            db.rollback()
            log.log_error(
                f"Service: failed to update stakeholder details | error={e}"
            )
            raise

    @staticmethod
    def delete(
        db: Session,
        stakeholder_id: UUID
    ) -> bool:
        """Delete stakeholder details."""
        log.log_info(
            f"Service: deleting stakeholder details | stakeholder_id={stakeholder_id}"
        )

        db_stakeholder = (
            db.query(StakeholderDetails)
            .filter(StakeholderDetails.id == stakeholder_id)
            .first()
        )

        if not db_stakeholder:
            log.log_warning(
                f"Service: stakeholder details not found for deletion | stakeholder_id={stakeholder_id}"
            )
            return False

        try:
            db.delete(db_stakeholder)
            db.commit()

            log.log_info(
                f"Service: stakeholder details deleted | stakeholder_id={stakeholder_id}"
            )
            return True

        except Exception as e:
            db.rollback()
            log.log_error(
                f"Service: failed to delete stakeholder details | error={e}"
            )
            raise

    @staticmethod
    def search_by_incumbency_strength(
        db: Session,
        incumbency_strength: str
    ) -> List[StakeholderDetails]:
        """Search stakeholder details by incumbency strength."""
        log.log_info(
            f"Service: searching stakeholder details by incumbency strength | "
            f"incumbency_strength={incumbency_strength}"
        )

        results = (
            db.query(StakeholderDetails)
            .filter(
                StakeholderDetails.incumbency_strength == incumbency_strength
            )
            .all()
        )

        log.log_info(
            f"Service: incumbency strength search completed | "
            f"incumbency_strength={incumbency_strength}, count={len(results)}"
        )
        return results