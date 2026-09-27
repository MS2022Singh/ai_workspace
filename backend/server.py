import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.event_bus import AIWorkspaceEventBus, TaskExecutionEngine

app = FastAPI(title="AI Workspace Command Center")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()
event_bus = AIWorkspaceEventBus()

def event_listener(event):
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(manager.broadcast(json.dumps(event)), loop)
    except RuntimeError:
        pass

event_bus.subscribe(event_listener)
engine = TaskExecutionEngine(event_bus)

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            task_text = payload.get("task", "Default Task")
            
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, engine.execute_task, task_text)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Mount frontend static directory to serve index.html at root
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.server:app", host="127.0.0.1", port=8000, reload=True)
