import webview
import threading
import uvicorn
import time
from app import app

def run_server():
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='error')

if __name__ == '__main__':
    # Start FastAPI server in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Allow server to spin up

    # Create PyWebView window pointing to local HTML or FastAPI endpoint
    webview.create_window('AI Workspace OS', 'app.html', width=1280, height=800)
    webview.start()
