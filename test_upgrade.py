import sys
import os

# Simulate dynamic capability expansion: adding a new custom analysis tool on the fly
print("--- STARTING DYNAMIC SELF-UPGRADATION TEST ---")

tool_registry = {}

def register_dynamic_tool(name: str, func, description: str):
    tool_registry[name] = {
        "function": func,
        "description": description
    }
    print(f"[UPGRADE SUCCESS] Dynamically registered new capability: '{name}' -> {description}")

# Define a newly 'discovered' or 'self-upgraded' tool function (e.g., text sentiment / JSON validator)
def validate_json_schema_tool(payload: dict) -> bool:
    return isinstance(payload, dict) and len(payload) > 0

# Perform the dynamic tool injection
register_dynamic_tool("json_validator", validate_json_schema_tool, "Validates JSON structure dynamically.")

# Verify tool execution
is_valid = tool_registry["json_validator"]["function"]({"status": "active"})
print(f"[VERIFICATION] Executing 'json_validator' result: {is_valid}")

if is_valid:
    print("--- DYNAMIC SELF-UPGRADATION TEST PASSED CLEANLY ---")
else:
    print("--- TEST FAILED ---")
    sys.exit(1)