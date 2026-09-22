import threading
import logging
from enum import Enum

class SystemState(Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    UNDERSTANDING = "UNDERSTANDING"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    VERIFYING = "VERIFYING"
    RESPONDING = "RESPONDING"
    RECOVERING = "RECOVERING"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"

class EventBus:
    def __init__(self):
        self._listeners = {}
        self._lock = threading.Lock()
        self.current_state = SystemState.IDLE
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("EventBus")

    def subscribe(self, event_type: str, callback):
        with self._lock:
            if event_type not in self._listeners:
                self._listeners[event_type] = []
            self._listeners[event_type].append(callback)
            self.logger.info(f"Subscribed to event: {event_type}")

    def publish(self, event_type: str, data=None):
        with self._lock:
            self.logger.info(f"Publishing event: {event_type} with data: {data}")
            listeners = list(self._listeners.get(event_type, []))
        
        for callback in listeners:
            try:
                callback(event_type, data)
            except Exception as e:
                self.logger.error(f"Error in listener for {event_type}: {e}")

    def transition_state(self, new_state: SystemState):
        with self._lock:
            self.logger.info(f"State transition: {self.current_state.value} -> {new_state.value}")
            self.current_state = new_state
