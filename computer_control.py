import os
import subprocess
import psutil
from permissions import PermissionEngine

class ComputerControlLayer:
    def __init__(self):
        self.permission_engine = PermissionEngine()

    def inspect_system(self, user_level: int = 1):
        perm = self.permission_engine.check_permission('READ', user_level)
        if not perm['allowed']:
            return {'status': 'error', 'message': perm.get('message', 'Permission denied')}
        
        return {
            'status': 'success',
            'level': 'Level 0 - Read',
            'cpu_usage': psutil.cpu_percent(interval=0.1),
            'ram_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'active_processes': len(psutil.pids())
        }

    def execute_low_risk_action(self, action_name: str, path: str = None, user_level: int = 1):
        perm = self.permission_engine.check_permission('WRITE', user_level)
        if not perm['allowed']:
            return {'status': 'error', 'message': perm.get('message', 'Permission denied')}
        
        if action_name == 'create_folder' and path:
            os.makedirs(path, exist_ok=True)
            return {'status': 'success', 'message': f'Created folder at {path}'}
        
        return {'status': 'error', 'message': 'Unknown low-risk action'}

    def execute_controlled_action(self, script_path: str, user_level: int = 1):
        perm = self.permission_engine.check_permission('EXECUTE', user_level)
        if not perm['allowed'] and perm.get('requires_approval'):
            return {'status': 'blocked', 'requires_approval': True, 'message': f'Execution of {script_path} requires explicit user approval (Level 2).'}
        
        return {'status': 'error', 'message': 'Execution blocked or unauthorized'}
