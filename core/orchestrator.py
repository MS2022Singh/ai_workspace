
import asyncio
from core.state_machine.machine import state_machine, SystemState
from core.event_bus.bus import event_bus

class Orchestrator:
    def __init__(self):
        self.active_task = None

    async def execute_task(self, task_description: str):
        print(f'[Orchestrator] Received task: {task_description}')
        state_machine.transition(SystemState.UNDERSTANDING)
        await event_bus.emit('task_received', task_description)
        
        state_machine.transition(SystemState.PLANNING)
        await asyncio.sleep(0.1)
        
        state_machine.transition(SystemState.PERMISSION_CHECK)
        await asyncio.sleep(0.1)
        
        state_machine.transition(SystemState.EXECUTING)
        print(f'[Orchestrator] Executing task actions...')
        await asyncio.sleep(0.2)
        
        state_machine.transition(SystemState.VERIFYING)
        print(f'[Orchestrator] Verifying execution results...')
        await asyncio.sleep(0.1)
        
        state_machine.transition(SystemState.RESPONDING)
        state_machine.transition(SystemState.MEMORY_UPDATE)
        state_machine.transition(SystemState.IDLE)
        print('[Orchestrator] Task workflow completed successfully.')

orchestrator = Orchestrator()
