import uvicorn
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("============================================================")
    print("Starting AI Workspace (Headless Mode) on port 8765")
    print("============================================================")
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8765, reload=False)
