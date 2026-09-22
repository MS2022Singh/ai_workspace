import os
import subprocess

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:  # Fix: Only attempt to create directories if a directory path exists
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("[+] Upgrading UI to Unified App/OS Command Center...")

# 1. Update main.py to serve standard static files correctly
main_py_content = """from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="AI Workspace OS")

# Ensure static directories exist
os.makedirs("ui/frontend", exist_ok=True)
app.mount("/static", StaticFiles(directory="ui/frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("ui/frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/health")
async def health_check():
    return {"status": "Command Center Active"}
"""
write_file("main.py", main_py_content)

# 2. Generate the Comprehensive index.html
index_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Workspace OS | Command Center</title>
    <link rel="stylesheet" href="/static/styles.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="os-container">
        <!-- Left Sidebar: Navigation -->
        <aside class="nav-sidebar">
            <div class="logo">
                <i class="fas fa-brain"></i>
                <span>OS Core</span>
            </div>
            <nav class="nav-menu">
                <button class="nav-btn active" data-target="chat-panel"><i class="fas fa-comment-dots"></i> Chat & Tasks</button>
                <button class="nav-btn" data-target="research-panel"><i class="fas fa-search"></i> Research</button>
                <button class="nav-btn" data-target="code-panel"><i class="fas fa-code"></i> Code & Build</button>
                <button class="nav-btn" data-target="media-panel"><i class="fas fa-photo-video"></i> Files & Media</button>
                <button class="nav-btn" data-target="system-panel"><i class="fas fa-terminal"></i> System</button>
            </nav>
            <div class="nav-bottom">
                <button class="icon-btn" id="btn-screenshot" title="Take Screenshot (Ctrl+Shift+S)"><i class="fas fa-camera"></i></button>
                <button class="icon-btn" id="btn-help" title="Help Information"><i class="fas fa-info-circle"></i></button>
            </div>
        </aside>

        <!-- Main Content Area -->
        <main class="main-workspace">
            
            <!-- Panel: Chat & Tasks (Default) -->
            <section id="chat-panel" class="workspace-panel active">
                <div class="chat-stream" id="chat-stream">
                    <div class="message system-msg">
                        <div class="msg-avatar"><i class="fas fa-robot"></i></div>
                        <div class="msg-content">
                            <p><strong>System Online.</strong> AI Workspace initialized. Awaiting commands.</p>
                        </div>
                    </div>
                </div>
                <div class="input-area">
                    <div class="input-wrapper">
                        <button class="attach-btn" title="Upload/Drag-Drop"><i class="fas fa-paperclip"></i></button>
                        <textarea id="main-input" placeholder="Enter task, command, or prompt... (Press Enter to submit, Shift+Enter for new line)" rows="1"></textarea>
                        <button class="send-btn" id="send-btn"><i class="fas fa-paper-plane"></i></button>
                    </div>
                </div>
            </section>

            <!-- Panel: Files & Media (Conversion & Editors) -->
            <section id="media-panel" class="workspace-panel hidden">
                <div class="panel-header"><h2>Files, Media & Conversion</h2></div>
                <div class="drop-zone" id="file-drop-zone">
                    <i class="fas fa-cloud-upload-alt fa-3x"></i>
                    <p>Drag & Drop files here, or click to upload</p>
                    <span class="sub-text">Supports conversion, compression, and editing</span>
                </div>
                <div class="conversion-tools">
                    <button class="action-btn"><i class="fas fa-file-pdf"></i> PDF Tools</button>
                    <button class="action-btn"><i class="fas fa-image"></i> Image Editor</button>
                    <button class="action-btn"><i class="fas fa-video"></i> Video Compress</button>
                    <button class="action-btn"><i class="fas fa-music"></i> Audio Extract</button>
                </div>
            </section>

            <!-- Panel: Code -->
            <section id="code-panel" class="workspace-panel hidden">
                <div class="panel-header"><h2>Code & Repository Operations</h2></div>
                <div class="code-workspace">
                    <div class="repo-input">
                        <input type="text" placeholder="Paste GitHub URL or Tool link for Auto-Incorporation...">
                        <button class="action-btn">Analyze & Merge</button>
                    </div>
                </div>
            </section>
        </main>

        <!-- Right Sidebar: Tool Registry & Toggles -->
        <aside class="tool-sidebar">
            <div class="tool-header">
                <h3>Active Tools & Repos</h3>
                <span class="status-indicator live"></span>
            </div>
            <div class="tool-list">
                <div class="tool-item">
                    <span class="tool-name">Web Search (Crawl4AI)</span>
                    <label class="toggle-switch">
                        <input type="checkbox" checked>
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="tool-item">
                    <span class="tool-name">Local LLM (Qwen)</span>
                    <label class="toggle-switch">
                        <input type="checkbox" checked>
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="tool-item">
                    <span class="tool-name">Coding Agent (OpenHands)</span>
                    <label class="toggle-switch">
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="tool-item">
                    <span class="tool-name">System Control (PowerShell)</span>
                    <label class="toggle-switch">
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>
                 <div class="tool-item">
                    <span class="tool-name">Image Gen (Fooocus)</span>
                    <label class="toggle-switch">
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
        </aside>
    </div>
    <script src="/static/app.js"></script>
