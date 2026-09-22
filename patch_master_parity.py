import os
import subprocess

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("[+] Upgrading Command Center to 100% Master Prompt Parity...")

master_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Workspace OS | Master Command Center</title>
    <link rel="stylesheet" href="/static/styles.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="os-container">
        <!-- Left Sidebar: Navigation & Modules -->
        <aside class="nav-sidebar">
            <div class="logo">
                <i class="fas fa-brain"></i>
                <span>OS Core v3.1</span>
            </div>
            <nav class="nav-menu">
                <button class="nav-btn active" data-target="chat-panel"><i class="fas fa-comment-dots"></i> Chat & Prompts</button>
                <button class="nav-btn" data-target="agents-panel"><i class="fas fa-users-cog"></i> Specialist Agents</button>
                <button class="nav-btn" data-target="memory-panel"><i class="fas fa-database"></i> Project Memory</button>
                <button class="nav-btn" data-target="research-panel"><i class="fas fa-search"></i> Research & Crawl</button>
                <button class="nav-btn" data-target="code-panel"><i class="fas fa-code"></i> Code & Build</button>
                <button class="nav-btn" data-target="media-panel"><i class="fas fa-photo-video"></i> Files & Media</button>
                <button class="nav-btn" data-target="security-panel"><i class="fas fa-shield-alt"></i> Security & OSINT</button>
                <button class="nav-btn" data-target="system-panel"><i class="fas fa-terminal"></i> System & Voice</button>
            </nav>
            <div class="nav-bottom">
                <button class="icon-btn" id="btn-screenshot" title="Take Screenshot"><i class="fas fa-camera"></i></button>
                <button class="icon-btn" id="btn-help" title="Help Information"><i class="fas fa-info-circle"></i></button>
            </div>
        </aside>

        <!-- Main Content Area -->
        <main class="main-workspace">
            
            <!-- Panel: Chat & Built-in Prompt Frameworks -->
            <section id="chat-panel" class="workspace-panel active">
                <div class="prompt-framework-bar" style="display: flex; gap: 8px; padding: 10px 15px; background: var(--bg-input); border-bottom: 1px solid var(--border); overflow-x: auto;">
                    <button class="framework-btn" onclick="applyPrompt('genius')"><i class="fas fa-lightbulb"></i> Genius Breakdown</button>
                    <button class="framework-btn" onclick="applyPrompt('skill')"><i class="fas fa-graduation-cap"></i> Master Skill</button>
                    <button class="framework-btn" onclick="applyPrompt('blocks')"><i class="fas fa-brain"></i> Fix Mental Blocks</button>
                    <button class="framework-btn" onclick="applyPrompt('clarity')"><i class="fas fa-bolt"></i> Clarity & Metaphor</button>
                    <button class="framework-btn" onclick="applyPrompt('phd')"><i class="fas fa-atom"></i> PhD-Level</button>
                    <button class="framework-btn" onclick="applyPrompt('frameworks')"><i class="fas fa-project-diagram"></i> Mental Models</button>
                    <button class="framework-btn" onclick="applyPrompt('upgrade')"><i class="fas fa-rocket"></i> 30-Day Brain Upgrade</button>
                </div>
                <div class="chat-stream" id="chat-stream">
                    <div class="message system-msg">
                        <div class="msg-avatar"><i class="fas fa-robot"></i></div>
                        <div class="msg-content">
                            <p><strong>System Online.</strong> Unified App/OS loaded with 7 Master Prompt response rules, Event Bus, and zero-trust permission engine active.</p>
                        </div>
                    </div>
                </div>
                <div class="input-area">
                    <div class="input-wrapper">
                        <button class="attach-btn" title="Upload File / Drag-Drop"><i class="fas fa-paperclip"></i></button>
                        <textarea id="main-input" placeholder="Enter task, prompt, or command (Press Enter)..." rows="1"></textarea>
                        <button class="send-btn" id="send-btn"><i class="fas fa-paper-plane"></i></button>
                    </div>
                </div>
            </section>

            <!-- Panel: Specialist Agents & Device Registry -->
            <section id="agents-panel" class="workspace-panel">
                <div class="panel-header"><h2>Specialist Agents & Device Registry</h2></div>
                <div class="agents-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; overflow-y: auto; padding-bottom: 20px;">
                    <div class="sys-card" style="background: var(--bg-input); padding: 15px; border-radius: 8px;">
                        <h4><i class="fas fa-microscope"></i> Research Agent</h4>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin: 8px 0;">Cross-checks sources & verifies facts.</p>
                        <span class="badge active">Active</span>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 15px; border-radius: 8px;">
                        <h4><i class="fas fa-laptop-code"></i> Coding Agent</h4>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin: 8px 0;">Manages Git trees & unit testing.</p>
                        <span class="badge active">Active</span>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 15px; border-radius: 8px;">
                        <h4><i class="fas fa-desktop"></i> Computer Agent</h4>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin: 8px 0;">Inspects filesystem & process state.</p>
                        <span class="badge active">Active</span>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 15px; border-radius: 8px;">
                        <h4><i class="fas fa-file-alt"></i> File/Document Agent</h4>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin: 8px 0;">Handles conversion & compression.</p>
                        <span class="badge active">Active</span>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 15px; border-radius: 8px;">
                        <h4><i class="fas fa-headphones"></i> Audio Agent</h4>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin: 8px 0;">Whisper STT & Kokoro TTS pipelines.</p>
                        <span class="badge inactive">Standby</span>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 15px; border-radius: 8px;">
                        <h4><i class="fas fa-briefcase"></i> Business & Web Agent</h4>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin: 8px 0;">Workflow automation & browser use.</p>
                        <span class="badge active">Active</span>
                    </div>
                </div>
            </section>

            <!-- Panel: Project Memory -->
            <section id="memory-panel" class="workspace-panel">
                <div class="panel-header"><h2>Project Memory & Knowledge Persistence</h2></div>
                <div class="memory-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: calc(100% - 60px); overflow-y: auto;">
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-list-check"></i> Requirements & Scope</h3>
                        <textarea style="width: 100%; height: 140px; background: var(--bg-dark); color: var(--text-main); border: 1px solid var(--border); border-radius: 4px; padding: 10px; margin-top: 10px;">Unified App/OS Command Center with 11,000+ asset inventory integration.</textarea>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-spinner"></i> Progress & Milestones</h3>
                        <textarea style="width: 100%; height: 140px; background: var(--bg-dark); color: var(--text-main); border: 1px solid var(--border); border-radius: 4px; padding: 10px; margin-top: 10px;">Milestone 7 finalized: Multi-panel UI, Event Bus, and Master Prompt rules active.</textarea>
                    </div>
                </div>
            </section>

            <!-- Panel: Research & Crawling -->
            <section id="research-panel" class="workspace-panel">
                <div class="panel-header"><h2>Deep Research & Crawling (Crawl4AI & Semantica)</h2></div>
                <div class="repo-input">
                    <input type="text" placeholder="Enter topic or URL to crawl with provenance verification...">
                    <button class="action-btn"><i class="fas fa-spider"></i> Dispatch Crawler</button>
                </div>
                <div class="chat-stream mt-20" style="border: 1px dashed var(--border); border-radius: 8px; flex: 1;">
                    <div class="message system-msg">
                        <div class="msg-avatar"><i class="fas fa-info-circle"></i></div>
                        <div class="msg-content"><p>Research engine ready. No unsupported claims policy enforced.</p></div>
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
                            <li><i class="fas fa-folder"></i> catalog/</li>
                            <li><i class="fas fa-folder"></i> ui/frontend/</li>
                            <li><i class="fab fa-python"></i> main.py</li>
                        </ul>
                    </div>
                    <div class="code-workspace" style="flex: 1; display: flex; flex-direction: column; gap: 15px;">
                        <div class="repo-input">
                            <input type="text" placeholder="Paste GitHub URL or Tool link for Auto-Incorporation...">
                            <button class="action-btn"><i class="fas fa-code-branch"></i> Analyze & Merge</button>
                        </div>
                        <div class="chat-stream" style="flex: 1; background: var(--bg-dark); border-radius: 8px; border: 1px solid var(--border);">
                            <pre style="padding: 15px; color: var(--text-muted); font-family: monospace;">// Isolated Sandbox & Git Worktree Active</pre>
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
                    <span class="sub-text">Stirling PDF, Fooocus Image Editor, Video Compress active</span>
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
                        <h3><i class="fas fa-shield-virus"></i> PyRIT Red-Teaming</h3>
                        <button class="action-btn mt-10" style="width: 100%;">Run Security Audit</button>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-binoculars"></i> OSINT Reconnaissance</h3>
                        <input type="text" placeholder="Target Domain / Handle" style="width: 100%; padding: 10px; margin: 10px 0; background: var(--bg-dark); border: 1px solid var(--border); color: white; border-radius: 4px;">
                        <button class="action-btn" style="width: 100%;">Execute Recon</button>
                    </div>
                </div>
            </section>

            <!-- Panel: System & Voice -->
            <section id="system-panel" class="workspace-panel">
                <div class="panel-header"><h2>System Diagnostics, Voice & Autonomy Policy</h2></div>
                <div class="system-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-robot"></i> Autonomy Policy Level</h3>
                        <select style="width: 100%; padding: 10px; margin-top: 10px; background: var(--bg-dark); border: 1px solid var(--border); color: white; border-radius: 4px;">
                            <option>Level 1: Observe Only</option>
                            <option>Level 2: Suggest Actions</option>
                            <option>Level 3: Execute with Approval</option>
                            <option>Level 4: Fully Autonomous</option>
                        </select>
                    </div>
                    <div class="sys-card" style="background: var(--bg-input); padding: 20px; border-radius: 8px;">
                        <h3><i class="fas fa-microphone-alt"></i> Voice Conversational Mode</h3>
                        <button class="action-btn mt-10" style="width: 100%; background: var(--success);"><i class="fas fa-microphone"></i> Start Realtime Voice Stream</button>
                    </div>
                </div>
            </section>
        </main>

        <!-- Right Sidebar: Comprehensive Tool Registry -->
        <aside class="tool-sidebar">
            <div class="tool-header">
                <h3>Master Tool Registry</h3>
                <span class="status-indicator live"></span>
            </div>
            <div class="tool-list">
                <div class="tool-category-title" style="font-size: 0.75rem; color: var(--accent); margin-top: 5px; text-transform: uppercase; font-weight: bold;">Orchestration & UI</div>
                <div class="tool-item"><span class="tool-name">ToolJet & n8n</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">AppFlowy Workspace</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                
                <div class="tool-category-title" style="font-size: 0.75rem; color: var(--accent); margin-top: 10px; text-transform: uppercase; font-weight: bold;">Multi-Agent & DAG</div>
                <div class="tool-item"><span class="tool-name">OpenHands Sandbox</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">Browser Use Engine</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                
                <div class="tool-category-title" style="font-size: 0.75rem; color: var(--accent); margin-top: 10px; text-transform: uppercase; font-weight: bold;">Models & RAG</div>
                <div class="tool-item"><span class="tool-name">Qwen 3.8 & Ollama</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>
                <div class="tool-item"><span class="tool-name">Crawl4AI & Semantica</span><label class="toggle-switch"><input type="checkbox" checked><span class="slider"></span></label></div>

                <div class="tool-category-title" style="font-size: 0.75rem; color: var(--accent); margin-top: 10px; text-transform: uppercase; font-weight: bold;">Security & OSINT</div>
                <div class="tool-item"><span class="tool-name">PyRIT & Vulture</span><label class="toggle-switch"><input type="checkbox"><span class="slider"></span></label></div>
            </div>
        </aside>
    </div>
    <script>
        function applyPrompt(type) {
            const input = document.getElementById('main-input');
            if(type === 'genius') input.value = "I want to understand [topic] as if I were a genius. Break down concept using advanced analogies...";
            if(type === 'skill') input.value = "Assume you're a master of [skill] with 20+ years of experience. Reverse engineer the process...";
            if(type === 'blocks') input.value = "I have been struggling with [personal issue]. Analyze it like a cognitive scientist...";
            if(type === 'clarity') input.value = "I don't understand [complex concept]. Break it down step-by-step using metaphors...";
            if(type === 'phd') input.value = "Teach me [topic] like I'm preparing for a PhD. Start from first principles...";
            if(type === 'frameworks') input.value = "I'm trying to master [skill/topic]. Build me a custom mental model or decision framework...";
            if(type === 'upgrade') input.value = "Design a 30 day brain upgrade program that includes high IQ thinking routines...";
            input.focus();
        }
    </script>
    <script src="/static/app.js"></script>
</body>
</html>
"""

write_file("ui/frontend/index.html", master_html_content)

# Update CSS for new badge elements
css_patch = """
.badge { background: var(--bg-dark); padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; }
.badge.active { color: var(--success); border: 1px solid var(--success); }
.badge.inactive { color: var(--text-muted); border: 1px solid var(--border); }
.framework-btn { background: var(--bg-dark); border: 1px solid var(--border); color: var(--text-main); padding: 6px 12px; border-radius: 6px; cursor: pointer; white-space: nowrap; font-size: 0.85rem; transition: 0.2s; }
.framework-btn:hover { background: var(--accent); border-color: var(--accent); }
"""
with open("ui/frontend/styles.css", "a", encoding="utf-8") as f:
    f.write(css_patch)

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "fix(ui): inject Master Prompt 7-rule prompt bar, Specialist Agents, Autonomy levels, and categorized tool registry"])
subprocess.run(["git", "push"])
print("[+] Master parity UI fully injected and pushed to GitHub.")
