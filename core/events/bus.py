import time
from pubsub import pub

class EventBus:
    def __init__(self):
        self.state = "IDLE"
        self.logs = []
        self.log(f"EventBus initialized. State: {self.state}")

    def set_state(self, new_state: str):
        self.state = new_state
        self.log(f"OS State Transition -> [{self.state}]")
        pub.sendMessage("os_state_change", state=self.state)

    def log(self, message: str, level: str = "INFO"):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(entry)
        if len(self.logs) > 200:
            self.logs.pop(0)

    def get_logs(self):
        return self.logs

event_bus = EventBus()