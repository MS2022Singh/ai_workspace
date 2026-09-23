import os

print("[+] Writing synchronized frontend app.js...")

app_js_content = """document.addEventListener("DOMContentLoaded", () => {
    // 1. Navigation Panel Switching
    const navButtons = document.querySelectorAll(".nav-btn");
    const panels = document.querySelectorAll(".workspace-panel");

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            navButtons.forEach(b => b.classList.remove("active"));
            panels.forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            const targetId = btn.getAttribute("data-target");
            const targetPanel = document.getElementById(targetId);
            if(targetPanel) {
                targetPanel.classList.add("active");
            }
        });
    });

    // 2. Chat & Command Submission via Event Bus
    const sendBtn = document.getElementById("send-btn");
    const mainInput = document.getElementById("main-input");
    const chatStream = document.getElementById("chat-stream");

    async function submitCommand(panelId, commandText) {
        if (!commandText.trim()) return;

        // Append user message
        const userMsg = document.createElement("div");
        userMsg.className = "message user-msg";
        userMsg.innerHTML = `<div class="msg-content"><p>${escapeHtml(commandText)}</p></div>`;
        chatStream.appendChild(userMsg);
        chatStream.scrollTop = chatStream.scrollHeight;

        try {
            const res = await fetch("/api/command", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ panel: panelId, command: commandText })
            });
            const data = await res.json();

            // Append system response
            const sysMsg = document.createElement("div");
            sysMsg.className = "message system-msg";
            sysMsg.innerHTML = `<div class="msg-avatar"><i class="fas fa-robot"></i></div><div class="msg-content"><p>${escapeHtml(data.message)}</p></div>`;
            chatStream.appendChild(sysMsg);
            chatStream.scrollTop = chatStream.scrollHeight;
        } catch (err) {
            console.error("Command dispatch failed:", err);
        }
    }

    if(sendBtn && mainInput) {
        sendBtn.addEventListener("click", () => {
            const val = mainInput.value;
            mainInput.value = "";
            submitCommand("chat-panel", val);
        });

        mainInput.addEventListener("keydown", (e) => {
            if(e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendBtn.click();
            }
        });
    }

    // 3. Tool Toggles Synchronization
    document.querySelectorAll(".tool-item input[type='checkbox']").forEach(toggle => {
        toggle.addEventListener("change", async (e) => {
            const toolName = e.target.closest(".tool-item").querySelector(".tool-name").innerText;
            const enabled = e.target.checked;
            try {
                await fetch("/api/toggle-tool", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ tool: toolName, enabled: enabled })
                });
                console.log(`Tool ${toolName} updated to ${enabled}`);
            } catch (err) {
                console.error("Failed to update tool state", err);
            }
        });
    });
});

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
"""

with open("ui/frontend/app.js", "w", encoding="utf-8") as f:
    f.write(app_js_content)

print("[+] Synchronized app.js written successfully.")
