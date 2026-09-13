class PermissionEngine:
    def __init__(self):
        self.permissions = {
            "READ": 0,
            "WRITE": 1,
            "EXECUTE": 2,
            "NETWORK": 1,
            "DELETE": 3,
            "SYSTEM": 3,
            "FINANCIAL": 3
        }

    def check_permission(self, action_type: str, requested_level: int) -> bool:
        required_level = self.permissions.get(action_type.upper(), 3)
        return requested_level >= required_level