import json
import os

def get_tool_catalog():
    catalog_path = os.path.join(os.path.dirname(__file__), "catalog.json")
    if not os.path.exists(catalog_path):
        return {"categories": []}
    with open(catalog_path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def execute_registered_tool(tool_id: str):
    return {
        "status": "success",
        "message": f"Successfully executed tool: {tool_id}"
    }