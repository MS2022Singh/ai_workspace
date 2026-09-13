import unittest
from computer_control import ComputerControlLayer

class TestComputerControlLayer(unittest.TestCase):
    def test_system_inspection(self):
        controller = ComputerControlLayer()
        status = controller.inspect_system(user_level=1)
        self.assertEqual(status['status'], 'success')
        self.assertIn('cpu_usage', status)

    def test_execute_approval_gate(self):
        controller = ComputerControlLayer()
        res = controller.execute_controlled_action('test_script.py', user_level=1)
        self.assertTrue(res.get('requires_approval'))

if __name__ == '__main__':
    unittest.main()
