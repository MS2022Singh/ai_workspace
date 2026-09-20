import os
import subprocess
import sys

def main():
    print("[+] Starting Phase 3: Interactive UI & Execution Engine...")

    # 1. Update Core Command Executor (core/executor.py)
    executor_py = """import subprocess

class CommandExecutor:
    def run(self, command: str):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
            output = result.stdout if result.stdout else result.stderr
            return {"status": "success", "command": command, "output": output.strip()}
        except subprocess.TimeoutExpired:
            return {"status": "error", "command": command, "output": "Command timed out after 15 seconds."}
        except Exception as e:
            return {"status": "error", "command": command, "output": str(e)}
"""
    with open("core/executor.py", "w", encoding="utf-8") as f:
        f.write(executor_py)
    print("  [?] File 'core/executor.py' written.")

    # 2. Update FastAPI Server (main.py)
    main_py = """from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from core.toggle_handler import ToolController
from core.executor import CommandExecutor

app = FastAPI(title="AI Workspace OS")
controller = ToolController()
executor = CommandExecutor()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/toggle")
async def toggle_tool(request: Request):
    data = await request.json()
    result = controller.set_tool_state(data.get("tool"), data.get("enabled"))
    return result

@app.post("/api/execute")
async def execute_command(request: Request):
    data = await request.json()
    return executor.run(data.get("command", ""))
"""
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(main_py)
    print("  [?] File 'main.py' updated with execution routes.")

    # 3. Generate Interactive Unified HTML (static/index.html)
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Workspace - Unified Command Center</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: monospace; }
        .active-tab { border-bottom: 2px solid #38bdf8; color: #38bdf8; }
        .view-section { display: none; height: 100%; flex-direction: column; }
        .view-section.active { display: flex; }
    </style>
</head>
<body class="h-screen flex flex-col">
    <!-- Top Navigation Header -->
    <header class="bg-slate-900 border-b border-slate-800 p-3 flex justify-between items-center">
        <div class="flex items-center gap-3">
            <h1 class="text-xl font-bold text-sky-400">AI WORKSPACE OS</h1>
            <span class="text-xs bg-sky-500/10 text-sky-400 px-2 py-1 rounded border border-sky-500/20">v1.0 Interactive</span>
        </div>
        <div class="flex gap-4 text-sm text-slate-400">
            <button id="tab-dashboard" class="active-tab px-3 py-1 font-semibold hover:text-white" onclick="switchTab('dashboard')">[Alt+1] Dashboard</button>
            <button id="tab-matrix" class="px-3 py-1 font-semibold hover:text-white" onclick="switchTab('matrix')">[Alt+2] Tool Matrix</button>
            <button id="tab-terminal" class="px-3 py-1 font-semibold hover:text-white" onclick="switchTab('terminal')">[Alt+3] Terminal</button>
        </div>
    </header>

    <!-- Main Workspace Area -->
    <div class="flex flex-1 overflow-hidden">
        <!-- Left Sidebar: Active Tools -->
        <aside class="w-72 bg-slate-900/50 border-r border-slate-800 p-4 overflow-y-auto flex flex-col gap-3">
            <h2 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">System Services</h2>
            <div id="tool-toggles" class="flex flex-col gap-2"></div>
        </aside>

        <!-- Dynamic Content View -->
        <main class="flex-1 p-4 overflow-hidden bg-slate-950 flex flex-col gap-4">
            
            <!-- Dashboard View -->
            <div id="view-dashboard" class="view-section active overflow-y-auto">
                <h2 class="text-2xl font-bold text-white mb-4">System Overview</h2>
                <div class="grid grid-cols-3 gap-4">
                    <div class="bg-slate-900 border border-slate-800 p-4 rounded">
                        <h3 class="text-slate-400 text-sm">Server Status</h3>
                        <p class="text-emerald-400 font-bold text-xl mt-1">ONLINE</p>
                    </div>
                    <div class="bg-slate-900 border border-slate-800 p-4 rounded">
                        <h3 class="text-slate-400 text-sm">Active Tools</h3>
                        <p class="text-sky-400 font-bold text-xl mt-1" id="dash-tool-count">38 Loaded</p>
                    </div>
                    <div class="bg-slate-900 border border-slate-800 p-4 rounded">
                        <h3 class="text-slate-400 text-sm">OS Host</h3>
                        <p class="text-white font-bold text-xl mt-1">Windows Core</p>
                    </div>
                </div>
            </div>

            <!-- Tool Matrix View -->
            <div id="view-matrix" class="view-section overflow-y-auto">
                <h2 class="text-2xl font-bold text-white mb-4">Integrated Repos & Capabilities</h2>
                <div id="matrix-grid" class="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <!-- Populated by JS -->
                </div>
            </div>

            <!-- Terminal View -->
            <div id="view-terminal" class="view-section overflow-y-auto bg-black p-4 rounded border border-slate-800">
                <div class="text-slate-400 text-sm mb-2">AI Workspace OS Terminal Session Started.</div>
                <div id="terminal-output" class="flex-1 overflow-y-auto pb-4"></div>
            </div>

            <!-- Bottom Interactive Command Input -->
            <div class="bg-slate-900 border border-slate-800 rounded p-2 flex gap-2 items-center mt-auto">
                <span class="text-sky-400 font-bold">&gt;</span>
                <input id="cmd-input" type="text" placeholder="Enter command (e.g., 'dir' or 'python --version')..." class="flex-1 bg-transparent text-white outline-none font-mono text-sm">
                <button id="btn-execute" class="bg-sky-600 hover:bg-sky-500 text-white px-4 py-1 text-sm rounded font-bold">Execute</button>
            </div>
        </main>
    </div>

    <script src="/static/app_bus.js"></script>
    <script src="/static/terminal.js"></script>
</body>
</html>
"""
    with open("static/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("  [?] File 'static/index.html' rewritten for interactivity.")

    # 4. Generate Enhanced Frontend Logic (static/app_bus.js)
    app_bus_js = """const categorizedTools = {
    "No-Code & Workflows": ["ToolJet", "n8n", "AppFlowy"],
    "Agents & Browsing": ["browser-use", "OpenHands", "AutoGPT", "CrewAI"],
    "Local LLMs & Inference": ["Ollama", "vLLM", "SGLang", "LiteLLM", "DeepSeek", "Qwen 2.5"],
    "Voice & Multimodal": ["Whisper", "Piper TTS", "Stirling PDF"],
    "RAG & Vectors": ["LangChain", "LlamaIndex", "ChromaDB", "Qdrant", "FAISS", "Unstructured"],
    "Core Infrastructure": ["FastAPI", "Docker Engine", "Kubernetes", "Git Automation", "SQLite Store", "PyPubSub Engine"],
    "App Packaging": ["Tauri Shell", "Electron Builder", "Capacitor", "PyInstaller"]
};

document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("tool-toggles");
    const matrix = document.getElementById("matrix-grid");
    let totalTools = 0;

    Object.entries(categorizedTools).forEach(([category, tools]) => {
        // Build Tool Matrix Cards
        const card = document.createElement("div");
        card.className = "bg-slate-900 border border-slate-800 p-4 rounded";
        card.innerHTML = `<h3 class="text-sky-400 font-bold border-b border-slate-700 pb-2 mb-3">${category}</h3>`;
        
        const list = document.createElement("ul");
        list.className = "text-sm text-slate-300 space-y-1";
        
        tools.forEach((tool) => {
            totalTools++;
            // Matrix Listing
            list.innerHTML += `<li><span class="text-emerald-500 mr-2">?</span>${tool}</li>`;
            
            // Sidebar Toggle
            if (sidebar && totalTools <= 15) { // Show first 15 in sidebar for brevity
                const div = document.createElement("div");
                div.className = "flex justify-between items-center text-xs p-2 bg-slate-800/50 rounded border border-slate-700/50";
                div.innerHTML = `<span class="text-slate-300 font-medium">${tool}</span>
                                 <input type="checkbox" checked onchange="toggleTool('${tool}', this.checked)" class="accent-sky-500 cursor-pointer">`;
                sidebar.appendChild(div);
            }
        });
        card.appendChild(list);
        if (matrix) matrix.appendChild(card);
    });

    document.getElementById("dash-tool-count").innerText = `${totalTools} Loaded`;
    
    // Keyboard shortcuts
    document.addEventListener("keydown", function(e) {
        if (e.altKey && e.key === "1") { switchTab("dashboard"); e.preventDefault(); }
        if (e.altKey && e.key === "2") { switchTab("matrix"); e.preventDefault(); }
        if (e.altKey && e.key === "3") { switchTab("terminal"); e.preventDefault(); }
        if (e.key === "Enter" && document.activeElement.id === "cmd-input") {
            document.getElementById("btn-execute").click();
            e.preventDefault();
        }
    });
});

