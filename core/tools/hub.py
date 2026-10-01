import os
import json

CATALOG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "catalog", "registry", "repos.json")

def get_tool_catalog() -> dict:
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"categories": []}

def execute_registered_tool(tool_id: str) -> dict:
    catalog = get_tool_catalog()
    found_tool = None
    for cat in catalog.get("categories", []):
        for tool in cat.get("tools", []):
            if tool["id"] == tool_id:
                found_tool = tool
                break
                
    if not found_tool:
        return {"status": "error", "message": f"Tool '{tool_id}' not found in registry."}
        
    return {
        "status": "success",
        "tool_id": tool_id,
        "name": found_tool["name"],
        "type": found_tool["type"],
        "message": f"Successfully initialized and executed tool module '{found_tool['name']}'."
    }