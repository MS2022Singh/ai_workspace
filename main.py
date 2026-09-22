from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from core.toggle_handler import ToolController
from core.executor import CommandExecutor

app = FastAPI(title="AI Workspace OS")
controller = ToolController()
executor = CommandExecutor()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/toggle")
async def toggle_tool(request: Request):
    data = await request.json()
    result = controller.set_tool_state(data.get("tool"), data.get("enabled"))
    return result

@app.post("/api/execute")
async def execute_command(request: Request):
    data = await request.json()
    return executor.run(data.get("command", ""))
