import unittest
import os
from memory_engine import MemoryEngine

class TestMemoryEngine(unittest.TestCase):
    def setUp(self):
        self.db_file = 'test_memory.db'
        self.memory = MemoryEngine(db_path=self.db_file)

    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_set_and_get(self):
        self.memory.set_memory('user_intent', 'Finalize desktop AI OS', 'project')
        val = self.memory.get_memory('user_intent')
        self.assertEqual(val, 'Finalize desktop AI OS')

if __name__ == '__main__':
    unittest.main()