</body>
</html>
"""
write_file("ui/frontend/index.html", index_html_content)

# 3. Generate CSS
styles_css_content = """
:root {
    --bg-dark: #0f111a;
    --bg-panel: #1a1d27;
    --bg-input: #232736;
    --text-main: #e2e8f0;
    --text-muted: #94a3b8;
    --accent: #3b82f6;
    --accent-hover: #2563eb;
    --border: #2d3748;
    --success: #10b981;
}

* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
body { background-color: var(--bg-dark); color: var(--text-main); height: 100vh; overflow: hidden; }

.os-container { display: flex; height: 100vh; width: 100vw; }

/* Left Sidebar */
.nav-sidebar { width: 220px; background-color: var(--bg-panel); border-right: 1px solid var(--border); display: flex; flex-direction: column; padding: 15px; }
.logo { display: flex; align-items: center; gap: 10px; font-size: 1.2rem; font-weight: bold; margin-bottom: 30px; color: var(--accent); }
.nav-menu { display: flex; flex-direction: column; gap: 8px; flex-grow: 1; }
.nav-btn { background: none; border: none; color: var(--text-muted); text-align: left; padding: 10px 15px; border-radius: 6px; cursor: pointer; transition: 0.2s; font-size: 0.95rem; display: flex; align-items: center; gap: 10px; }
.nav-btn:hover, .nav-btn.active { background-color: var(--bg-input); color: var(--text-main); }
.nav-bottom { display: flex; gap: 10px; border-top: 1px solid var(--border); padding-top: 15px; }
.icon-btn { background: var(--bg-input); border: 1px solid var(--border); color: var(--text-muted); padding: 8px 12px; border-radius: 6px; cursor: pointer; }
.icon-btn:hover { color: var(--text-main); }

/* Main Workspace */
.main-workspace { flex-grow: 1; display: flex; flex-direction: column; background-color: var(--bg-dark); position: relative; }
.workspace-panel { display: none; flex-direction: column; height: 100%; padding: 20px; }
.workspace-panel.active { display: flex; }
.panel-header { margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 10px; }

/* Chat Panel */
.chat-stream { flex-grow: 1; overflow-y: auto; padding: 10px; display: flex; flex-direction: column; gap: 20px; }
.message { display: flex; gap: 15px; max-width: 85%; }
.message.system-msg .msg-avatar { color: var(--accent); }
.message.user-msg { flex-direction: row-reverse; align-self: flex-end; }
.message.user-msg .msg-content { background-color: var(--bg-input); border-radius: 12px 12px 0 12px; padding: 12px 16px; }
.msg-avatar { font-size: 1.5rem; }
.msg-content { background-color: var(--bg-panel); padding: 12px 16px; border-radius: 12px 12px 12px 0; line-height: 1.5; }

/* Input Area */
.input-area { padding: 20px; border-top: 1px solid var(--border); background: var(--bg-dark); }
.input-wrapper { display: flex; align-items: center; background-color: var(--bg-input); border: 1px solid var(--border); border-radius: 8px; padding: 5px 15px; }
.attach-btn { background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 10px; font-size: 1.1rem; }
textarea { flex-grow: 1; background: transparent; border: none; color: var(--text-main); padding: 12px; resize: none; font-size: 1rem; outline: none; }
.send-btn { background: var(--accent); border: none; color: white; padding: 10px 15px; border-radius: 6px; cursor: pointer; transition: 0.2s; }
.send-btn:hover { background: var(--accent-hover); }

