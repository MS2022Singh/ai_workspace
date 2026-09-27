
from enum import IntEnum

class PermissionLevel(IntEnum):
    READ = 0
    LOW_RISK = 1
    CONTROLLED_MOD = 2
    HIGH_RISK = 3

class PermissionEngine:
    def __init__(self):
        self.default_level = PermissionLevel.LOW_RISK

    def verify_permission(self, required_level: PermissionLevel, granted_level: PermissionLevel) -> bool:
        allowed = granted_level >= required_level
        if not allowed:
            print(f'[Permission Engine] Access DENIED. Required: {required_level.name}, Granted: {granted_level.name}')
        return allowed

permission_engine = PermissionEngine()
