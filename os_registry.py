from permissions import PermissionEngine
from computer_control import ComputerControlLayer
from cognitive_engine import CognitiveEngine
from self_upgradation import SelfUpgradationEngine

class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: str, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: dict):
        results = []
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                results.append(callback(data))
        return results

class WorkspaceOSEngine:
    def __init__(self):
        self.event_bus = EventBus()
        self.permissions = PermissionEngine()
        self.computer_control = ComputerControlLayer()
        self.cognitive_engine = CognitiveEngine()
        self.upgrader = SelfUpgradationEngine()
        
        self.state = 'INITIALIZING'
        
        self.event_bus.subscribe('SYSTEM_BOOT', self._handle_boot)
        self.event_bus.subscribe('TASK_CREATED', self._handle_task_creation)

    def _handle_boot(self, device_data: dict):
        self.state = 'LOADING_UI_REPOSITORIES'
        
        # Auto-incorporate UI interactive designing repos so they are active immediately
        self.upgrader.register_tool('interactive_ui_engine', ['render_dynamic_components', 'apply_fluid_animations'])
        self.upgrader.register_tool('data_visualization', ['render_live_graphs'])
        
        self.state = 'IDLE'
        return {
            'status': 'Boot Complete', 
            'device_registry': device_data,
            'active_background_modules': list(self.upgrader.installed_tools.keys())
        }

    def _handle_task_creation(self, payload: dict):
        self.state = 'PLANNING'
        return {'status': 'Task Logged'}

    def execute_central_task(self, task_type: str, payload: dict, user_level: int = 1):
        self.event_bus.publish('TASK_CREATED', {'type': task_type, 'payload': payload})
        self.state = 'EXECUTING'
        
        result = {'status': 'error', 'message': 'Unknown task type'}
        
        if task_type == 'learn_skill':
            result = self.cognitive_engine.build_skill_mastery_path(payload.get('skill', 'Unknown'))
        elif task_type == 'upgrade_tool':
            repo = payload.get('repo')
            analysis = self.upgrader.analyze_repository(repo)
            if analysis['status'] == 'success':
                result = self.upgrader.sandbox_install(analysis['repo_name'])
        elif task_type == 'inspect_system':
            result = self.computer_control.inspect_system(user_level)
        elif task_type == 'eliminate_block':
            result = self.cognitive_engine.eliminate_mental_block(payload.get('block', ''))
            
        self.state = 'IDLE'
        return result
