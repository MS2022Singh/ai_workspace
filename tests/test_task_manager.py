import unittest
from memory_engine import MemoryEngine
from event_bus import EventBus
from task_manager import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.memory = MemoryEngine(db_path=':memory:')
        self.bus = EventBus()
        self.manager = TaskManager(self.memory, self.bus)

    def test_create_and_get_task(self):
        events = []
        self.bus.subscribe('TASK_CREATED', lambda d: events.append(d))
        self.manager.create_task('t1', 'Implement UI', 'Frontend Expert')
        task = self.manager.get_task('t1')
        self.assertEqual(task['title'], 'Implement UI')
        self.assertEqual(task['status'], 'PENDING')
        self.assertEqual(len(events), 1)

if __name__ == '__main__':
    unittest.main()
