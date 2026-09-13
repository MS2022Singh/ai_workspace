from memory_engine import MemoryEngine
from event_bus import EventBus
from task_manager import TaskManager
from agent_dispatcher import AgentDispatcher

class CoreApplication:
    def __init__(self, db_path='workspace_memory.db'):
        self.memory = MemoryEngine(db_path=db_path)
        self.bus = EventBus()
        self.tasks = TaskManager(self.memory, self.bus)
        self.dispatcher = AgentDispatcher()

    def run_workflow(self, task_id: str, title: str, domain: str):
        self.tasks.create_task(task_id, title)
        assignment = self.dispatcher.dispatch(domain, title)
        return {
            'task': self.tasks.get_task(task_id),
            'assignment': assignment
        }

if __name__ == '__main__':
    app = CoreApplication()
    print('Core Application Initialized Successfully.')
