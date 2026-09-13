import unittest
from unittest.mock import patch
import sys
from cli import main

class TestCLI(unittest.TestCase):
    def test_cli_execution(self):
        with patch('sys.argv', ['cli.py', '--task_id', 'cli_1', '--title', 'Test CLI Task', '--domain', 'frontend']), \
             patch('app.CoreApplication.run_workflow') as mock_workflow:
            mock_workflow.return_value = {'status': 'success'}
            try:
                main()
            except SystemExit:
                pass
            mock_workflow.assert_called_once_with('cli_1', 'Test CLI Task', 'frontend')

if __name__ == '__main__':
    unittest.main()
