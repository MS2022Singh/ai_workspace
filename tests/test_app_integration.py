import unittest
from app import CoreApplication

class TestAppIntegration(unittest.TestCase):
    def test_workflow(self):
        app = CoreApplication(db_path=':memory:')
        result = app.run_workflow('task_100', 'Design API schema', 'backend')
        self.assertEqual(result['task']['status'], 'PENDING')
        self.assertEqual(result['assignment']['assigned_expert'], 'Backend Systems Expert')

if __name__ == '__main__':
    unittest.main()