function switchTab(tabName) {
    document.querySelectorAll(".view-section").forEach(el => el.classList.remove("active"));
    document.getElementById("view-" + tabName).classList.add("active");
    
    document.querySelectorAll("button[id^='tab-']").forEach(btn => btn.classList.remove("active-tab"));
    document.getElementById("tab-" + tabName).classList.add("active-tab");
}

function toggleTool(toolName, isEnabled) {
    fetch("/api/toggle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tool: toolName, enabled: isEnabled })
    }).catch(err => console.log("Backend offline."));
}
"""
    with open("static/app_bus.js", "w", encoding="utf-8") as f:
        f.write(app_bus_js)
    print("  [?] File 'static/app_bus.js' updated with interactive routing.")

    # 5. Generate Terminal Execution Script (static/terminal.js)
    terminal_js = """document.addEventListener("DOMContentLoaded", function() {
    const btn = document.getElementById("btn-execute");
    const input = document.getElementById("cmd-input");
    const outputView = document.getElementById("terminal-output");

    btn.addEventListener("click", async () => {
        const cmd = input.value.trim();
        if (!cmd) return;
        
        // Auto-switch to terminal tab on execution
        switchTab('terminal');

        const cmdLine = document.createElement("div");
        cmdLine.className = "text-sky-400 font-mono text-sm mt-3 font-bold";
        cmdLine.innerText = "C:\\\\AI_Workspace> " + cmd;
        outputView.appendChild(cmdLine);
        
        input.value = ""; 
        outputView.scrollTop = outputView.scrollHeight;
        
        try {
            const res = await fetch("/api/execute", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command: cmd })
            });
            const data = await res.json();
            
            const outLine = document.createElement("div");
            outLine.className = data.status === "success" 
                ? "text-slate-300 font-mono text-sm whitespace-pre-wrap mt-1" 
                : "text-red-400 font-mono text-sm whitespace-pre-wrap mt-1";
            outLine.innerText = data.output || "[Process completed]";
            outputView.appendChild(outLine);
            outputView.scrollTop = outputView.scrollHeight;
        } catch (err) {
            const errLine = document.createElement("div");
            errLine.className = "text-red-500 font-mono text-sm mt-1";
            errLine.innerText = "Error: Could not reach execution server.";
            outputView.appendChild(errLine);
        }
    });
});
"""
    with open("static/terminal.js", "w", encoding="utf-8") as f:
        f.write(terminal_js)
    print("  [?] File 'static/terminal.js' written.")

    # 6. Commit and Push
    print("[+] Committing Phase 3 interactive updates to GitHub...")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "feat(ui): interactive tab routing, structured tool matrix, and active terminal execution"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    
    print("\n[+] Phase 3 Successfully Executed & Pushed!")
    print("[!] Run 'uvicorn main:app --reload' to test the new UI.")

if __name__ == "__main__":
    main()
