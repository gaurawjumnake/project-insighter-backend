from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import UUID
import uuid

from backend.app.models.account_dashboard import AccountDashboard
from backend.app.schemas.account_dashboard import (
    AccountDashboardCreate,
    AccountDashboardUpdate
)
from backend.app.models.stakeholder_details import StakeholderDetails
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

# List of fields that belong to the stakeholder table
STAKEHOLDER_KEYS =[
    "executive_sponsor", "technical_decision_maker", "influencers",
    "neutral_stakeholders", "negative_stakeholder", "succession_risk",
    "key_competitors", "our_positioning_vs_competition", "incumbency_strength",
    "areas_competition_stronger", "white_spaces_we_own", 
    "account_review_cadence_frequency", "qbr_happening", "technical_audit_frequency"
]

class AccountDashboardService:
    """Service class for AccountDashboard CRUD operations."""

    @staticmethod
    def _sanitize_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Converts empty strings to None for database cleanliness."""
        return {k: (None if isinstance(v, str) and v.strip() == "" else v) for k, v in data.items()}

    @staticmethod
    def create(db: Session, account_data: AccountDashboardCreate) -> AccountDashboard:
        log.log_info("Service: creating account and stakeholder entry from combined payload")
        
        try:
            raw_data = account_data.model_dump()
            
            # 1. Extract Stakeholder data out of the giant payload
            stakeholder_dict = {k: raw_data.pop(k) for k in STAKEHOLDER_KEYS if k in raw_data}
            
            # 2. Prepare & Create Account
            account_dict = AccountDashboardService._sanitize_data(raw_data)
            account_dict["account_id"] = uuid.uuid4()
            
            db_account = AccountDashboard(**account_dict)
            db.add(db_account)
            db.flush() # Locks in the ID without committing

            # 3. Prepare & Create Stakeholder
            stk_dict = AccountDashboardService._sanitize_data(stakeholder_dict)
            stk_dict["account_id"] = db_account.account_id
            stk_dict["account_name"] = db_account.account_name
            
            db_stakeholder = StakeholderDetails(**stk_dict)
            db.add(db_stakeholder)

            # 4. Commit both at once
            db.commit()
            db.refresh(db_account)
            return db_account

        except Exception as e:
            db.rollback()
            log.log_error(f"Service: failed to create | error={e}")
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
    def update(db: Session, account_id: UUID, account_data: AccountDashboardUpdate) -> Optional[AccountDashboard]:
        db_account = db.query(AccountDashboard).filter(AccountDashboard.account_id == account_id).first()
        db_stakeholder = db.query(StakeholderDetails).filter(StakeholderDetails.account_id == account_id).first()

        if not db_account:
            return None

        try:
            raw_update_data = account_data.model_dump(exclude_unset=True)
            
            # 1. Extract Stakeholder updates
            stakeholder_update = {k: raw_update_data.pop(k) for k in STAKEHOLDER_KEYS if k in raw_update_data}
            
            # 2. Apply Account Updates
            if raw_update_data:
                account_update_sanitized = AccountDashboardService._sanitize_data(raw_update_data)
                for field, value in account_update_sanitized.items():
                    setattr(db_account, field, value)

            # 3. Apply Stakeholder Updates
            if stakeholder_update and db_stakeholder:
                stk_update_sanitized = AccountDashboardService._sanitize_data(stakeholder_update)
                # Keep account_name synced if it was changed
                if "account_name" in raw_update_data:
                    stk_update_sanitized["account_name"] = raw_update_data["account_name"]
                
                for field, value in stk_update_sanitized.items():
                    setattr(db_stakeholder, field, value)

            db.commit()
            db.refresh(db_account)
            return db_account

        except Exception as e:
            db.rollback()
            raise
            
    # get_by_id, get_all, and delete remain exactly the same..

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

    