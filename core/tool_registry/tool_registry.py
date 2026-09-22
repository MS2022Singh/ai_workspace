import logging
from core.permission_engine.permission_engine import PermissionEngine, PermissionClass

class ToolRegistry:
    def __init__(self, permission_engine: PermissionEngine):
        self.permission_engine = permission_engine
        self.logger = logging.getLogger("ToolRegistry")
        self._tools = {}

    def register_tool(self, tool_name: str, permission_class: PermissionClass, func):
        self._tools[tool_name] = {
            "permission_class": permission_class,
            "function": func
        }
        self.logger.info(f"Registered tool '{tool_name}' with permission class {permission_class.value}")

    def execute_tool(self, tool_name: str, user_authorized: bool = False, *args, **kwargs):
        if tool_name not in self._tools:
            self.logger.error(f"Tool '{tool_name}' not found in registry.")
            raise ValueError(f"Tool '{tool_name}' not found.")

        tool_info = self._tools[tool_name]
        perm_class = tool_info["permission_class"]

        if not self.permission_engine.validate_action(perm_class, user_authorized):
            self.logger.warning(f"Execution blocked for tool '{tool_name}': Permission denied.")
            return {"status": "DENIED", "message": f"Required permission class {perm_class.value} not authorized."}

        self.logger.info(f"Executing tool '{tool_name}'...")
        result = tool_info["function"](*args, **kwargs)
        return {"status": "SUCCESS", "result": result}
