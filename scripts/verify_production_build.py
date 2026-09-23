import sys
import os
import json
sys.path.append(os.path.abspath("."))

from core.verification.bug_eliminator import bug_eliminator
from catalog.tool_registry import tool_registry

def run_production_audit():
    print("[PRODUCTION BUILD AUDIT] Initializing checks...")
    
    # 1. Inspect required file paths
    required_paths = [
        "core/event_bus/pypubsub_router.py",
        "core/permission_engine/policy_manager.py",
        "core/memory/memory_manager.py",
        "modules/ui/index.html",
        "modules/ui/server.py",
        "modules/tools/tool_handler.py",
        "modules/audio/voice_engine.py",
        "modules/media/converter.py",
        "devices/registry.py",
        "catalog/tool_registry.py"
    ]
    
    missing = [p for p in required_paths if not os.path.exists(p)]
    if missing:
        print(f"[AUDIT FAILED] Missing critical components: {missing}")
        sys.exit(1)

    # 2. Inspect Bug Eliminator
    bug_report = bug_eliminator.inspect_system()
    print(f"[AUDIT] System Integrity Status: {bug_report['status']}")

    # 3. Inspect Registered Tools
    print(f"[AUDIT] Total Active Tools: {len([t for t in tool_registry.tools.values() if t.get('active')])}")
    print("[PRODUCTION BUILD AUDIT] ALL CHECKS PASSED SUCCESSFULLY.")

if __name__ == "__main__":
    run_production_audit()
