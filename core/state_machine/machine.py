
from enum import Enum

class SystemState(Enum):
    IDLE = 'IDLE'
    LISTENING = 'LISTENING'
    UNDERSTANDING = 'UNDERSTANDING'
    PLANNING = 'PLANNING'
    PERMISSION_CHECK = 'PERMISSION_CHECK'
    EXECUTING = 'EXECUTING'
    VERIFYING = 'VERIFYING'
    RESPONDING = 'RESPONDING'
    MEMORY_UPDATE = 'MEMORY_UPDATE'

class StateMachine:
    def __init__(self):
        self.current_state = SystemState.IDLE

    def transition(self, new_state: SystemState):
        self.current_state = new_state
        print(f'[State Machine] Transitioned to: {self.current_state.value}')

state_machine = StateMachine()
