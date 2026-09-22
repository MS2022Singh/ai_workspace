import os
import subprocess

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("[+] Finalizing Command Center UI structure...")

# 1. Update HTML with Research and System Panels
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

            <!-- Panel: Research (Crawl4AI & Deep Search) -->
            <section id="research-panel" class="workspace-panel">
                <div class="panel-header"><h2>Deep Research & Crawling</h2></div>
                <div class="repo-input">
                    <input type="text" placeholder="Enter research topic or URL to crawl (e.g., 'Latest AI models' or 'https://...')">
                    <button class="action-btn"><i class="fas fa-spider"></i> Dispatch Crawler</button>
                </div>
                <div class="chat-stream mt-20" style="border: 1px dashed var(--border); border-radius: 8px;">
                    <div class="message system-msg">
                        <div class="msg-avatar"><i class="fas fa-info-circle"></i></div>
                        <div class="msg-content">
                            <p>Research module standing by. Awaiting targets.</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Panel: Files & Media (Conversion & Editors) -->
            <section id="media-panel" class="workspace-panel">
                <div class="panel-header"><h2>Files, Media & Conversion</h2></div>
                <div class="drop-zone" id="file-drop-zone">
                    <i class="fas fa-cloud-upload-alt fa-3x"></i>
                    <p>Drag & Drop files here, or click to upload</p>
                    <span class="sub-text">Supports format conversion, data extraction, and visual analysis</span>
                </div>
                <div class="conversion-tools">
                    <button class="action-btn"><i class="fas fa-file-pdf"></i> PDF Tools</button>
                    <button class="action-btn"><i class="fas fa-image"></i> Image Editor</button>
                    <button class="action-btn"><i class="fas fa-video"></i> Video Compress</button>
                    <button class="action-btn"><i class="fas fa-music"></i> Audio Extract</button>
                </div>
            </section>

            <!-- Panel: Code -->
            <section id="code-panel" class="workspace-panel">
                <div class="panel-header"><h2>Code & Repository Operations</h2></div>
                <div class="code-workspace">
                    <div class="repo-input">
                        <input type="text" placeholder="Paste GitHub URL or Tool link for Auto-Incorporation...">
                        <button class="action-btn"><i class="fas fa-code-branch"></i> Analyze & Merge</button>
                    </div>
                </div>
                <div class="chat-stream mt-20" style="background: var(--bg-input); border-radius: 8px;">
                    <pre style="padding: 15px; color: var(--text-muted); font-family: monospace;">// Code analysis workspace loaded.
// Ready to invoke OpenHands or Qwen logic.</pre>
                </div>
            </section>

            <!-- Panel: System -->
            <section id="system-panel" class="workspace-panel">
                <div class="panel-header"><h2>System & Environment Control</h2></div>
                <div class="system-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px; border: 1px solid var(--border);">
                        <h3 style="margin-bottom: 15px;"><i class="fas fa-key"></i> API Configuration</h3>
                        <input type="password" placeholder="OpenAI API Key" style="width: 100%; padding: 10px; margin-bottom: 10px; background: var(--bg-dark); border: 1px solid var(--border); color: white; border-radius: 4px;">
                        <input type="password" placeholder="Anthropic API Key" style="width: 100%; padding: 10px; margin-bottom: 10px; background: var(--bg-dark); border: 1px solid var(--border); color: white; border-radius: 4px;">
                        <button class="action-btn" style="width: 100%;">Save Configuration</button>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px; border: 1px solid var(--border);">
                        <h3 style="margin-bottom: 15px;"><i class="fas fa-terminal"></i> Local Terminal Output</h3>
                        <div class="terminal-window" style="background: #000; padding: 10px; border-radius: 4px; font-family: monospace; color: #0f0; height: 110px; overflow-y: auto;">
                            <p>PS C:\AI_Workspace\ai_workspace_core> </p>
                        </div>
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

# 2. Update JavaScript to correctly toggle '.active' instead of '.hidden'
app_js_content = """
document.addEventListener("DOMContentLoaded", () => {
    // Panel Switching Logic - FIXED
    const navButtons = document.querySelectorAll(".nav-btn");
    const panels = document.querySelectorAll(".workspace-panel");

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            // Remove active states from all buttons and panels
            navButtons.forEach(b => b.classList.remove("active"));
            panels.forEach(p => p.classList.remove("active"));
            
            // Add active state to clicked button and targeted panel
            btn.classList.add("active");
            document.getElementById(btn.dataset.target).classList.add("active");
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

# 3. Quick CSS utility patch
css_patch = """
.mt-20 { margin-top: 20px; }
.mt-10 { margin-top: 10px; }
"""
with open("ui/frontend/styles.css", "a", encoding="utf-8") as f:
    f.write(css_patch)

# 4. Commit to GitHub Memory
subprocess.run(["git", "add", "ui/frontend/"])
subprocess.run(["git", "commit", "-m", "fix(ui): inject missing Research/System panels, correct JS tab routing logic"])
subprocess.run(["git", "push"])
print("[+] UI logic fixed and new panels injected. Pushed to GitHub.")
