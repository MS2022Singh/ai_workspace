import unittest
from event_bus import EventBus

class TestEventBus(unittest.TestCase):
    def test_pub_sub(self):
        bus = EventBus()
        received = []
        bus.subscribe('TASK_CREATED', lambda data: received.append(data))
        bus.publish('TASK_CREATED', {'task_id': 1})
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['task_id'], 1)

if __name__ == '__main__':
    unittest.main()
