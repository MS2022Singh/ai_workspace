from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from core.toggle_handler import ToolController

app = FastAPI(title="AI Workspace OS")
controller = ToolController()

# Mount the static directory so HTML/JS/CSS can be served
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    '''Serve the main Phase 1 UI Shell'''
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/toggle")
async def toggle_tool(request: Request):
    '''Handle tool toggling from the frontend event bus'''
    data = await request.json()
    tool = data.get("tool")
    enabled = data.get("enabled")
    
    # Update backend state
    result = controller.set_tool_state(tool, enabled)
    print(f"[Server Log] Tool State Updated: {result}")
    return result
