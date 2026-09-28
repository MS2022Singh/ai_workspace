import platform

class DeviceRegistry:
    @staticmethod
    def get_system_specs() -> dict:
        return {
            "device_id": "PRIMARY_NODE_DESKTOP",
            "platform": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor() or "x86_64 Compatible",
            "status": "online"
        }

device_registry = DeviceRegistry()
