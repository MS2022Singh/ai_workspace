import subprocess
import logging

class SandboxRunner:
    def __init__(self):
        self.logger = logging.getLogger("SandboxRunner")

    def run_isolated_command(self, command: list):
        self.logger.info(f"Running isolated command in sandbox environment: {command}")
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            return {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            self.logger.error(f"Sandbox execution failed: {e}")
            return {"exit_code": -1, "stdout": "", "stderr": str(e)}
