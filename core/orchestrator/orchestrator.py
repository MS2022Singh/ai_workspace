import logging
from core.event_bus.event_bus import EventBus, SystemState
from core.permission_engine.permission_engine import PermissionEngine, PermissionClass

class MultiAgentOrchestrator:
    def __init__(self, event_bus: EventBus, permission_engine: PermissionEngine):
        self.event_bus = event_bus
        self.permission_engine = permission_engine
        self.logger = logging.getLogger("MultiAgentOrchestrator")
        self.agents = {}

    def register_agent(self, agent_name: str, expert_profile: dict):
        self.agents[agent_name] = expert_profile
        self.logger.info(f"Registered AI Expert Agent: {agent_name} with profile: {expert_profile}")

    def coordinate_task(self, task_name: str, required_permission: PermissionClass, user_authorized: bool = False):
        self.logger.info(f"Coordinating task: {task_name}")
        self.event_bus.transition_state(SystemState.PLANNING)
        
        # Validate permissions before delegation
        if not self.permission_engine.validate_action(required_permission, user_authorized):
            self.event_bus.transition_state(SystemState.APPROVAL_REQUIRED)
            self.logger.warning(f"Task '{task_name}' halted: Approval required for permission class {required_permission.value}")
            return False

        self.event_bus.transition_state(SystemState.EXECUTING)
        self.logger.info(f"Task '{task_name}' executed successfully.")
        self.event_bus.transition_state(SystemState.VERIFYING)
        self.event_bus.transition_state(SystemState.RESPONDING)
        return True
