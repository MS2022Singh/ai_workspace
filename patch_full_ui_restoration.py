import os
import subprocess

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("[+] Restoring full Master Prompt UI layout and components...")

full_html_content = """<!DOCTYPE html>
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
        <!-- Left Sidebar: Navigation & Modules -->
        <aside class="nav-sidebar">
            <div class="logo">
                <i class="fas fa-brain"></i>
                <span>OS Core</span>
            </div>
            <nav class="nav-menu">
                <button class="nav-btn active" data-target="chat-panel"><i class="fas fa-comment-dots"></i> Chat & Tasks</button>
                <button class="nav-btn" data-target="memory-panel"><i class="fas fa-database"></i> Project Memory</button>
                <button class="nav-btn" data-target="research-panel"><i class="fas fa-search"></i> Research & Crawl</button>
                <button class="nav-btn" data-target="code-panel"><i class="fas fa-code"></i> Code & Build</button>
                <button class="nav-btn" data-target="media-panel"><i class="fas fa-photo-video"></i> Files & Media</button>
                <button class="nav-btn" data-target="security-panel"><i class="fas fa-shield-alt"></i> Security & OSINT</button>
                <button class="nav-btn" data-target="system-panel"><i class="fas fa-terminal"></i> System & Diagnostics</button>
            </nav>
            <div class="nav-bottom">
                <button class="icon-btn" id="btn-screenshot" title="Take Screenshot (Ctrl+Shift+S)"><i class="fas fa-camera"></i></button>
                <button class="icon-btn" id="btn-help" title="Help & Documentation"><i class="fas fa-info-circle"></i></button>
            </div>
        </aside>

        <!-- Main Content Area -->
        <main class="main-workspace">
            
            <!-- Panel: Chat & Tasks -->
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
                        <button class="attach-btn" title="Upload/Drag-Drop"><i class="fas fa-paperclip"></i></button>
                        <textarea id="main-input" placeholder="Enter task, command, or prompt... (Press Enter to submit)" rows="1"></textarea>
                        <button class="send-btn" id="send-btn"><i class="fas fa-paper-plane"></i></button>
                    </div>
                </div>
            </section>

            <!-- Panel: Project Memory -->
            <section id="memory-panel" class="workspace-panel">
                <div class="panel-header"><h2>Project Memory & Knowledge Base</h2></div>
                <div class="memory-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: calc(100% - 60px); overflow-y: auto;">
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-list-check"></i> Requirements & Scope</h3>
                        <textarea style="width: 100%; height: 140px; background: var(--bg-dark); color: var(--text-main); border: 1px solid var(--border); border-radius: 4px; padding: 10px; margin-top: 10px;" placeholder="Core requirements..."></textarea>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-spinner"></i> Progress & Milestones</h3>
                        <textarea style="width: 100%; height: 140px; background: var(--bg-dark); color: var(--text-main); border: 1px solid var(--border); border-radius: 4px; padding: 10px; margin-top: 10px;" placeholder="Completed milestones..."></textarea>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px; grid-column: span 2;">
                        <h3><i class="fas fa-bug"></i> Active Issues & Decisions</h3>
                        <textarea style="width: 100%; height: 100px; background: var(--bg-dark); color: var(--text-main); border: 1px solid var(--border); border-radius: 4px; padding: 10px; margin-top: 10px;" placeholder="Log issues, errors, and fixes..."></textarea>
                        <button class="action-btn mt-10"><i class="fas fa-save"></i> Commit to Governance Memory</button>
                    </div>
                </div>
            </section>

            <!-- Panel: Research -->
            <section id="research-panel" class="workspace-panel">
                <div class="panel-header"><h2>Deep Research & Crawling (Crawl4AI)</h2></div>
                <div class="repo-input">
                    <input type="text" placeholder="Enter research topic or URL to crawl...">
                    <button class="action-btn"><i class="fas fa-spider"></i> Dispatch Crawler</button>
                </div>
                <div class="chat-stream mt-20" style="border: 1px dashed var(--border); border-radius: 8px; flex: 1;">
                    <div class="message system-msg">
                        <div class="msg-avatar"><i class="fas fa-info-circle"></i></div>
                        <div class="msg-content"><p>Research ingestion engine active. Sources verified with provenance tagging.</p></div>
                    </div>
                </div>
            </section>

            <!-- Panel: Code & Build -->
            <section id="code-panel" class="workspace-panel">
                <div class="panel-header"><h2>Code Workspace & Tool Auto-Incorporation</h2></div>
                <div class="code-layout" style="display: flex; gap: 20px; height: calc(100% - 60px);">
                    <div class="file-tree" style="width: 250px; background: var(--bg-input); border-radius: 8px; padding: 15px; border: 1px solid var(--border);">
                        <h4 style="margin-bottom: 10px; color: var(--text-muted);"><i class="fas fa-folder-open"></i> Workspace</h4>
                        <ul style="list-style: none; padding-left: 10px; color: var(--text-main); font-family: monospace; font-size: 13px; line-height: 1.8;">
                            <li><i class="fas fa-folder"></i> core/</li>
                            <li><i class="fas fa-folder"></i> ui/</li>
                            <li><i class="fab fa-python"></i> main.py</li>
                            <li><i class="fas fa-file-alt"></i> governance/project_memory.json</li>
                        </ul>
                    </div>
                    <div class="code-workspace" style="flex: 1; display: flex; flex-direction: column; gap: 15px;">
                        <div class="repo-input">
                            <input type="text" placeholder="Paste GitHub URL or Tool link for Auto-Incorporation...">
                            <button class="action-btn"><i class="fas fa-code-branch"></i> Analyze & Merge</button>
                        </div>
                        <div class="chat-stream" style="flex: 1; background: var(--bg-dark); border-radius: 8px; border: 1px solid var(--border);">
                            <pre style="padding: 15px; color: var(--text-muted); font-family: monospace;">// Isolated Sandbox & Git Worktree Active
// Awaiting agent instruction...</pre>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Panel: Files & Media -->
            <section id="media-panel" class="workspace-panel">
                <div class="panel-header"><h2>Files, Media Conversion & Editors</h2></div>
                <div class="drop-zone" id="file-drop-zone">
                    <i class="fas fa-cloud-upload-alt fa-3x"></i>
                    <p>Drag & Drop files, media, or archives here, or click to upload</p>
                    <span class="sub-text">Supports lossless compression, format conversion, and visual editing</span>
                </div>
                <div class="conversion-tools">
                    <button class="action-btn"><i class="fas fa-file-pdf"></i> Stirling PDF Tools</button>
                    <button class="action-btn"><i class="fas fa-image"></i> Fooocus Image Editor</button>
                    <button class="action-btn"><i class="fas fa-video"></i> Video Compressor</button>
                    <button class="action-btn"><i class="fas fa-music"></i> Audio Extractor</button>
                </div>
            </section>

            <!-- Panel: Security & OSINT -->
            <section id="security-panel" class="workspace-panel">
                <div class="panel-header"><h2>Security, Threat Intel & OSINT Scanner</h2></div>
                <div class="system-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-shield-virus"></i> Vulnerability Scanner</h3>
                        <p style="color: var(--text-muted); margin: 10px 0; font-size: 0.9rem;">Run PyRIT red-teaming checks and dependency dependency audits.</p>
                        <button class="action-btn" style="width: 100%;">Run Security Audit</button>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-binoculars"></i> OSINT Reconnaissance</h3>
                        <input type="text" placeholder="Target Domain / IP / Handle" style="width: 100%; padding: 10px; margin: 10px 0; background: var(--bg-dark); border: 1px solid var(--border); color: white; border-radius: 4px;">
                        <button class="action-btn" style="width: 100%;">Execute Recon</button>
                    </div>
                </div>
            </section>

            <!-- Panel: System -->
            <section id="system-panel" class="workspace-panel">
                <div class="panel-header"><h2>System Diagnostics & Environment</h2></div>
                <div class="system-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-key"></i> API Configuration</h3>
                        <input type="password" placeholder="OpenAI / Qwen API Key" style="width: 100%; padding: 10px; margin-bottom: 10px; background: var(--bg-dark); border: 1px solid var(--border); color: white; border-radius: 4px;">
                        <button class="action-btn" style="width: 100%;">Save Credentials</button>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-satellite-dish"></i> Agent Status</h3>
                        <ul style="list-style: none; padding: 0; color: var(--text-muted); font-size: 14px; line-height: 2;">
                            <li><i class="fas fa-circle" style="color: #10b981; font-size: 10px;"></i> Event Bus: Active</li>
                            <li><i class="fas fa-circle" style="color: #10b981; font-size: 10px;"></i> Permission Engine: Zero-Trust</li>
                            <li><i class="fas fa-circle" style="color: #10b981; font-size: 10px;"></i> Sandbox Runner: Isolated</li>
                        </ul>
                    </div>
                </div>
            </section>
        </main>

        <!-- Right Sidebar: Tool Registry & Toggles -->
        <aside class="tool-sidebar">
            <div class="tool-header">
                <h3>Active Tool Registry</h3>
                <span class="status-indicator live"></span>
            </div>
            <div class="tool-list">
                <div class="tool-item"><span class="tool-name">Web Search (Crawl4AI)</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">Local LLM (Qwen)</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">Coding Agent (OpenHands)</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">System Control (PowerShell)</span><label class="toggle-switch"><input type="checkbox"><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">Image Gen (Fooocus)</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">Workflow Auto (n8n)</span><label class="toggle-switch"><input type="checkbox"><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">Voice STT/TTS (Whisper)</span><label class="toggle-switch"><input type="checkbox"><span class="slider"></span></label></div>
            </div>
        </aside>
    </div>
    <script src="/static/app.js"></script>
</body>
</html>
"""
write_file("ui/frontend/index.html", full_html_content)

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "fix(ui): fully restore all Master Prompt modules, panels, tool toggles, and workspace components"])
subprocess.run(["git", "push"])
print("[+] Full UI successfully restored and pushed to GitHub.")
