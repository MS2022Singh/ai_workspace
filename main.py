import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from core.event_bus.bus import event_bus
from core.state_machine.state_machine import state_machine
from core.permission_engine.policy import permission_engine
from core.agent_manager.orchestrator import orchestrator
from core.upgrade_engine.self_upgrader import self_upgrader
from devices.registry.device_registry import device_registry
from media.conversion.converter import converter
from media.compression.compressor import compressor

app = FastAPI(title="AI Workspace OS | Master Command Center")

os.makedirs("ui/frontend", exist_ok=True)
app.mount("/static", StaticFiles(directory="ui/frontend"), name="static")

class CommandPayload(BaseModel):
    module: str
    action: str
    prompt: str = ""
    methodology: str = None

class UpgradePayload(BaseModel):
    repo_url: str
    tool_name: str
    category: str
    description: str

class PolicyPayload(BaseModel):
    autonomy_level: int
    permissions: dict

@app.get("/", response_class=HTMLResponse)
async def read_root():
    if os.path.exists("ui/frontend/index.html"):
        with open("ui/frontend/index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Master OS index.html missing</h1>"

@app.get("/api/state")
async def get_state():
    return JSONResponse({
        "state": state_machine.get_state(),
        "autonomy_level": permission_engine.autonomy_level,
        "permissions": permission_engine.active_permissions,
        "device_specs": device_registry.get_system_specs(),
        "recent_events": event_bus.event_log[-10:]
    })

@app.post("/api/command")
async def execute_command(payload: CommandPayload):
    result = orchestrator.dispatch(
        agent_name=f"{payload.module.capitalize()}Agent",
        task=payload.action or payload.prompt,
        payload={"methodology": payload.methodology}
    )
    return JSONResponse(result)

@app.post("/api/upgrade")
async def auto_upgrade(payload: UpgradePayload):
    res = self_upgrader.discover_and_register(
        repo_url=payload.repo_url,
        tool_name=payload.tool_name,
        category=payload.category,
        description=payload.description
    )
    return JSONResponse(res)

@app.post("/api/policy")
async def update_policy(payload: PolicyPayload):
    permission_engine.update_policy(payload.autonomy_level, payload.permissions)
    return JSONResponse({"status": "success", "autonomy_level": permission_engine.autonomy_level})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
