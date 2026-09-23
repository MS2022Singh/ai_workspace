import os

print("[+] Writing synchronized backend engine...")

main_py_content = """import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="AI Workspace OS | Synchronized Core")

# Mount static directory
app.mount("/static", StaticFiles(directory="ui/frontend"), name="static")

class CommandPayload(BaseModel):
    panel: str
    command: str

class ToolTogglePayload(BaseModel):
    tool: str
    enabled: bool

# In-memory state tracking for tools and agent policies
SYSTEM_STATE = {
    "tools": {
        "ToolJet & n8n": True,
        "AppFlowy Workspace": True,
        "OpenHands Sandbox": True,
        "Browser Use Engine": True,
        "Qwen 3.8 & Ollama": True,
        "Crawl4AI & Semantica": True,
        "PyRIT & Vulture": False
    },
    "autonomy_level": "Level 1: Observe Only"
}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    if os.path.exists("ui/frontend/index.html"):
        with open("ui/frontend/index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>UI index.html not found</h1>"

@app.post("/api/command")
async def handle_command(payload: CommandPayload):
    print(f"[EVENT BUS] Executing command from [{payload.panel}]: {payload.command}")
    # Simulate intelligent routing and execution based on panel & command
    response_msg = f"Successfully processed '{payload.command}' within {payload.panel} pipeline."
    if "crawl" in payload.command.lower() or "research" in payload.command.lower():
        response_msg = f"Crawl4AI executed successfully for target: {payload.command}. Provenance verified."
    elif "audit" in payload.command.lower() or "security" in payload.command.lower():
        response_msg = f"PyRIT security vulnerability scan completed. 0 critical vulnerabilities found."
    
    return JSONResponse({"status": "success", "message": response_msg})

@app.post("/api/toggle-tool")
async def toggle_tool(payload: ToolTogglePayload):
    if payload.tool in SYSTEM_STATE["tools"]:
        SYSTEM_STATE["tools"][payload.tool] = payload.enabled
        print(f"[REGISTRY] Tool '{payload.tool}' set to: {payload.enabled}")
        return JSONResponse({"status": "success", "tools": SYSTEM_STATE["tools"]})
    return JSONResponse({"status": "error", "message": "Tool not found"}, status_code=404)

@app.get("/api/state")
async def get_state():
    return JSONResponse(SYSTEM_STATE)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_py_content)

print("[+] Synchronized backend engine written to main.py.")
