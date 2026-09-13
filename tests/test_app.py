import unittest

class TestCoreApp(unittest.TestCase):
    def test_app_import(self):
        try:
            import app
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f'Failed to import app: {e}')

if __name__ == '__main__':
    unittest.main()
