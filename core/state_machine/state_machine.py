class WorkspaceStateMachine:
    STATES = [
        "IDLE", "LISTENING", "UNDERSTANDING", "PLANNING",
        "PERMISSION_CHECK", "EXECUTING", "VERIFYING",
        "RESPONDING", "MEMORY_UPDATE"
    ]

    def __init__(self):
        self.current_state = "IDLE"
        self.history = ["IDLE"]

    def transition_to(self, target_state: str) -> bool:
        if target_state in self.STATES:
            self.current_state = target_state
            self.history.append(target_state)
            return True
        return False

    def get_state(self) -> str:
        return self.current_state

state_machine = WorkspaceStateMachine()
