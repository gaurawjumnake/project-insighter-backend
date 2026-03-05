from uuid import UUID
from backend.app.core.config import settings

def get_current_user_id() -> UUID:
    """
    Returns the hardcoded System User ID.
    Used for Approach A (Shared Calendar).
    """
    return UUID(settings.SYSTEM_USER_ID)