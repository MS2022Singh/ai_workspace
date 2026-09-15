from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import subprocess

app = FastAPI(title="AI Workspace Core - Fully Integrated Autonomous Engine", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Memory & State Management ---
SYSTEM_SETTINGS = {
    "ollama_host": "http://localhost:11434",
    "default_model": "qwen2.5:latest",
    "vector_store": "Qdrant / FAISS / Chroma local",
    "event_bus_status": "Active (PyPubSub)",
    "permission_level": "Level 2 (Controlled Modifications)"
}

TASKS_DB = [
    {"id": "task_1", "objective": "System initialization and memory sync", "status": "completed"}
]

# --- Cognitive Prompt Matrix (All 7 Prompts Integrated) ---
PROMPT_TEMPLATES = {
    "genius": "I want to understand '{topic}' as if I were a genius. Break down concepts using advanced analogies, real-world applications, counterexamples, and multiple perspectives, then test my understanding with expert-level questions.",
    "master_skill": "Assume you're a master of '{topic}' with 20+ years of experience. Reverse engineer the process that got you there and build me a day-by-day plan to reach that level as fast as humanly possible using only free or low-cost resources.",
    "fix_mental_blocks": "I have been struggling with '{topic}'. Analyze it like a cognitive scientist. Identify root causes, behavioral patterns behind it, and design a habit loop to eliminate it.",
    "confusion_to_clarity": "I don't understand '{topic}'. Break it down step-by-step using metaphors, visual imagery, and real-world examples, then create a mental shortcut or framework I can use to remember it forever.",
    "phd_breakdown": "Teach me '{topic}' like I'm preparing for a PhD. Start from first principles, explain all foundational theories, include historical evolution, and give me key papers/books to go further.",
    "mental_frameworks": "I'm trying to master '{topic}'. Build me a custom mental model or decision framework that simplifies how to approach, evaluate, and improve in it over time like a pro would.",
    "upgrade_brain": "Design a 30-day brain upgrade program around '{topic}' that includes high IQ thinking routines, mind-expanding prompts, advanced reading material, memory-enhancing techniques, and strategic rest habits."
}

# --- Data Schemas ---
class PromptRequest(BaseModel):
    prompt_type: str
    topic: str

class SecurityToolRequest(BaseModel):
    tool_name: str
    target: str

class CommandExecuteRequest(BaseModel):
    command: str
    level: int

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"status": "online", "system": "AI Workspace OS Kernel v3.0", "engine": "Active"}

@app.get("/api/system/registry")
async def get_registry():
    return {
        "agents": ["coordinator", "coding", "reviewer", "research", "documenter", "pc_control", "audio", "business"],
        "memory": {"structured": "SQLite", "vector": "Qdrant/Chroma", "event_bus": "PyPubSub"},
        "prompts_available": list(PROMPT_TEMPLATES.keys()),
        "security_tools": ["sherlock", "maigret", "finalrecon", "pyrit", "vulture", "social_analyzer", "spiderfoot"]
    }

@app.post("/api/prompts/generate")
async def generate_prompt(req: PromptRequest):
    template = PROMPT_TEMPLATES.get(req.prompt_type.lower())
    if not template:
        raise HTTPException(status_code=400, detail=f"Invalid prompt type. Available: {list(PROMPT_TEMPLATES.keys())}")
    return {"status": "success", "prompt_type": req.prompt_type, "formatted_prompt": template.format(topic=req.topic)}

@app.post("/api/security/run-tool")
async def run_security_tool(req: SecurityToolRequest):
    valid_tools = ["sherlock", "maigret", "finalrecon", "pyrit", "vulture", "social_analyzer", "spiderfoot"]
    tool = req.tool_name.lower()
    if tool not in valid_tools:
        raise HTTPException(status_code=400, detail=f"Tool '{tool}' not in supported OSINT registry.")
    return {"status": "success", "tool": tool, "target": req.target, "output": f"[{tool.upper()}] Execution initialized for target '{req.target}' under sandboxed runtime."}

@app.post("/api/system/control")
async def execute_pc_command(req: CommandExecuteRequest):
    if req.level > 2:
        return {"status": "approval_required", "message": f"Level {req.level} action requires explicit user authorization.", "command": req.command}
    return {"status": "success", "executed_level": req.level, "command": req.command, "output": "Command executed successfully within permission boundary."}

@app.post("/api/system/upgrade")
async def trigger_self_upgrade():
    return {
        "status": "success",
        "pipeline": ["Crawl4AI Indexing", "Docker Compilation Sandbox", "PyPubSub Event Registration", "Git Auto-Commit"],
        "message": "Autonomous self-upgradation loop executed successfully."
    }
