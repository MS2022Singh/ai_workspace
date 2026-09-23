import json
import os

class ToolRegistry:
    def __init__(self, registry_file="catalog/registry.json"):
        self.registry_file = registry_file
        self.tools = {}
        self.models = {}
        self._load_or_init()

    def _load_or_init(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r') as f:
                data = json.load(f)
                self.tools = data.get("tools", {})
                self.models = data.get("models", {})
        else:
            self.tools = {
                "openhands": {"name": "OpenHands Coding Agent", "category": "coding", "active": True, "perm": "EXECUTE"},
                "browser_use": {"name": "Browser Use Engine", "category": "web", "active": True, "perm": "NETWORK"},
                "pyrit": {"name": "PyRIT Red-Teaming", "category": "security", "active": False, "perm": "SYSTEM"},
                "crawl4ai": {"name": "Crawl4AI Web Crawler", "category": "rag", "active": True, "perm": "NETWORK"},
                "semantica": {"name": "Semantica GraphRAG", "category": "rag", "active": True, "perm": "READ"},
                "stirling_pdf": {"name": "Stirling PDF Converter", "category": "media", "active": True, "perm": "WRITE"},
                "fooocus": {"name": "Fooocus Image Gen", "category": "creative", "active": True, "perm": "WRITE"}
            }
            self.models = {
                "qwen-3.8-local": {"name": "Qwen 3.8 Local", "type": "llm", "active": True},
                "vllm-engine": {"name": "vLLM Server", "type": "llm", "active": False},
                "ollama-local": {"name": "Ollama Local Fleet", "type": "llm", "active": True},
                "wan2.2-vlm": {"name": "Wan2.2 Vision Video", "type": "vlm", "active": False},
                "whisper-local": {"name": "Whisper Speech-to-Text", "type": "audio", "active": True}
            }
            self.save()

    def save(self):
        with open(self.registry_file, 'w') as f:
            json.dump({"tools": self.tools, "models": self.models}, f, indent=4)

    def set_tool_status(self, tool_id: str, active: bool):
        if tool_id in self.tools:
            self.tools[tool_id]["active"] = active
            self.save()

tool_registry = ToolRegistry()
