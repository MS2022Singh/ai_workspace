import os
import subprocess

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("[+] Aligning UI with Master Prompt requirements (Memory, File Tree, Logs)...")

# 1. Update HTML with Project Memory and File Explorer
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
                <i class="fas fa-layer-group"></i>
                <span>OS Core</span>
            </div>
            <nav class="nav-menu">
                <button class="nav-btn active" data-target="chat-panel"><i class="fas fa-comment-dots"></i> Chat & Tasks</button>
                <button class="nav-btn" data-target="memory-panel"><i class="fas fa-brain"></i> Project Memory</button>
                <button class="nav-btn" data-target="research-panel"><i class="fas fa-search"></i> Research</button>
                <button class="nav-btn" data-target="code-panel"><i class="fas fa-code"></i> Code & Build</button>
                <button class="nav-btn" data-target="media-panel"><i class="fas fa-photo-video"></i> Files & Media</button>
                <button class="nav-btn" data-target="system-panel"><i class="fas fa-terminal"></i> System</button>
            </nav>
            <div class="nav-bottom">
                <button class="icon-btn" id="btn-screenshot" title="Take Screenshot"><i class="fas fa-camera"></i></button>
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
                            <p><strong>System Online.</strong> All sub-agents integrated. Event Bus listening.</p>
                        </div>
                    </div>
                </div>
                <div class="input-area">
                    <div class="input-wrapper">
                        <button class="attach-btn" title="Upload"><i class="fas fa-paperclip"></i></button>
                        <textarea id="main-input" placeholder="Enter task, command, or prompt..." rows="1"></textarea>
                        <button class="send-btn" id="send-btn"><i class="fas fa-paper-plane"></i></button>
                    </div>
                </div>
            </section>

            <!-- Panel: Project Memory (NEW) -->
            <section id="memory-panel" class="workspace-panel">
                <div class="panel-header"><h2>Project Memory & Tracking</h2></div>
                <div class="memory-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: calc(100% - 60px); overflow-y: auto;">
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-list-check"></i> Requirements & Scope</h3>
                        <textarea style="width: 100%; height: 150px; background: var(--bg-dark); color: var(--text-light); border: 1px solid var(--border); border-radius: 4px; padding: 10px; margin-top: 10px;" placeholder="Document project requirements here..."></textarea>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-spinner"></i> Progress & Pending Work</h3>
                        <textarea style="width: 100%; height: 150px; background: var(--bg-dark); color: var(--text-light); border: 1px solid var(--border); border-radius: 4px; padding: 10px; margin-top: 10px;" placeholder="Track completed and pending tasks..."></textarea>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px; grid-column: span 2;">
                        <h3><i class="fas fa-bug"></i> Issues & Decisions</h3>
                        <textarea style="width: 100%; height: 100px; background: var(--bg-dark); color: var(--text-light); border: 1px solid var(--border); border-radius: 4px; padding: 10px; margin-top: 10px;" placeholder="Log issues, testing results, and architectural decisions..."></textarea>
                        <button class="action-btn mt-10"><i class="fas fa-save"></i> Save to Memory File</button>
                    </div>
                </div>
            </section>

            <!-- Panel: Research -->
            <section id="research-panel" class="workspace-panel">
                <div class="panel-header"><h2>Deep Research & Crawling</h2></div>
                <div class="repo-input">
                    <input type="text" placeholder="Enter research topic or URL...">
                    <button class="action-btn"><i class="fas fa-spider"></i> Dispatch Crawler</button>
                </div>
                <div class="chat-stream mt-20" style="border: 1px dashed var(--border); border-radius: 8px;">
                    <div class="message system-msg">
                        <div class="msg-avatar"><i class="fas fa-info-circle"></i></div>
                        <div class="msg-content"><p>Research module standing by.</p></div>
                    </div>
                </div>
            </section>

            <!-- Panel: Code (UPDATED with File Tree) -->
            <section id="code-panel" class="workspace-panel">
                <div class="panel-header"><h2>Code & Repository Operations</h2></div>
                <div class="code-layout" style="display: flex; gap: 20px; height: calc(100% - 60px);">
                    <!-- File Explorer -->
                    <div class="file-tree" style="width: 250px; background: var(--bg-input); border-radius: 8px; padding: 15px; border: 1px solid var(--border); overflow-y: auto;">
                        <h4 style="margin-bottom: 10px; color: var(--text-muted);"><i class="fas fa-folder-open"></i> Workspace</h4>
                        <ul style="list-style: none; padding-left: 10px; color: var(--text-light); font-family: monospace; font-size: 13px; line-height: 1.8;">
                            <li><i class="fas fa-folder"></i> ui/
                                <ul style="list-style: none; padding-left: 15px;">
                                    <li><i class="fab fa-html5"></i> index.html</li>
                                    <li><i class="fab fa-css3"></i> styles.css</li>
                                    <li><i class="fab fa-js"></i> app.js</li>
                                </ul>
                            </li>
                            <li><i class="fab fa-python"></i> main.py</li>
                            <li><i class="fas fa-file-alt"></i> requirements.txt</li>
                        </ul>
                    </div>
                    <!-- Editor/Terminal -->
                    <div class="code-workspace" style="flex: 1; display: flex; flex-direction: column; gap: 15px;">
                        <div class="repo-input">
                            <input type="text" placeholder="Paste GitHub URL or Tool link...">
                            <button class="action-btn"><i class="fas fa-code-branch"></i> Analyze</button>
                        </div>
                        <div class="chat-stream" style="flex: 1; background: var(--bg-dark); border-radius: 8px; border: 1px solid var(--border);">
                            <pre style="padding: 15px; color: var(--text-muted); font-family: monospace;">// File editor and analysis workspace loaded.
