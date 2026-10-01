import psutil, platform

def get_system_telemetry():
    return {
        'os': platform.system(),
        'os_release': platform.release(),
        'cpu_cores': psutil.cpu_count(logical=True),
        'cpu_usage_pct': psutil.cpu_percent(interval=0.5),
        'ram_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
        'ram_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
        'disk_usage_pct': psutil.disk_usage('/').percent
    }
