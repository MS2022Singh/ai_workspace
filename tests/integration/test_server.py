import unittest
import sys
import os
sys.path.append(os.path.abspath("."))

from modules.tools.tool_handler import tool_handler
from catalog.tool_registry import tool_registry
from core.permission_engine.policy_manager import policy_engine, PermissionClass

class TestIntegration(unittest.TestCase):

    def test_image_generation_payload(self):
        policy_engine.set_permission(PermissionClass.WRITE, True)
        tool_registry.set_tool_status("fooocus", True)
        res = tool_handler.execute_tool("fooocus", {"prompt": "A futuristic glowing crystal flower"})
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["type"], "image")
        self.assertIn("prompt", res)

    def test_permission_enforcement_on_tool(self):
        policy_engine.set_permission(PermissionClass.EXECUTE, False)
        tool_registry.set_tool_status("openhands", True)
        res = tool_handler.execute_tool("openhands", {"command": "build"})
        self.assertEqual(res["status"], "permission_denied")

if __name__ == "__main__":
    unittest.main()
