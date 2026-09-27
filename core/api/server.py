
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.orchestrator import orchestrator

app = FastAPI(title='AI Workspace OS API', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class TaskRequest(BaseModel):
    task: str

@app.post('/api/execute')
async def execute_task(req: TaskRequest):
    await orchestrator.execute_task(req.task)
    return {'status': 'success', 'task': req.task, 'message': 'Task executed successfully.'}

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f'Echo: {data}')
    except:
        pass


@app.get("/")
async def root():
    return {"status": "online", "system": "AI Workspace OS API", "version": "1.0.0"}
