import uvicorn
import os
import sys

# Ensure backend module paths resolve in bundled environment
sys.path.insert(0, os.path.dirname(__file__))

from backend.app import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
