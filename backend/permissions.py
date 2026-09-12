from enum import IntEnum
import logging
from backend.event_bus import event_bus, TOPIC_APPROVAL_REQUIRED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PermissionEngine")

class PermissionLevel(IntEnum):
    READ_ONLY = 0
    SAFE_WRITE = 1
    EXTERNAL_API = 2
    CRITICAL_SYSTEM = 3

class PermissionEngine:
    def __init__(self, auto_approve_up_to: PermissionLevel = PermissionLevel.SAFE_WRITE):
        self.auto_approve_limit = auto_approve_up_to

    def check_permission(self, action_name: str, required_level: PermissionLevel, details: dict = None) -> bool:
        details = details or {}
        logger.info(f"Permission check for '{action_name}' [Required: L{required_level.value}]")

        if required_level <= self.auto_approve_limit:
            logger.info(f"Action '{action_name}' auto-approved (L{required_level.value} <= L{self.auto_approve_limit.value})")
            return True

        logger.warning(f"Action '{action_name}' requires manual approval! Triggering event.")
        event_bus.publish(
            TOPIC_APPROVAL_REQUIRED,
            action=action_name,
            level=required_level.value,
            details=details
        )
        return False

permission_engine = PermissionEngine()