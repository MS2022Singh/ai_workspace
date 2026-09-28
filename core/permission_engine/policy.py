class PermissionEngine:
    PERMISSIONS = ["READ", "WRITE", "EXECUTE", "NETWORK", "DELETE", "SYSTEM", "FINANCIAL"]

    def __init__(self, autonomy_level: int = 1):
        self.autonomy_level = autonomy_level  # 1: Observe, 2: Suggest, 3: Execute w/ approval, 4: Autonomous
        self.active_permissions = {p: (p in ["READ", "WRITE", "NETWORK"]) for p in self.PERMISSIONS}

    def check_permission(self, perm: str) -> bool:
        return self.active_permissions.get(perm.upper(), False)

    def update_policy(self, autonomy_level: int, permissions: dict):
        self.autonomy_level = autonomy_level
        for k, v in permissions.items():
            if k.upper() in self.PERMISSIONS:
                self.active_permissions[k.upper()] = bool(v)

permission_engine = PermissionEngine()
