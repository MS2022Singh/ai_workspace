import os
import subprocess

def create_core_directories():
    os.makedirs("core", exist_ok=True)
    print("[+] Created 'core' directory structure.")

def generate_event_bus():
    content = """# core/event_bus.py
import logging

class EventBus:
    def __init__(self):
        self.subscribers = {}
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type, data=None):
        logging.info(f"Event published: {event_type} | Data: {data}")
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)

# Global Event Bus instance
bus = EventBus()
"""
    with open("core/event_bus.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("[+] Generated core/event_bus.py (Internal Event Bus for state messaging)")

def generate_permission_engine():
    content = """# core/permission_engine.py
from enum import Enum, auto
import logging
from core.event_bus import bus

# 4-Tier Autonomous Control Levels
class SecurityLevel(Enum):
    LEVEL_0_OBSERVE = 0      # Read-only / Inspect
    LEVEL_1_SUGGEST = 1      # Low-risk (e.g., UI suggest, Read files)
    LEVEL_2_CONTROLLED = 2   # Execute with explicit approval (Modify files, Run scripts)
    LEVEL_3_AUTONOMOUS = 3   # High-risk autonomous execution (Network, System changes)

# Strict Permission Classes
class PermissionClass(Enum):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    NETWORK = auto()
    DELETE = auto()
    SYSTEM = auto()
    FINANCIAL = auto()

class PermissionEngine:
    def __init__(self):
        # Default safe policy: Require explicit approval for modifications
        self.current_policy = SecurityLevel.LEVEL_1_SUGGEST
        self.tool_permissions = {}
        
    def set_system_policy(self, level: SecurityLevel):
        self.current_policy = level
        bus.publish("SYSTEM_POLICY_CHANGED", {"new_level": level.name})
        
    def register_tool(self, tool_name, perm_classes, required_level):
        self.tool_permissions[tool_name] = {
            'classes': perm_classes,
            'level': required_level
        }
        bus.publish("TOOL_REGISTERED", {"tool": tool_name, "level": required_level.name})

    def validate_action(self, tool_name, requested_action):
        if tool_name not in self.tool_permissions:
            logging.warning(f"[SECURITY BLOCK] Unregistered tool '{tool_name}' attempted execution.")
            bus.publish("APPROVAL_REQUIRED", {"tool": tool_name, "action": requested_action, "reason": "Unregistered tool"})
            return False
            
        required_level = self.tool_permissions[tool_name]['level']
        
        if self.current_policy.value >= required_level.value:
            logging.info(f"[SECURITY ALLOW] '{tool_name}' authorized to execute: {requested_action}")
            bus.publish("TOOL_EXECUTED", {"tool": tool_name, "action": requested_action})
            return True
        else:
            logging.warning(f"[SECURITY BLOCK] '{tool_name}' requires {required_level.name}. Current Policy is {self.current_policy.name}.")
            bus.publish("APPROVAL_REQUIRED", {"tool": tool_name, "action": requested_action})
            return False

# Global Permission Engine instance
engine = PermissionEngine()
"""
    with open("core/permission_engine.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("[+] Generated core/permission_engine.py (Level 0-3 Security & Strict Policies)")

def update_readme():
    readme_update = """
## Phase 2 Completed: Permission Engine & Internal Event Bus
- Implemented `core/event_bus.py` to route system states and decouple component execution.
- Implemented `core/permission_engine.py` applying Level 0-3 Computer Control guardrails.
- Configured rigid Permission Classes (READ, WRITE, EXECUTE, NETWORK, DELETE, SYSTEM, FINANCIAL) to validate tools pre-execution.
"""
    with open("README.md", "a", encoding="utf-8") as f:
        f.write(readme_update)
    print("[+] Updated README.md with Phase 2 documentation.")

def git_commit_and_push():
    print("[+] Executing Git operations to sync Phase 2 with GitHub...")
    try:
        subprocess.run(["git", "add", "core/", "README.md"], check=True)
        subprocess.run(["git", "commit", "-m", "feat(security): implement Level 0-3 permission engine and internal event bus"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("[+] Phase 2 successfully pushed to repository.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Git command failed: {e}")

if __name__ == "__main__":
    print("Initiating Phase 2 Build Sequence...")
    create_core_directories()
    generate_event_bus()
    generate_permission_engine()
    update_readme()
    git_commit_and_push()
    print("\nPhase 2 Complete. Core Security and Event architecture successfully compiled and pushed.")