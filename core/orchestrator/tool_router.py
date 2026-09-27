
# [Appended via CMD] Expose Tool Registry to Frontend Event Bus
import json

def load_tool_registry():
    try:
        with open("catalog/registry/tool_registry.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tools": []}

# Wire directly to the PyPubSub Event Bus
if 'event_bus' in globals():
    event_bus.subscribe("FETCH_TOOLS", load_tool_registry)
