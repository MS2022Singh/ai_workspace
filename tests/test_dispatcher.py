import unittest
from agent_dispatcher import AgentDispatcher

class TestAgentDispatcher(unittest.TestCase):
    def test_dispatch_known_domain(self):
        dispatcher = AgentDispatcher()
        result = dispatcher.dispatch('frontend', 'Build React dashboard')
        self.assertEqual(result['assigned_expert'], 'Frontend Developer Expert')
        self.assertEqual(result['status'], 'DISPATCHED')

    def test_dispatch_unknown_domain(self):
        dispatcher = AgentDispatcher()
        result = dispatcher.dispatch('unknown', 'Perform general task')
        self.assertEqual(result['assigned_expert'], 'General AI Assistant')

if __name__ == '__main__':
    unittest.main()
