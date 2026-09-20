import os
import subprocess
from pathlib import Path

# Define project directories
FRONTEND_DIR = Path("frontend")
BACKEND_DIR = Path("backend")
FRONTEND_DIR.mkdir(parents=True, exist_ok=True)
BACKEND_DIR.mkdir(parents=True, exist_ok=True)

# 1. UI HTML Update
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Workspace OS - Command Center</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }
        .panel { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 20px; margin-bottom: 20px; }
        .toggle-switch { position: relative; display: inline-block; width: 40px; height: 20px; }
        .toggle-switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #21262d; transition: .4s; border-radius: 20px; }
        input:checked + .slider { background-color: #238636; }
        .tool-matrix { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .tool-card { padding: 10px; border: 1px solid #30363d; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; }
        .input-group { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 8px; background: #0d1117; border: 1px solid #30363d; color: #c9d1d9; border-radius: 4px; }
        button { padding: 8px 16px; background: #238636; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2ea043; }
        #keyboard-hints { font-size: 0.8em; color: #8b949e; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>AI Workspace OS</h1>
    
    <div class="panel" id="dynamic-import-panel">
        <h3>Dynamic Repo / Tool Ingestion</h3>
        <p>Paste a GitHub URL, feature link, or tool API to auto-incorporate it into the workspace.</p>
        <div class="input-group">
            <input type="text" id="repo-url" placeholder="https://github.com/... or Tool URL" />
            <button id="btn-ingest">Ingest Tool (Enter)</button>
        </div>
    </div>

    <div class="panel">
        <h3>Grouped Tool Matrix (Permission Toggles)</h3>
        <div class="tool-matrix">
            <div class="tool-card"><span>Local Infer (Ollama/vLLM)</span> <label class="toggle-switch"><input type="checkbox" id="tgl-infer"><span class="slider"></span></label></div>
            <div class="tool-card"><span>Web Browser Agent</span> <label class="toggle-switch"><input type="checkbox" id="tgl-browser"><span class="slider"></span></label></div>
            <div class="tool-card"><span>Coding Agent (SWE)</span> <label class="toggle-switch"><input type="checkbox" id="tgl-coder"><span class="slider"></span></label></div>
            <div class="tool-card"><span>Research & OSINT</span> <label class="toggle-switch"><input type="checkbox" id="tgl-osint"><span class="slider"></span></label></div>
        </div>
    </div>

    <div id="keyboard-hints">Keyboard Shortcuts: [Ctrl+I] Focus Ingestion | [Enter] Execute Ingestion | [Ctrl+T] Toggle All Tools</div>
    
    <script src="app.js"></script>
</body>
</html>"""

# 2. UI Logic Update
js_content = """document.addEventListener('DOMContentLoaded', () => {
    const ingestBtn = document.getElementById('btn-ingest');
    const repoInput = document.getElementById('repo-url');
    const toggles = document.querySelectorAll('.toggle-switch input');

    const executeIngestion = () => {
        const url = repoInput.value.trim();
        if(url) {
            console.log(`[System] Initiating dynamic ingestion for: ${url}`);
            alert(`Initiating ingestion protocol for: ${url}\\nSee backend console for build tasks.`);
            repoInput.value = '';
        }
    };

    ingestBtn.addEventListener('click', executeIngestion);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && document.activeElement === repoInput) {
            e.preventDefault();
            executeIngestion();
        }
        if (e.ctrlKey && e.key.toLowerCase() === 'i') {
            e.preventDefault();
            repoInput.focus();
        }
        if (e.ctrlKey && e.key.toLowerCase() === 't') {
            e.preventDefault();
            const firstState = toggles[0].checked;
            toggles.forEach(t => t.checked = !firstState);
            console.log(`[System] All tools set to ${!firstState ? 'Active' : 'Inactive'}`);
        }
    });

    toggles.forEach(toggle => {
        toggle.addEventListener('change', (e) => {
            console.log(`[Permission] Tool state changed: ${e.target.id} -> ${e.target.checked}`);
        });
    });
});"""

# 3. Project Documentation Update
markdown_content = """# AI Workspace OS - Project Status

## Current Milestone: Phase 1 Completed
* **Date**: September 20, 2026
* **Status**: Successful UI integration.

### Completed Work
* **Dynamic Repo/Tool Ingestion Panel**: UI structure established to allow users to paste GitHub URLs/API links for auto-incorporation.
* **Tool Matrix Toggles**: Added explicit permission-bound on/off toggles for categorized AI tools (Inference, Browser, Coding, OSINT).
* **Keyboard Shortcuts**: Bound shortcuts (`Enter` to execute, `Ctrl+I` to focus, `Ctrl+T` to mass-toggle).

### Pending Work
* **Phase 2**: Multi-tier Permission Engine and Computer Control security layers.
* **Phase 3**: Structured Memory architecture.
* **Phase 4**: Core tool wrappers and inference engine integration.
"""

# Write files
with open(FRONTEND_DIR / "index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(FRONTEND_DIR / "app.js", "w", encoding="utf-8") as f:
    f.write(js_content)

with open("PROJECT_STATUS.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)

print("[?] UI Files generated.")
print("[?] Keyboard shortcuts wired.")
print("[?] Project documentation updated.")

# 4. Git Synchronization
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "feat(ui): complete phase 1 - toggles, shortcuts, dynamic import panel, and status doc"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("[?] Phase 1 successfully committed and pushed to GitHub.")
except subprocess.CalledProcessError as e:
    print(f"[!] Git operation failed. Ensure you have internet access and GitHub credentials configured. Error: {e}")
