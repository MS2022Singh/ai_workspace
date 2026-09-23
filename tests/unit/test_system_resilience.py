import unittest
import sys
import os
sys.path.append(os.path.abspath("."))

from core.verification.bug_eliminator import bug_eliminator
from devices.registry import device_registry
from core.orchestrator.self_upgrade import self_upgrade_engine
from catalog.tool_registry import tool_registry

class TestSystemResilience(unittest.TestCase):

    def test_bug_eliminator_inspection(self):
        report = bug_eliminator.inspect_system()
        self.assertIn(report["status"], ["clean", "issues_detected"])

    def test_device_registry(self):
        info = device_registry.device_info
        self.assertIn("os", info)
        device_registry.sync_to_memory()

    def test_self_upgradation_pipeline(self):
        res = self_upgrade_engine.discover_and_incorporate("Custom Scraper Tool", "https://github.com/example/scraper")
        self.assertEqual(res["status"], "success")
        self.assertIn("custom_scraper_tool", tool_registry.tools)

if __name__ == "__main__":
    unittest.main()
