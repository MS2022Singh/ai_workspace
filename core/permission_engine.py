# core/permission_engine.py
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
