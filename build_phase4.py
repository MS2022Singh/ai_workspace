import os
import subprocess

os.makedirs("core", exist_ok=True)

inference_code = '''# core/inference_router.py
import urllib.request
import json
import logging
from core.event_bus import bus

class InferenceRouter:
    def __init__(self):
        self.providers = {
            "ollama": "http://localhost:11434/api/generate",
            "vllm": "http://localhost:8000/v1/completions",
            "sglang": "http://localhost:30000/v1/completions",
            "litellm": "http://localhost:4000/v1/completions"
        }
        self.active_provider = "ollama"

    def set_provider(self, provider_name):
        if provider_name in self.providers:
            self.active_provider = provider_name
            bus.publish("PROVIDER_CHANGED", {"provider": provider_name})
            return True
        return False

    def route_request(self, prompt, model="qwen2.5:latest"):
        endpoint = self.providers.get(self.active_provider)
        payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
        
        bus.publish("INFERENCE_STARTED", {"provider": self.active_provider, "model": model})
        
        try:
            req = urllib.request.Request(endpoint, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                bus.publish("INFERENCE_COMPLETED", {"status": "SUCCESS"})
                return res_data
        except Exception as e:
            bus.publish("INFERENCE_FAILED", {"error": str(e)})
            logging.warning(f"Inference provider {self.active_provider} unavailable: {e}")
            return {"error": f"Provider {self.active_provider} offline or unreachable", "details": str(e)}

router = InferenceRouter()
'''

system_tools_code = '''# core/system_tools.py
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
'''

with open("core/inference_router.py", "w", encoding="utf-8") as f:
    f.write(inference_code)

with open("core/system_tools.py", "w", encoding="utf-8") as f:
    f.write(system_tools_code)

readme_update = """
## Phase 4 Completed: External Tool Wrappers & Local Inference Engines
- Implemented `core/inference_router.py` supporting unified model routing (Ollama, vLLM, SGLang, LiteLLM).
- Implemented `core/system_tools.py` for PowerShell execution, process inspection, and system diagnostics bounded by `PermissionEngine`.
- Integrated tool invocation logging into `MemoryManager` episodic timeline.
"""

with open("README.md", "a", encoding="utf-8") as f:
    f.write(readme_update)

subprocess.run(["git", "add", "core/inference_router.py", "core/system_tools.py", "README.md"], check=True)
subprocess.run(["git", "commit", "-m", "feat(tools): integrate inference router and permission-guarded system tools"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("[+] Phase 4 successfully compiled, integrated, and pushed to GitHub.")
