import sys
import os
sys.path.append(os.path.abspath("."))

from catalog.tool_registry import tool_registry
from core.event_bus.pypubsub_router import event_bus

class SelfUpgradationEngine:
    def discover_and_incorporate(self, capability_name: str, repo_url: str = None) -> dict:
        tool_id = capability_name.lower().replace(" ", "_")
        if tool_id in tool_registry.tools:
            return {"status": "exists", "message": f"Tool '{tool_id}' already registered."}

        # Dynamically register newly discovered tool/capability
        tool_registry.tools[tool_id] = {
            "name": capability_name,
            "category": "auto_incorporated",
            "active": True,
            "perm": "EXECUTE",
            "source_repo": repo_url or "discovered_online"
        }
        tool_registry.save()
        event_bus.publish("UPGRADE_COMPLETED", {"tool_id": tool_id, "source": repo_url})
        return {"status": "success", "message": f"Capability '{capability_name}' incorporated successfully."}

self_upgrade_engine = SelfUpgradationEngine()
