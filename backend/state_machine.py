from enum import Enum
import logging
from backend.event_bus import event_bus, TOPIC_USER_SPOKE, TOPIC_INTENT_DETECTED, TOPIC_APPROVAL_REQUIRED, TOPIC_TASK_COMPLETED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StateMachine")

class SystemState(str, Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    PROCESSING = "PROCESSING"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    EXECUTING = "EXECUTING"
    RESPONDING = "RESPONDING"
    ERROR = "ERROR"

class StateMachine:
    def __init__(self):
        self.current_state = SystemState.IDLE
        self._setup_event_listeners()

    def transition_to(self, new_state: SystemState, reason: str = ""):
        old_state = self.current_state
        self.current_state = new_state
        logger.info(f"State Transition: {old_state.value} -> {new_state.value} | Reason: {reason}")
        event_bus.publish("system.state_changed", old_state=old_state.value, new_state=new_state.value, reason=reason)

    def _setup_event_listeners(self):
        event_bus.subscribe(TOPIC_USER_SPOKE, self._on_user_spoke)
        event_bus.subscribe(TOPIC_INTENT_DETECTED, self._on_intent_detected)
        event_bus.subscribe(TOPIC_APPROVAL_REQUIRED, self._on_approval_required)
        event_bus.subscribe(TOPIC_TASK_COMPLETED, self._on_task_completed)

    def _on_user_spoke(self, text: str = ""):
        self.transition_to(SystemState.PROCESSING, f"User input received: {text[:20]}...")

    def _on_intent_detected(self, intent: str = "", **kwargs):
        self.transition_to(SystemState.EXECUTING, f"Intent: {intent}")

    def _on_approval_required(self, action: str = "", level: int = 0, details: dict = None):
        self.transition_to(SystemState.AWAITING_APPROVAL, f"Approval required for Level {level} action: {action}")

    def _on_task_completed(self, result: str = "", **kwargs):
        self.transition_to(SystemState.RESPONDING, "Task execution finished")

state_machine = StateMachine()