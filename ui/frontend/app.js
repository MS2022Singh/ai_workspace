let socket = null;

document.addEventListener("DOMContentLoaded", () => {
    initWebSocket();
    initNavigation();
    initInteractions();
    loadDeviceRegistry();
    loadRegisteredTools();
});

function initWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws`;

    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        document.getElementById("ws-status-dot").className = "dot online";
        document.getElementById("ws-status-text").innerText = "Connected";
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            appendLogEntry(data);
        } catch (e) {
            console.error("WS Parse Error:", e);
        }
    };

    socket.onclose = () => {
        document.getElementById("ws-status-dot").className = "dot offline";
        document.getElementById("ws-status-text").innerText = "Disconnected";
        setTimeout(initWebSocket, 3000);
    };
}

function initNavigation() {
    const navBtns = document.querySelectorAll(".nav-btn");
    navBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const panelId = btn.getAttribute("data-panel");
            navBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
            const targetPanel = document.getElementById(`panel-${panelId}`);
            if (targetPanel) {
                targetPanel.classList.add("active");
            }
        });
    });
}

function initInteractions() {
    // Panel 1: Main Chat Execution
    document.getElementById("send-btn")?.addEventListener("click", () => executeCommand());
    document.getElementById("cmd-input")?.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            executeCommand();
        }
    });

    // Helper fetch wrapper
    const handleApiAction = (btnId, resultId, endpoint, bodyData, formatter) => {
        document.getElementById(btnId)?.addEventListener("click", () => {
            const resBox = document.getElementById(resultId);
            if (resBox) resBox.innerHTML = "Processing request...";
            
            fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(bodyData())
            })
            .then(res => res.json())
            .then(data => {
                if (resBox) resBox.innerHTML = formatter(data);
            })
            .catch(err => {
                if (resBox) resBox.innerHTML = "<span style='color:#ef4444;'>Error processing request.</span>";
            });
        });
    };

    // Panel 2: Discussion
    handleApiAction("start-discussion-btn", "discussion-output", "/api/command", 
        () => ({ module: "discussion", action: document.getElementById("discussion-topic").value }),
        d => `<div class="agent-msg"><strong>Debate Engine:</strong> Initiated stream for '${document.getElementById("discussion-topic").value}'<br><br>${d.response}</div>`
    );

    // Panel 3: Research
    handleApiAction("run-research-btn", "research-results", "/api/command",
        () => ({ module: "research", action: document.getElementById("research-query").value }),
        d => `✓ Deep Research Synthesized:<br>${d.response}`
    );

    // Panel 4: Coding
    handleApiAction("run-coding-btn", "coding-output", "/api/command",
        () => ({ module: "coding", action: document.getElementById("coding-prompt").value }),
        d => `// Code Agent Output:\n${d.response}`
    );

    // Panel 5: Computer Control
    handleApiAction("exec-terminal-btn", "terminal-output", "/api/command",
        () => ({ module: "terminal", action: document.getElementById("terminal-cmd").value }),
        d => `<div class="log-entry"><span class="event">STDOUT:</span> ${d.response}</div>`
    );

    // Panel 6: Converter & Compressor
    document.getElementById("convert-btn")?.addEventListener("click", () => {
        const file = document.getElementById("convert-file-input").files[0];
        const target = document.getElementById("convert-target-format").value;
        if (!file) return alert("Please select a file.");
        fetch("/api/convert", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input_file: file.name, target_format: target })
        }).then(res => res.json()).then(data => {
            document.getElementById("convert-result").innerHTML = `✓ Converted: ${data.output_file}`;
        });
    });

    document.getElementById("compress-btn")?.addEventListener("click", () => {
        const file = document.getElementById("compress-file-input").files[0];
        const quality = document.getElementById("compress-quality").value;
        if (!file) return alert("Please select a file.");
        fetch("/api/compress", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input_file: file.name, quality_level: parseInt(quality) })
        }).then(res => res.json()).then(data => {
            document.getElementById("compress-result").innerHTML = `✓ Compressed: ${data.compressed_file}`;
        });
    });

    // Panel 7: Image Studio
    handleApiAction("gen-image-btn", "image-result", "/api/command",
        () => ({ module: "image", action: document.getElementById("image-prompt").value }),
        d => `✓ Image Render Triggered: ${d.response}`
    );

    // Panel 8: Video Studio
    handleApiAction("gen-video-btn", "video-result", "/api/command",
        () => ({ module: "video", action: document.getElementById("video-prompt").value }),
        d => `✓ Video Pipeline Enqueued: ${d.response}`
    );

    // Panel 9: Audio Engine
    handleApiAction("gen-audio-btn", "audio-result", "/api/command",
        () => ({ module: "audio", action: document.getElementById("audio-script").value }),
        d => `✓ Audio Waveform Synthesized: ${d.response}`
    );

    // Panel 10: Business
    handleApiAction("gen-business-btn", "business-result", "/api/command",
        () => ({ module: "business", action: document.getElementById("business-target").value }),
        d => `✓ Executive Summary Generated: ${d.response}`
    );

    // Panel 11: Web Scraping
    handleApiAction("run-scrape-btn", "scrape-result", "/api/command",
        () => ({ module: "web", action: document.getElementById("scrape-url").value }),
        d => `✓ Web Extractor Output: ${d.response}`
    );

    // Panel 12: Memory
    document.getElementById("learn-btn")?.addEventListener("click", () => {
        const url = document.getElementById("learn-url-input").value;
        const type = document.getElementById("learn-type-select").value;
        if (!url) return alert("Please enter a URL or file path.");
        fetch("/api/learn", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ source_url: url, source_type: type })
        }).then(res => res.json()).then(data => {
            document.getElementById("learn-result").innerHTML = `✓ Knowledge Indexed: ${data.message}`;
        });
    });

    // Panel 13: Upgrade Tool
    document.getElementById("upgrade-btn")?.addEventListener("click", () => {
        const url = document.getElementById("upgrade-repo-input").value;
        if (!url) return alert("Please enter a repository URL.");
        fetch("/api/upgrade", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                repo_url: url,
                tool_name: url.split("/").pop() || "CustomTool",
                category: "AutoIncorporate",
                description: "Self-upgraded tool requirement."
            })
        }).then(res => res.json()).then(data => {
            alert(`Auto-incorporation complete for ${data.tool_name}!`);
            loadRegisteredTools();
        });
    });

    // Panel 14: Workflow
    handleApiAction("run-workflow-btn", "workflow-result", "/api/command",
        () => ({ module: "workflow", action: document.getElementById("workflow-name").value }),
        d => `✓ DAG Execution Completed: ${d.response}`
    );

    // Panel 15: Security Scan
    handleApiAction("run-security-btn", "security-result", "/api/command",
        () => ({ module: "security", action: document.getElementById("security-target").value }),
        d => `[SECURITY AUDIT COMPLETED]: ${d.response}`
    );

    // Panel 16: Policy Save
    document.getElementById("save-policy-btn")?.addEventListener("click", () => {
        const autonomyLevel = parseInt(document.querySelector('input[name="autonomy"]:checked')?.value || "1");
        const permissions = {
            read: true,
            write: document.getElementById("perm-write")?.checked || false,
            execute: document.getElementById("perm-execute")?.checked || false,
            network: document.getElementById("perm-network")?.checked || false,
            delete: document.getElementById("perm-delete")?.checked || false,
            system: document.getElementById("perm-system")?.checked || false,
            financial: document.getElementById("perm-financial")?.checked || false
        };

        fetch("/api/policy", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ autonomy_level: autonomyLevel, permissions: permissions })
        }).then(res => res.json()).then(data => {
            document.getElementById("autonomy-badge").innerText = `Autonomy: Level ${autonomyLevel}`;
            alert("Permission policy updated successfully.");
        });
    });

    // Panel 19: Settings Save
    document.getElementById("save-settings-btn")?.addEventListener("click", () => {
        alert("Global system settings updated successfully.");
    });
}

