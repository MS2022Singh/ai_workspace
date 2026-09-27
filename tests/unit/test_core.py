import unittest
import sys
import os
sys.path.append(os.path.abspath("."))

from core.event_bus.pypubsub_router import event_bus
from core.permission_engine.policy_manager import policy_engine, PermissionClass
from core.memory.memory_manager import memory_manager
from catalog.tool_registry import tool_registry
from modules.agents.agent_manager import agent_manager

class TestCoreArchitecture(unittest.TestCase):

    def test_permission_engine(self):
        self.assertTrue(policy_engine.check_permission(PermissionClass.READ))
        self.assertFalse(policy_engine.check_permission(PermissionClass.EXECUTE))

    def test_memory_manager(self):
        memory_manager.set_fact("test_key", "test_value")
        memory_manager.log_episode("TEST_EVENT", "Executing unit tests")

    def test_tool_registry(self):
        self.assertIn("openhands", tool_registry.tools)
        tool_registry.set_tool_status("openhands", True)
        self.assertTrue(tool_registry.tools["openhands"]["active"])

    def test_agent_dispatch(self):
        res = agent_manager.dispatch("research", "Quantum computing fundamentals")
        self.assertEqual(res["status"], "success")

if __name__ == "__main__":
    unittest.main()
