import os
import subprocess
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI(title="AI Workspace OS")

# Serve main index.html at root
@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

# Properly mount static folder for CSS/JS assets
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/api/execute")
async def execute_command(request: Request):
    data = await request.json()
    cmd = data.get("command", "").strip()
    if not cmd:
        return JSONResponse({"output": "No command provided."})
    
    if cmd.startswith("/ai "):
        query = cmd[4:]
        return JSONResponse({"output": f"[AI ORCHESTRATOR]: Processing request -> '{query}'"})
    elif cmd.startswith("/agent "):
        agent_req = cmd[7:]
        return JSONResponse({"output": f"[SPECIALIST AGENT ROUTER]: Task dispatched to agent -> '{agent_req}'"})
    else:
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            out = res.stdout if res.stdout else res.stderr
            return JSONResponse({"output": out if out else "Command executed successfully."})
        except Exception as e:
            return JSONResponse({"output": f"Execution error: {str(e)}"})

@app.post("/api/toggle")
async def toggle_tool(request: Request):
    data = await request.json()
    tool = data.get("tool")
    enabled = data.get("enabled")
    return JSONResponse({"status": "success", "tool": tool, "enabled": enabled})

if __name__ == "__main__":
    print("\n[+] Server active at http://127.0.0.1:8000")
    print("[+] Press Ctrl+C in this terminal to stop the server.\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
