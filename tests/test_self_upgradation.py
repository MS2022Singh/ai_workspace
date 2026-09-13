import unittest
from self_upgradation import SelfUpgradationEngine

class TestSelfUpgradationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SelfUpgradationEngine()

    def test_analyze_repository(self):
        res = self.engine.analyze_repository('https://github.com/example/awesome-ai-tool.git')
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['repo_name'], 'awesome-ai-tool')
        self.assertTrue(res['dependencies_analyzed'])

    def test_sandbox_install(self):
        res = self.engine.sandbox_install('awesome-ai-tool')
        self.assertEqual(res['status'], 'success')
        self.assertTrue(res['isolated'])

    def test_register_tool(self):
        res = self.engine.register_tool('awesome-ai-tool', ['process_data', 'generate_insight'])
        self.assertEqual(res['status'], 'success')
        self.assertIn('awesome-ai-tool', self.engine.installed_tools)
        self.assertEqual(len(self.engine.installed_tools['awesome-ai-tool']), 2)

if __name__ == '__main__':
    unittest.main()
