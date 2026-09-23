from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    LISTENING = auto()
    UNDERSTANDING = auto()
    PLANNING = auto()
    PERMISSION_CHECK = auto()
    EXECUTING = auto()
    VERIFYING = auto()
    RESPONDING = auto()
    MEMORY_UPDATE = auto()

class ExecutionStateMachine:
    def __init__(self):
        self.current_state = State.IDLE

    def transition_to(self, new_state: State):
        print(f"[STATE MACHINE] Transition: {self.current_state.name} -> {new_state.name}")
        self.current_state = new_state

state_machine = ExecutionStateMachine()
