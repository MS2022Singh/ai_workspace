import os, pathlib
pathlib.Path('ai_workspace/catalog/registry').mkdir(parents=True, exist_ok=True)
content = """import json
from pathlib import Path

class ToolRegistry:
    def __init__(self, registry_path: str = "ai_workspace/catalog/registry/tools.json"):
        self.registry_path = Path(registry_path)
        self.tools = self._load_registry()

    def _load_registry(self) -> dict:
        if self.registry_path.exists():
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_registry(self):
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self.tools, f, indent=2)

    def register_tool(self, name: str, category: str, description: str, enabled: bool = True):
        self.tools[name] = {
            "category": category,
            "description": description,
            "enabled": enabled,
            "status": "active" if enabled else "disabled"
        }
        self.save_registry()
"""
with open("ai_workspace/catalog/registry/tool_registry.py", "w", encoding="utf-8") as f:
    f.write(content)
