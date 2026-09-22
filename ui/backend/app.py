from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from core.memory.project_memory import ProjectMemory

app = FastAPI(title="AI Workspace Dashboard", version="1.0")
memory = ProjectMemory()

@app.get("/api/status")
def get_status():
    return memory.load_memory()

@app.post("/api/memory/decision")
def add_decision(decision: str):
    memory.add_decision(decision)
    return {"status": "success", "state": memory.load_memory()}

@app.post("/api/memory/completed")
def add_completed(item: str):
    memory.log_completed_work(item)
    return {"status": "success", "state": memory.load_memory()}

# Serve static frontend files
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
