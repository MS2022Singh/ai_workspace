
// Central Event Bus Logic
function firePrompt(promptName) {
    const termIn = document.getElementById('term-in');
    termIn.value = `/ai Execute macro: ${promptName}`;
    termIn.focus();
}

function insertPrompt(text) {
    const termIn = document.getElementById('term-in');
    termIn.value = text;
    termIn.focus();
}

async function ingestRepo() {
    const url = document.getElementById('repo-url').value;
    if(!url) return;
    
    document.getElementById('term-out').innerHTML += `<div><span style="color:var(--warning)">[EVENT]</span> Ingestion started for: ${url}</div>`;
    document.getElementById('term-out').innerHTML += `<div><span style="color:var(--accent)">[SYS]</span> Validating repo, generating Python wrapper, and mapping to Event Bus...</div>`;
    
    // Simulate backend ingestion call
    setTimeout(() => {
        document.getElementById('term-out').innerHTML += `<div><span style="color:var(--success)">[SUCCESS]</span> Repo incorporated securely into Workspace OS.</div>`;
        document.getElementById('term-out').scrollTop = document.getElementById('term-out').scrollHeight;
        document.getElementById('repo-url').value = '';
    }, 2000);
}

async function toggleTool(tool, isEnabled) {
    const status = isEnabled ? "GRANTED" : "REVOKED";
    const color = isEnabled ? "var(--success)" : "var(--danger)";
    document.getElementById('term-out').innerHTML += `<div><span style="color:${color}">[PERMISSION ENGINE]</span> Access ${status} for ${tool}.</div>`;
    document.getElementById('term-out').scrollTop = document.getElementById('term-out').scrollHeight;
    
    await fetch('/api/toggle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool: tool, enabled: isEnabled })
    });
}
