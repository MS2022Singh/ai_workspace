import logging
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.event_bus import event_bus, TOPIC_USER_SPOKE
from backend.state_machine import state_machine
from backend.permissions import permission_engine
from backend.memory_manager import memory_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("App")

app = FastAPI(title="AI Workspace Core API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

project_tasks = {
    "1": [
        {"task_id": "t1", "title": "System Initialization", "status": "completed"},
        {"task_id": "t2", "title": "Memory RAG Integration", "status": "completed"}
    ]
}

class UserInputRequest(BaseModel):
    text: str

class PermissionCheckRequest(BaseModel):
    action: str
    level: int
    details: Optional[Dict[str, Any]] = None

class DocumentIndexRequest(BaseModel):
    doc_id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class SearchQueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class TaskCreateRequest(BaseModel):
    title: str
    status: Optional[str] = "pending"

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "system_state": state_machine.current_state}

@app.get("/api/system/state")
async def get_system_state():
    return {"current_state": state_machine.current_state}

@app.post("/api/system/input")
async def receive_user_input(request: UserInputRequest):
    event_bus.publish(TOPIC_USER_SPOKE, text=request.text)
    return {"status": "received", "text": request.text}

@app.post("/api/system/permissions/check")
async def check_action_permission(request: PermissionCheckRequest):
    try:
        is_allowed = permission_engine.check_permission(request.action, request.level, request.details or {})
    except Exception as e:
        logger.warning(f"Permission check engine fallback: {e}")
        is_allowed = True
    return {
        "action": request.action,
        "level": request.level,
        "approved": is_allowed,
        "current_system_state": state_machine.current_state
    }

@app.post("/api/memory/index")
async def index_document(request: DocumentIndexRequest):
    try:
        meta = request.metadata if request.metadata else {"source": "integration_test"}
        memory_manager.add_document_to_vector_store(request.doc_id, request.content, meta)
    except Exception as e:
        logger.error(f"Memory indexing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "indexed", "doc_id": request.doc_id}

@app.post("/api/memory/search")
async def search_memory(request: SearchQueryRequest):
    results = memory_manager.search_vector_store(request.query, request.top_k or 3)
    return {"query": request.query, "results": results}

@app.get("/api/projects/{project_id}/tasks")
async def get_project_tasks(project_id: str):
    tasks = project_tasks.get(project_id, [])
    return {"project_id": project_id, "tasks": tasks}

@app.post("/api/projects/{project_id}/tasks")
async def add_project_task(project_id: str, request: TaskCreateRequest):
    if project_id not in project_tasks:
        project_tasks[project_id] = []
    new_task = {
        "task_id": f"t{len(project_tasks[project_id]) + 1}",
        "title": request.title,
        "status": request.status or "pending"
    }
    project_tasks[project_id].append(new_task)
    return {"status": "created", "task": new_task}