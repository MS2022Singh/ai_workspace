from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pubsub import pub
import json
import asyncio

app = FastAPI(title="AI OS Command Center API")

# Allow UI to connect across different localhost ports
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

# Listener: Bridge outgoing PyPubSub events to the WebSocket
def pubsub_to_ws(topic=pub.AUTO_TOPIC, **kwargs):
    topic_name = topic.getName() if hasattr(topic, 'getName') else str(topic)
    payload = {"topic": topic_name, "payload": kwargs}
    
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(manager.broadcast(json.dumps(payload)))
    except RuntimeError:
        pass # Handle cases where there is no running event loop

# Subscribe to all backend events
pub.subscribe(pubsub_to_ws, pub.ALL_TOPICS)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive UI commands from WebSocket
            data = await websocket.receive_text()
            message = json.loads(data)
            topic = message.get("topic")
            payload = message.get("payload", {})
            
            if topic:
                # Route UI commands directly into the Python Event Bus
                pub.sendMessage(topic, **payload)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)
        print(f"WebSocket Error: {e}")

@app.get("/")
def read_root():
    return {"status": "AI OS Event Bus is live", "websocket": "ws://localhost:8000/ws"}
