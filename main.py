from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="AI Workspace OS")

# Ensure static directories exist
os.makedirs("ui/frontend", exist_ok=True)
app.mount("/static", StaticFiles(directory="ui/frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("ui/frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/health")
async def health_check():
    return {"status": "Command Center Active"}
