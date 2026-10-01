import subprocess
from core.permissions.enforcer import require_permission
from core.events.bus import event_bus

def execute_system_command(command: str) -> dict:
    require_permission("EXECUTE")
    event_bus.set_state("EXECUTING")
    event_bus.log(f"Dispatching shell command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
        event_bus.set_state("IDLE")
        return {
            "command": command,
            "stdout": result.stdout if result.stdout else result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        event_bus.set_state("IDLE")
        return {"command": command, "stdout": f"Execution Error: {str(e)}", "returncode": 1}