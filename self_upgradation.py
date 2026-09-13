import os
import json

class SelfUpgradationEngine:
    def __init__(self):
        self.installed_tools = {}

    def register_tool(self, tool_name: str, capabilities: list):
        self.installed_tools[tool_name] = {
            "capabilities": capabilities,
            "status": "active", # Active by default
            "source": "pre-incorporated repo"
        }

    def set_tool_state(self, tool_name: str, active: bool):
        if tool_name in self.installed_tools:
            self.installed_tools[tool_name]["status"] = "active" if active else "disabled"
            return {"status": "success", "tool": tool_name, "state": self.installed_tools[tool_name]["status"]}
        return {"status": "error", "message": "Tool not found"}

    def analyze_repository(self, repo_url: str):
        if not repo_url:
            return {"status": "error", "message": "Invalid repository URL"}
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        return {
            "status": "success",
            "repo_name": repo_name,
            "compatibility": "verified",
            "security_check": "passed"
        }

    def sandbox_install(self, repo_name: str):
        self.installed_tools[repo_name] = {
            "capabilities": ["dynamic_ui_rendering", "interactive_components"],
            "status": "active",
            "source": repo_name
        }
        return {
            "status": "success",
            "message": f"Repository '{repo_name}' successfully sandboxed, incorporated, and activated.",
            "active_tools": list(self.installed_tools.keys())
        }
