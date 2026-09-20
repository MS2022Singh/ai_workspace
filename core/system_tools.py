# core/system_tools.py
import subprocess
import os
import psutil
from core.permission_engine import engine, SecurityLevel, PermissionClass
from core.event_bus import bus
from core.memory_manager import memory

class SystemTools:
    def __init__(self):
        engine.register_tool("shell_execution", [PermissionClass.EXECUTE, PermissionClass.SYSTEM], SecurityLevel.LEVEL_2_CONTROLLED)
        engine.register_tool("process_inspection", [PermissionClass.READ, PermissionClass.SYSTEM], SecurityLevel.LEVEL_0_OBSERVE)
        engine.register_tool("file_read", [PermissionClass.READ], SecurityLevel.LEVEL_0_OBSERVE)

    def execute_powershell(self, command):
        if not engine.validate_action("shell_execution", f"Execute PowerShell: {command}"):
            return {"status": "BLOCKED", "reason": "Permission denied by Permission Engine"}

        try:
            result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, timeout=30)
            output = result.stdout if result.returncode == 0 else result.stderr
            memory.log_episode("SHELL_EXECUTION", {"command": command, "exit_code": result.returncode})
            return {"status": "SUCCESS", "output": output, "exit_code": result.returncode}
        except Exception as e:
            memory.log_episode("SHELL_ERROR", {"command": command, "error": str(e)})
            return {"status": "ERROR", "error": str(e)}

    def inspect_processes(self, limit=10):
        if not engine.validate_action("process_inspection", "Inspect System Processes"):
            return {"status": "BLOCKED"}
        
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                procs.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return {"status": "SUCCESS", "processes": procs[:limit]}

tools = SystemTools()
