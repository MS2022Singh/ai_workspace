from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="AI Workspace OS Core")

# Mount static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="ui/frontend"), name="static")

# Event Bus Data Model
class CommandPayload(BaseModel):
    source_panel: str
    command: str
    parameters: dict = {}

@app.get("/")
async def serve_ui():
    return FileResponse("ui/frontend/index.html")

# Phase 4: Central Event Bus Endpoint
@app.post("/api/command")
async def process_command(payload: CommandPayload):
    # Log incoming command to terminal
    print(f"\n[EVENT BUS] Received from {payload.source_panel}: {payload.command}")
    
    # Basic routing logic (to be expanded with actual AI agents later)
    response_msg = f"Task received by core bus. Target: {payload.source_panel}. Execution pending integration."
    
    if payload.source_panel == "research-panel":
        response_msg = f"Initializing Crawl4AI sequence for target: {payload.command}"
    elif payload.source_panel == "code-panel":
        response_msg = f"Analyzing repository logic for: {payload.command}"
    elif payload.source_panel == "system-panel":
        response_msg = "System configuration updated securely."

    return {"status": "success", "message": response_msg, "echo": payload.command}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
