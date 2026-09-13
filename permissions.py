class PermissionEngine:
    def __init__(self):
        self.levels = {
            'READ': 0,
            'WRITE': 1,
            'EXECUTE': 2,
            'NETWORK': 2,
            'DELETE': 3,
            'SYSTEM': 3,
            'FINANCIAL': 3
        }

    def check_permission(self, action_type: str, user_authorized_level: int = 1):
        action_level = self.levels.get(action_type.upper(), 3)
        if action_level <= user_authorized_level:
            return {'allowed': True, 'requires_approval': False}
        elif action_level == 2:
            return {'allowed': False, 'requires_approval': True, 'message': f'Action {action_type} requires explicit approval.'}
        else:
            return {'allowed': False, 'requires_approval': False, 'message': f'Action {action_type} is restricted or high-risk.'}
