from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI(title='AI Workspace Core')

@app.get('/')
def serve_ui():
    index_path = os.path.join('frontend', 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {'status': 'online', 'message': 'AI Workspace Core API running'}
