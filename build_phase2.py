import os
import subprocess
import sys

def main():
    print("[+] Starting Phase 2: API & Server Integration...")
    
    # 1. Generate requirements.txt
    requirements = """fastapi
uvicorn
"""
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements)
    print("  [?] File 'requirements.txt' written.")

    # 2. Generate main.py (FastAPI Server)
    main_py = """from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from core.toggle_handler import ToolController

app = FastAPI(title="AI Workspace OS")
controller = ToolController()

# Mount the static directory so HTML/JS/CSS can be served
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    '''Serve the main Phase 1 UI Shell'''
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/toggle")
async def toggle_tool(request: Request):
    '''Handle tool toggling from the frontend event bus'''
    data = await request.json()
    tool = data.get("tool")
    enabled = data.get("enabled")
    
    # Update backend state
    result = controller.set_tool_state(tool, enabled)
    print(f"[Server Log] Tool State Updated: {result}")
    return result
"""
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(main_py)
    print("  [?] File 'main.py' written.")

    # 3. Install Requirements
    print("[+] Installing Python dependencies (FastAPI & Uvicorn)...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    # 4. Commit and Push
    print("[+] Committing Phase 2 files to GitHub...")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "feat(phase2): setup FastAPI server, routing, and requirements"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    
    print("\n[+] Phase 2 successfully executed and pushed to GitHub!")
    print("[!] To start your server, run: uvicorn main:app --reload")

if __name__ == "__main__":
    main()
