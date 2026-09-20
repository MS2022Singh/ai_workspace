import subprocess

class CommandExecutor:
    def run(self, command: str):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
            output = result.stdout if result.stdout else result.stderr
            return {"status": "success", "command": command, "output": output.strip()}
        except subprocess.TimeoutExpired:
            return {"status": "error", "command": command, "output": "Command timed out after 15 seconds."}
        except Exception as e:
            return {"status": "error", "command": command, "output": str(e)}
