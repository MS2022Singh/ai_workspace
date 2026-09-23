import sys
import os
import logging
sys.path.append(os.path.abspath("."))

from core.event_bus.pypubsub_router import event_bus

logger = logging.getLogger("BugEliminator")

class BugEliminator:
    def __init__(self):
        self.error_log = []

    def inspect_system(self) -> dict:
        issues_found = []
        # Check database existence
        if not os.path.exists("docs/project_memory/workspace_memory.db"):
            issues_found.append({"type": "missing_db", "severity": "medium"})
        
        # Check UI static files
        if not os.path.exists("modules/ui/index.html"):
            issues_found.append({"type": "missing_ui", "severity": "high"})

        return {"status": "clean" if not issues_found else "issues_detected", "issues": issues_found}

    def resolve_issue(self, issue: dict) -> bool:
        if issue["type"] == "missing_db":
            from core.memory.memory_manager import memory_manager
            memory_manager._init_db()
            logger.info("[BUG ELIMINATOR] Re-initialized missing SQLite DB.")
            return True
        return False

bug_eliminator = BugEliminator()
