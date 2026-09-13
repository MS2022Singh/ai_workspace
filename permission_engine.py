class PermissionEngine:
    def __init__(self):
        # Action risk levels: 0=Read, 1=Low-Risk, 2=Controlled, 3=High-Risk
        self.permissions = {
            'read_file': 0,
            'open_app': 1,
            'install_package': 2,
            'delete_files': 3,
            'financial_transaction': 3
        }

    def check_permission(self, action: str, requested_level: int) -> bool:
        if action not in self.permissions:
            return False
        return requested_level >= self.permissions[action]
