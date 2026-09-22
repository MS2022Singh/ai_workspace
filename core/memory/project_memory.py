import json
import os
import logging
from datetime import datetime

class ProjectMemory:
    def __init__(self, memory_file: str = "governance/project_memory.json"):
        self.memory_file = memory_file
        self.logger = logging.getLogger("ProjectMemory")
        self._ensure_directory()
        self.state = self.load_memory()

    def _ensure_directory(self):
        directory = os.path.dirname(self.memory_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def load_memory(self) -> dict:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.logger.info(f"Loaded project memory from {self.memory_file}")
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load memory file: {e}")
        
        # Default baseline memory structure
        return {
            "project_name": "AI Workspace Core",
            "last_updated": str(datetime.now()),
            "requirements": [],
            "decisions": [],
            "completed_work": [],
            "pending_work": [],
            "issues": []
        }

    def save_memory(self):
        self.state["last_updated"] = str(datetime.now())
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=4)
            self.logger.info("Project memory successfully persisted to disk.")
        except Exception as e:
            self.logger.error(f"Failed to save project memory: {e}")

    def log_completed_work(self, item: str):
        self.state["completed_work"].append({"item": item, "timestamp": str(datetime.now())})
        self.save_memory()

    def add_decision(self, decision: str):
        self.state["decisions"].append({"decision": decision, "timestamp": str(datetime.now())})
        self.save_memory()

    def add_issue(self, issue: str):
        self.state["issues"].append({"issue": issue, "timestamp": str(datetime.now())})
        self.save_memory()
