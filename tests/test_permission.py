import unittest
from permission_engine import PermissionEngine

class TestPermissionEngine(unittest.TestCase):
    def test_permissions(self):
        engine = PermissionEngine()
        self.assertTrue(engine.check_permission('read_file', 0))
        self.assertFalse(engine.check_permission('delete_files', 1))
        self.assertTrue(engine.check_permission('delete_files', 3))

if __name__ == '__main__':
    unittest.main()
