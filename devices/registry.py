import platform
import sys
import os
sys.path.append(os.path.abspath("."))

from core.memory.memory_manager import memory_manager

class DeviceRegistry:
    def __init__(self):
        self.device_info = self._get_local_hardware()

    def _get_local_hardware(self) -> dict:
        return {
            "device_id": platform.node(),
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "status": "online"
        }

    def sync_to_memory(self):
        memory_manager.set_fact("device_info", str(self.device_info))
        memory_manager.log_episode("DEVICE_SYNC", f"Synced device {self.device_info['device_id']}")

device_registry = DeviceRegistry()