/* File Drop Zone */
.drop-zone { border: 2px dashed var(--border); border-radius: 12px; padding: 50px; text-align: center; color: var(--text-muted); cursor: pointer; transition: 0.2s; margin-bottom: 20px; }
.drop-zone:hover { border-color: var(--accent); background: rgba(59, 130, 246, 0.05); }
.sub-text { display: block; font-size: 0.85rem; margin-top: 10px; opacity: 0.7; }
.conversion-tools { display: flex; gap: 15px; }
.action-btn { background: var(--bg-input); border: 1px solid var(--border); color: var(--text-main); padding: 10px 20px; border-radius: 6px; cursor: pointer; flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px; }
.repo-input { display: flex; gap: 10px; }
.repo-input input { flex-grow: 1; padding: 12px; background: var(--bg-input); border: 1px solid var(--border); color: white; border-radius: 6px; }

/* Right Sidebar (Tools) */
.tool-sidebar { width: 260px; background-color: var(--bg-panel); border-left: 1px solid var(--border); padding: 20px; overflow-y: auto; }
.tool-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
.status-indicator.live { height: 10px; width: 10px; background-color: var(--success); border-radius: 50%; box-shadow: 0 0 8px var(--success); }
.tool-list { display: flex; flex-direction: column; gap: 15px; }
.tool-item { display: flex; justify-content: space-between; align-items: center; padding: 10px; background: var(--bg-dark); border-radius: 6px; border: 1px solid var(--border); }
.tool-name { font-size: 0.9rem; }

/* Toggles */
.toggle-switch { position: relative; display: inline-block; width: 40px; height: 20px; }
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: var(--border); transition: .4s; border-radius: 20px; }
.slider:before { position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px; background-color: white; transition: .4s; border-radius: 50%; }
input:checked + .slider { background-color: var(--success); }
input:checked + .slider:before { transform: translateX(20px); }
.hidden { display: none !important; }
"""
write_file("ui/frontend/styles.css", styles_css_content)

# 4. Generate JavaScript
app_js_content = """
document.addEventListener("DOMContentLoaded", () => {
    // Panel Switching Logic
    const navButtons = document.querySelectorAll(".nav-btn");
    const panels = document.querySelectorAll(".workspace-panel");

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            navButtons.forEach(b => b.classList.remove("active"));
            panels.forEach(p => p.classList.add("hidden"));
            
            btn.classList.add("active");
            document.getElementById(btn.dataset.target).classList.remove("hidden");
        });
    });

    // Chat Input Logic
    const chatInput = document.getElementById("main-input");
    const sendBtn = document.getElementById("send-btn");
    const chatStream = document.getElementById("chat-stream");

    const sendMessage = () => {
        const text = chatInput.value.trim();
        if (!text) return;

        // Append User Message
        const userMsg = document.createElement("div");
        userMsg.className = "message user-msg";
        userMsg.innerHTML = `<div class="msg-content"><p>${text}</p></div>`;
        chatStream.appendChild(userMsg);
        
        chatInput.value = "";
        chatStream.scrollTop = chatStream.scrollHeight;

        // Simulate backend routing call
        setTimeout(() => {
            const sysMsg = document.createElement("div");
            sysMsg.className = "message system-msg";
            sysMsg.innerHTML = `<div class="msg-avatar"><i class="fas fa-robot"></i></div>
                                <div class="msg-content"><p>Command received. Routing through internal Event Bus...</p></div>`;
            chatStream.appendChild(sysMsg);
            chatStream.scrollTop = chatStream.scrollHeight;
        }, 500);
    };

    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    sendBtn.addEventListener("click", sendMessage);

    // File Drag and Drop Simulation
    const dropZone = document.getElementById("file-drop-zone");
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.style.borderColor = "var(--accent)";
    });
    dropZone.addEventListener("dragleave", () => {
        dropZone.style.borderColor = "var(--border)";
    });
    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.style.borderColor = "var(--border)";
        alert("File registered for processing pipeline.");
    });
});
"""
write_file("ui/frontend/app.js", app_js_content)

print("[+] UI files successfully generated in ui/frontend/")

# 5. Commit to GitHub Memory
subprocess.run(["git", "add", "main.py", "ui/frontend/"])
subprocess.run(["git", "commit", "-m", "fix(ui): patch winerror 3 in dir creation, build command center interface"])
subprocess.run(["git", "push"])
print("[+] Pushed Phase 3 UI Refactor to GitHub.")
