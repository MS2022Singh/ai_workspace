import unittest
from os_registry import WorkspaceOSEngine

class TestWorkspaceOSEngine(unittest.TestCase):
    def setUp(self):
        self.os = WorkspaceOSEngine()

    def test_system_boot_event(self):
        res = self.os.event_bus.publish('SYSTEM_BOOT', {'os': 'Windows', 'arch': 'x64'})
        self.assertEqual(self.os.state, 'IDLE')
        self.assertEqual(res[0]['status'], 'Boot Complete')

    def test_central_task_routing_cognitive(self):
        res = self.os.execute_central_task('learn_skill', {'skill': 'Python Architecture'})
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['skill'], 'Python Architecture')
        self.assertEqual(self.os.state, 'IDLE')

    def test_central_task_routing_inspection(self):
        res = self.os.execute_central_task('inspect_system', {}, user_level=1)
        self.assertEqual(res['status'], 'success')
        self.assertIn('cpu_usage', res)

if __name__ == '__main__':
    unittest.main()