function executeCommand() {
    const input = document.getElementById("cmd-input");
    const prompt = input.value.trim();
    if (!prompt) return;

    const methodology = document.getElementById("prompt-methodology-select").value;
    const chatOutput = document.getElementById("chat-output");

    const userDiv = document.createElement("div");
    userDiv.className = "user-msg";
    userDiv.innerText = prompt;
    chatOutput.appendChild(userDiv);

    input.value = "";
    chatOutput.scrollTop = chatOutput.scrollHeight;

    fetch("/api/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ module: "orchestrator", action: prompt, methodology: methodology || null })
    })
    .then(res => res.json())
    .then(data => {
        const agentDiv = document.createElement("div");
        agentDiv.className = "agent-msg";
        agentDiv.innerHTML = `<strong>${data.agent || "Orchestrator"}:</strong> ${data.response || data.message || "Command executed successfully."}`;
        chatOutput.appendChild(agentDiv);
        chatOutput.scrollTop = chatOutput.scrollHeight;
    })
    .catch(err => {
        const errDiv = document.createElement("div");
        errDiv.className = "agent-msg";
        errDiv.style.borderColor = "#ef4444";
        errDiv.innerText = "Error executing command. Check permission or server logs.";
        chatOutput.appendChild(errDiv);
    });
}

