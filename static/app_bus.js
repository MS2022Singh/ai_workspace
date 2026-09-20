function switchTab(tabId) {
    const tabs = document.querySelectorAll('.workspace-tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => {
        btn.classList.remove('active');
    });

    const selectedTab = document.getElementById(tabId);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    event.currentTarget.classList.add('active');
}

async function sendChat() {
    const input = document.getElementById('chat-input');
    const history = document.getElementById('chat-history');
    const text = input.value.trim();
    if (!text) return;

    const userDiv = document.createElement('div');
    userDiv.className = 'msg user';
    userDiv.textContent = 'User: ' + text;
    history.appendChild(userDiv);
    input.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ prompt: text, agent: document.getElementById('agent-selector').value })
        });
        const data = await response.json();

        const aiDiv = document.createElement('div');
        aiDiv.className = 'msg ai';
        aiDiv.textContent = data.response || 'Action executed successfully.';
        history.appendChild(aiDiv);
        history.scrollTop = history.scrollHeight;
    } catch (e) {
        console.error(e);
    }
}

async function triggerCognitive(key) {
    const history = document.getElementById('chat-history');
    try {
        const response = await fetch('/api/cognitive', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ framework: key, topic: 'AI Workspace OS Optimization' })
        });
        const data = await response.json();

        const aiDiv = document.createElement('div');
        aiDiv.className = 'msg ai';
        aiDiv.textContent = data.prompt;
        history.appendChild(aiDiv);
        history.scrollTop = history.scrollHeight;
    } catch (e) {
        console.error(e);
    }
}

async function execCmd() {
    const input = document.getElementById('terminal-input');
    const out = document.getElementById('terminal-out');
    const cmd = input.value.trim();
    if (!cmd) return;

    out.textContent += '\n> ' + cmd + '\nRunning command...\n';
    input.value = '';

    try {
        const response = await fetch('/api/terminal', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ command: cmd })
        });
        const data = await response.json();
        out.textContent += data.output + '\n';
        out.scrollTop = out.scrollHeight;
    } catch (e) {
        out.textContent += 'Error executing command.\n';
    }
}

async function runConvert() {
    const file = document.getElementById('convert-file-input').value || 'document.pdf';
    const type = document.getElementById('convert-type').value;
    const target = document.getElementById('convert-target').value || 'docx';
    const resultBox = document.getElementById('convert-result');

    resultBox.textContent = 'Processing conversion...';
    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ filename: file, source_type: type, target_format: target })
        });
        const data = await response.json();
        resultBox.textContent = data.message + ' -> Available at: ' + data.download_url;
    } catch (e) {
        resultBox.textContent = 'Conversion failed.';
    }
}

async function runCompress() {
    const file = document.getElementById('compress-file-input').value || 'media.mp4';
    const quality = document.getElementById('compress-quality').value;
    const targetMB = document.getElementById('compress-target-size').value;
    const resultBox = document.getElementById('compress-result');

    resultBox.textContent = 'Compressing media file...';
    try {
        const response = await fetch('/api/compress', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ filename: file, level: parseInt(quality), target_size: parseFloat(targetMB) })
        });
        const data = await response.json();
        resultBox.textContent = data.message;
    } catch (e) {
        resultBox.textContent = 'Compression failed.';
    }
}

async function loadTools() {
    const container = document.getElementById('tools-matrix-container');
    if (!container) return;
    try {
        const response = await fetch('/api/tools');
        const data = await response.json();
        let html = '';
        for (const [cat, tools] of Object.entries(data.categories)) {
            html += `<div class="tool-category-card"><h4>${cat}</h4>`;
            tools.forEach(t => {
                html += `<div class="tool-item"><span>${t}</span><span style="color:#3fb950;">Active</span></div>`;
            });
            html += `</div>`;
        }
        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = 'Failed to load tools matrix.';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadTools();
});
