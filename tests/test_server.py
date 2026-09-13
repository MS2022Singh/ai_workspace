import unittest
import json
from server import app

class TestCommandCenter(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_status_endpoint(self):
        response = self.app.get('/api/status')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'online')
        self.assertIn('os_state', data)

    def test_execute_endpoint(self):
        payload = {
            'task_type': 'learn_skill',
            'payload': {'skill': 'Neural Networks'}
        }
        response = self.app.post('/api/execute', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['skill'], 'Neural Networks')

if __name__ == '__main__':
    unittest.main()