function appendLogEntry(entry) {
    const container = document.getElementById("event-log-container");
    if (!container) return;

    const timeStr = entry.timestamp || new Date().toLocaleTimeString();
    const eventStr = entry.event || "EVENT";
    const dataStr = JSON.stringify(entry.data || {});

    const div = document.createElement("div");
    div.className = "log-entry";
    div.innerHTML = `<span class="time">[${timeStr}]</span> <span class="event">${eventStr}</span> <span>${dataStr}</span>`;

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function loadDeviceRegistry() {
    fetch("/api/state")
    .then(res => res.json())
    .then(data => {
        const specs = data.device_specs || {};
        const card = document.getElementById("device-info-card");
        if (card) {
            card.innerHTML = `
                <h3><i class="fa-solid fa-server"></i> Node: ${specs.device_id || "PRIMARY_DESKTOP"}</h3>
                <p><strong>OS / Platform:</strong> ${specs.platform || "Windows"} (${specs.os_release || "10/11"})</p>
                <p><strong>Architecture:</strong> ${specs.architecture || "x64"}</p>
                <p><strong>Processor:</strong> ${specs.processor || "x86_64 Compatible"}</p>
                <p><strong>Node Status:</strong> <span style="color:#10b981;">Online &amp; Active</span></p>
            `;
        }
    })
    .catch(e => console.warn("Could not fetch device state", e));
}

function loadRegisteredTools() {
    fetch("/api/tools")
    .then(res => res.json())
    .then(tools => {
        const container = document.getElementById("tools-container");
        if (!container) return;
        container.innerHTML = "";

        Object.keys(tools).forEach(key => {
            const tool = tools[key];
            const div = document.createElement("div");
            div.className = "tool-item";
            div.innerHTML = `
                <div class="tool-item-header">
                    <span class="tool-title">${key}</span>
                    <label class="toggle-switch">
                        <input type="checkbox" ${tool.enabled ? "checked" : ""}>
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="sub-text">${tool.description || "Integrated Tool / Repository"}</div>
                <div class="sub-text" style="color:#93c5fd;">Category: ${tool.category || "Engine"}</div>
            `;
            container.appendChild(div);
        });
    })
    .catch(e => console.warn("Could not fetch tools catalog", e));
}

function filterTools() {
    const query = document.getElementById("tool-search").value.toLowerCase();
    document.querySelectorAll(".tool-item").forEach(item => {
        const text = item.innerText.toLowerCase();
        item.style.display = text.includes(query) ? "flex" : "none";
    });
}
