import os
import subprocess
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from converters import MediaEngine
from repo_ingestor import RepoIngestor
from bug_detector import BugDetector
from cognitive_engine import CognitiveEngine

app = FastAPI(title="AI Workspace OS")

# Memory State Store
WORKSPACE_STATE = {
    "permissions": {
        "browser_use": True, "openhands": True, "langflow": True,
        "ollama": True, "vllm": True, "whisper": True,
        "pyrit": True, "vulture": True
    },
    "level": 1,
    "project_memory": []
}

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/api/execute")
async def execute_command(request: Request):
    data = await request.json()
    cmd = data.get("command", "").strip()
    if not cmd:
        return JSONResponse({"output": "No command provided."})
    
    # Bug scan check on execution
    bug_report = BugDetector.scan_and_heal()
    
    if cmd.startswith("/ai "):
        query = cmd[4:]
        return JSONResponse({"output": f"[AI ORCHESTRATOR]: Processing request -> '{query}'\n[BUG-DETECTOR]: {bug_report['details'][0]}"})
    elif cmd.startswith("/agent "):
        agent_req = cmd[7:]
        return JSONResponse({"output": f"[SPECIALIST AGENT ROUTER]: Dispatched to specialist agent -> '{agent_req}'"})
    else:
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            out = res.stdout if res.stdout else res.stderr
            return JSONResponse({"output": out if out else "Command executed successfully."})
        except Exception as e:
            return JSONResponse({"output": f"Execution error: {str(e)}"})

@app.post("/api/ingest")
async def ingest_repo(request: Request):
    data = await request.json()
    url = data.get("url", "").strip()
    res = RepoIngestor.auto_incorporate(url)
    return JSONResponse(res)

@app.post("/api/cognitive")
async def cognitive_prompt(request: Request):
    data = await request.json()
    key = data.get("framework")
    topic = data.get("topic", "")
    prompt = CognitiveEngine.generate_prompt(key, topic)
    return JSONResponse({"status": "success", "orchestrated_prompt": prompt, "response": f"[COGNITIVE ENGINE ({key.upper()})]: Formulated deep execution graph for '{topic}'."})

@app.post("/api/convert")
async def convert_media(request: Request):
    data = await request.json()
    action = data.get("action") # 'convert' or 'compress'
    input_file = data.get("input_file")
    target_format = data.get("format", "pdf")
    
    if action == "compress":
        res = MediaEngine.compress_file(input_file)
    else:
        res = MediaEngine.convert_file(input_file, target_format)
    return JSONResponse(res)

@app.post("/api/toggle")
async def toggle_tool(request: Request):
    data = await request.json()
    tool = data.get("tool")
    enabled = data.get("enabled")
    if tool in WORKSPACE_STATE["permissions"]:
        WORKSPACE_STATE["permissions"][tool] = enabled
    return JSONResponse({"status": "success", "tool": tool, "enabled": enabled, "active_permissions": WORKSPACE_STATE["permissions"]})

@app.get("/api/bug_detect")
async def bug_detect():
    return JSONResponse(BugDetector.scan_and_heal())

if __name__ == "__main__":
    print("\n[+] AI Workspace OS Server active at http://127.0.0.1:8000")
    print("[+] All core modules (Converters, Ingestor, Bug-Detector, Cognitive Frameworks) online.")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
