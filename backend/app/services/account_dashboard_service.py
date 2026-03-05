from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from backend.app.models.account_dashboard import AccountDashboard
from backend.app.schemas.account_dashboard import (
    AccountDashboardCreate,
    AccountDashboardUpdate
)
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()


class AccountDashboardService:
    """Service class for AccountDashboard CRUD operations."""

    @staticmethod
    def create(db: Session, account_data: AccountDashboardCreate) -> AccountDashboard:
        """Create a new account dashboard entry."""
        log.log_info(
            f"Service: creating account dashboard | payload={account_data.model_dump()}"
        )

        try:
            db_account = AccountDashboard(**account_data.model_dump())
            db.add(db_account)
            db.commit()
            db.refresh(db_account)

            log.log_info(
                f"Service: account dashboard created | account_id={db_account.account_id}"
            )
            return db_account

        except Exception as e:
            db.rollback()
            log.log_error(
                f"Service: failed to create account dashboard | error={e}"
            )
            raise

    @staticmethod
    def get_by_id(db: Session, account_id: UUID) -> Optional[AccountDashboard]:
        """Get account dashboard by ID."""
        log.log_info(
            f"Service: fetching account dashboard by id | account_id={account_id}"
        )

        account = (
            db.query(AccountDashboard)
            .filter(AccountDashboard.account_id == account_id)
            .first()
        )

        if not account:
            log.log_warning(
                f"Service: account dashboard not found | account_id={account_id}"
            )

        return account

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[AccountDashboard]:
        """Get all account dashboards with pagination."""
        log.log_info(
            f"Service: fetching all account dashboards | skip={skip}, limit={limit}"
        )

        results = db.query(AccountDashboard).offset(skip).limit(limit).all()

        log.log_info(
            f"Service: account dashboards fetched | count={len(results)}"
        )
        return results

    @staticmethod
    def update(
        db: Session,
        account_id: UUID,
        account_data: AccountDashboardUpdate
    ) -> Optional[AccountDashboard]:
        """Update an existing account dashboard."""
        log.log_info(
            f"Service: updating account dashboard | "
            f"account_id={account_id}, payload={account_data.model_dump(exclude_unset=True)}"
        )

        db_account = (
            db.query(AccountDashboard)
            .filter(AccountDashboard.account_id == account_id)
            .first()
        )

        if not db_account:
            log.log_warning(
                f"Service: account dashboard not found for update | account_id={account_id}"
            )
            return None

        try:
            update_data = account_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_account, field, value)

            db.commit()
            db.refresh(db_account)

            log.log_info(
                f"Service: account dashboard updated | account_id={account_id}"
            )
            return db_account

        except Exception as e:
            db.rollback()
            log.log_error(
                f"Service: failed to update account dashboard | error={e}"
            )
            raise

    @staticmethod
    def delete(db: Session, account_id: UUID) -> bool:
        """Delete an account dashboard."""
        log.log_info(
            f"Service: deleting account dashboard | account_id={account_id}"
        )

        db_account = (
            db.query(AccountDashboard)
            .filter(AccountDashboard.account_id == account_id)
            .first()
        )

        if not db_account:
            log.log_warning(
                f"Service: account dashboard not found for deletion | account_id={account_id}"
            )
            return False

        try:
            db.delete(db_account)
            db.commit()

            log.log_info(
                f"Service: account dashboard deleted | account_id={account_id}"
            )
            return True

        except Exception as e:
            db.rollback()
            log.log_error(
                f"Service: failed to delete account dashboard | error={e}"
            )
            raise

    