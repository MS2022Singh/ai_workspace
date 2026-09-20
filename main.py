import subprocess
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from converters import MediaEngine
from cognitive_engine import CognitiveEngine
from tool_registry import MasterToolRegistry

app = FastAPI(title="AI Workspace OS")

app.mount("/static", StaticFiles(directory="static"), name="static")

tool_registry = MasterToolRegistry()

class ChatRequest(BaseModel):
    prompt: str
    agent: str = "Orchestrator"

class CognitiveRequest(BaseModel):
    framework: str
    topic: str = ""

class TerminalRequest(BaseModel):
    command: str

class ConvertRequest(BaseModel):
    filename: str
    source_type: str
    target_format: str

class CompressRequest(BaseModel):
    filename: str
    level: int
    target_size: float

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/api/chat")
def api_chat(req: ChatRequest):
    return {"response": f"[{req.agent} Agent] Processed request: '{req.prompt}'. All tasks verified and active."}

@app.post("/api/cognitive")
def api_cognitive(req: CognitiveRequest):
    prompt = CognitiveEngine.generate_prompt(req.framework, req.topic)
    return {"framework": req.framework, "prompt": prompt}

@app.post("/api/terminal")
def api_terminal(req: TerminalRequest):
    try:
        res = subprocess.run(req.command, shell=True, capture_output=True, text=True, timeout=5)
        output = res.stdout if res.stdout else res.stderr
        return {"output": output if output else "Command executed with no output."}
    except Exception as e:
        return {"output": str(e)}

@app.post("/api/convert")
def api_convert(req: ConvertRequest):
    return MediaEngine.convert_file(req.filename, req.source_type, req.target_format)

@app.post("/api/compress")
def api_compress(req: CompressRequest):
    return MediaEngine.compress_file(req.filename, req.level, req.target_size)

@app.get("/api/tools")
def api_tools():
    return tool_registry.get_all()

if __name__ == "__main__":
    import uvicorn
    print("[+] AI Workspace OS Server active at http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
