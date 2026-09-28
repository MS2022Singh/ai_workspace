import pathlib, json
from core.event_bus.bus import event_bus

class SelfUpgraderEngine:
    def __init__(self, registry_file: str = "ai_workspace/catalog/registry/tools.json"):
        self.registry_path = pathlib.Path(registry_file)

    def discover_and_register(self, repo_url: str, tool_name: str, category: str, description: str) -> dict:
        event_bus.publish("UPGRADE_STARTED", {"repo_url": repo_url, "tool_name": tool_name})
        
        registry = {}
        if self.registry_path.exists():
            with open(self.registry_path, "r", encoding="utf-8") as f:
                try:
                    registry = json.load(f)
                except Exception:
                    registry = {}

        registry[tool_name] = {
            "category": category,
            "description": description,
            "source_url": repo_url,
            "enabled": True,
            "status": "active"
        }

        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)

        event_bus.publish("UPGRADE_COMPLETED", {"tool_name": tool_name})
        return {"status": "success", "tool_name": tool_name, "registry": registry}

self_upgrader = SelfUpgraderEngine()