// Waiting for OpenHands / Qwen instruction...</pre>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Panel: Files & Media -->
            <section id="media-panel" class="workspace-panel">
                <div class="panel-header"><h2>Files, Media & Conversion</h2></div>
                <div class="drop-zone" id="file-drop-zone">
                    <i class="fas fa-cloud-upload-alt fa-3x"></i>
                    <p>Drag & Drop files here, or click to upload</p>
                </div>
                <div class="conversion-tools">
                    <button class="action-btn"><i class="fas fa-file-pdf"></i> PDF Tools</button>
                    <button class="action-btn"><i class="fas fa-image"></i> Image Editor</button>
                    <button class="action-btn"><i class="fas fa-video"></i> Video Compress</button>
                    <button class="action-btn"><i class="fas fa-music"></i> Audio Extract</button>
                </div>
            </section>

            <!-- Panel: System -->
            <section id="system-panel" class="workspace-panel">
                <div class="panel-header"><h2>System & Environment Control</h2></div>
                <div class="system-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-key"></i> API Configuration</h3>
                        <input type="password" placeholder="OpenAI API Key" style="width: 100%; padding: 10px; margin-bottom: 10px; background: var(--bg-dark); border: 1px solid var(--border); color: white; border-radius: 4px;">
                        <button class="action-btn" style="width: 100%;">Save Configuration</button>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-satellite-dish"></i> Agent Status</h3>
                        <ul style="list-style: none; padding: 0; color: var(--text-muted); font-size: 14px; line-height: 2;">
                            <li><i class="fas fa-circle" style="color: #0f0; font-size: 10px;"></i> Event Bus: Active</li>
                            <li><i class="fas fa-circle" style="color: #0f0; font-size: 10px;"></i> UI Routing: Active</li>
                            <li><i class="fas fa-circle" style="color: #555; font-size: 10px;"></i> OpenHands: Offline</li>
                        </ul>
                    </div>
                </div>
            </section>
        </main>

        <!-- Right Sidebar: Tool Registry -->
        <aside class="tool-sidebar">
            <div class="tool-header">
                <h3>Active Tools</h3>
                <span class="status-indicator live"></span>
            </div>
            <div class="tool-list">
                <div class="tool-item"><span class="tool-name">Web Search (Crawl4AI)</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">Local LLM (Qwen)</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">Coding Agent</span><label class="toggle-switch"><input type="checkbox"><span class="slider"></span></label></div>
            </div>
        </aside>
    </div>
    <script src="/static/app.js"></script>
</body>
</html>
"""
write_file("ui/frontend/index.html", index_html_content)

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "feat(ui): add Project Memory, File Explorer, and Agent Status to align with Master Prompt"])
subprocess.run(["git", "push"])
print("[+] Master alignment components injected. Pushed to GitHub.")
