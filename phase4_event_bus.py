import os
import subprocess

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("[+] Executing Phase 4: Event Bus Integration...")

# 1. Update main.py to include the API router
main_py_content = """from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="AI Workspace OS Core")

# Mount static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="ui/frontend"), name="static")

# Event Bus Data Model
class CommandPayload(BaseModel):
    source_panel: str
    command: str
    parameters: dict = {}

@app.get("/")
async def serve_ui():
    return FileResponse("ui/frontend/index.html")

# Phase 4: Central Event Bus Endpoint
@app.post("/api/command")
async def process_command(payload: CommandPayload):
    # Log incoming command to terminal
    print(f"\\n[EVENT BUS] Received from {payload.source_panel}: {payload.command}")
    
    # Basic routing logic (to be expanded with actual AI agents later)
    response_msg = f"Task received by core bus. Target: {payload.source_panel}. Execution pending integration."
    
    if payload.source_panel == "research-panel":
        response_msg = f"Initializing Crawl4AI sequence for target: {payload.command}"
    elif payload.source_panel == "code-panel":
        response_msg = f"Analyzing repository logic for: {payload.command}"
    elif payload.source_panel == "system-panel":
        response_msg = "System configuration updated securely."

    return {"status": "success", "message": response_msg, "echo": payload.command}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
"""
write_file("main.py", main_py_content)

# 2. Update app.js to use fetch() API instead of setTimeout
app_js_patch = """
document.addEventListener("DOMContentLoaded", () => {
    const navButtons = document.querySelectorAll(".nav-btn");
    const panels = document.querySelectorAll(".workspace-panel");
    let activePanelId = "chat-panel"; // Default tracking

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            navButtons.forEach(b => b.classList.remove("active"));
            panels.forEach(p => p.classList.remove("active"));
            btn.classList.add("active");
            activePanelId = btn.dataset.target;
            document.getElementById(activePanelId).classList.add("active");
        });
    });

    const chatInput = document.getElementById("main-input");
    const sendBtn = document.getElementById("send-btn");
    const chatStream = document.getElementById("chat-stream");

    // Phase 4: Async backend communication
    const sendToEventBus = async (commandText, source) => {
        try {
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    source_panel: source,
                    command: commandText,
                    parameters: {}
                })
            });
            const data = await response.json();
            return data.message;
        } catch (error) {
            console.error("Bus Error:", error);
            return "Error: Event Bus connection failed.";
        }
    };

    const sendMessage = async () => {
        const text = chatInput.value.trim();
        if (!text) return;

        // Render User Message
        const userMsg = document.createElement("div");
        userMsg.className = "message user-msg";
        userMsg.innerHTML = `<div class="msg-content"><p>${text}</p></div>`;
        chatStream.appendChild(userMsg);
        chatInput.value = "";
        chatStream.scrollTop = chatStream.scrollHeight;

        // Await Backend Response
        const backendResponse = await sendToEventBus(text, activePanelId);
        
        // Render System Message
        const sysMsg = document.createElement("div");
        sysMsg.className = "message system-msg";
        sysMsg.innerHTML = `<div class="msg-avatar"><i class="fas fa-robot"></i></div>
                            <div class="msg-content"><p>${backendResponse}</p></div>`;
        chatStream.appendChild(sysMsg);
        chatStream.scrollTop = chatStream.scrollHeight;
    };

    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    sendBtn.addEventListener("click", sendMessage);

    // Panel Action Buttons Mapping
    document.querySelectorAll(".action-btn").forEach(btn => {
        btn.addEventListener("click", async (e) => {
            const btnText = e.target.innerText.trim();
            const parentInput = e.target.previousElementSibling;
            const command = parentInput && parentInput.tagName === "INPUT" ? parentInput.value : btnText;
            
            if(command) {
                const sysResponse = await sendToEventBus(command, activePanelId);
                alert(`System Response:\\n${sysResponse}`);
            }
        });
    });

    const dropZone = document.getElementById("file-drop-zone");
    if(dropZone) {
        dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.style.borderColor = "var(--accent)"; });
        dropZone.addEventListener("dragleave", () => { dropZone.style.borderColor = "var(--border)"; });
        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropZone.style.borderColor = "var(--border)";
            alert("File upload event triggered. Ready for backend pipeline.");
        });
    }
});
"""
write_file("ui/frontend/app.js", app_js_patch)

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "feat(backend): implement Phase 4 Event Bus API and rewire JS frontend"])
subprocess.run(["git", "push"])
print("[+] Phase 4 Event Bus deployed. Pushed to GitHub.")
