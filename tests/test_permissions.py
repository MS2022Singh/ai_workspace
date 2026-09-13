import unittest
from permissions import PermissionEngine

class TestPermissionEngine(unittest.TestCase):
    def test_read_permission(self):
        engine = PermissionEngine()
        res = engine.check_permission('READ', user_authorized_level=1)
        self.assertTrue(res['allowed'])

    def test_execute_approval(self):
        engine = PermissionEngine()
        res = engine.check_permission('EXECUTE', user_authorized_level=1)
        self.assertTrue(res['requires_approval'])

if __name__ == '__main__':
    unittest.main()
