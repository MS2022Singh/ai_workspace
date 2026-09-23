
document.addEventListener("DOMContentLoaded", () => {
    // Navigation Panel Switching
    const navBtns = document.querySelectorAll(".nav-btn");
    const panels = document.querySelectorAll(".workspace-panel");

    navBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            navBtns.forEach(b => b.classList.remove("active"));
            panels.forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            const targetId = btn.getAttribute("data-target");
            const target = document.getElementById(targetId);
            if(target) target.classList.add("active");
        });
    });

    // Chat Command Handling
    const sendBtn = document.getElementById("send-btn");
    const mainInput = document.getElementById("main-input");
    const chatStream = document.getElementById("chat-stream");

    async function sendCommand(actionText, module="Chat Hub") {
        if(!actionText.trim()) return;

        // User Message
        const userDiv = document.createElement("div");
        userDiv.className = "message user";
        userDiv.innerHTML = `<div class="msg-bubble"><p>${escapeHtml(actionText)}</p></div>`;
        chatStream.appendChild(userDiv);
        chatStream.scrollTop = chatStream.scrollHeight;

        mainInput.value = "";

        try {
            const res = await fetch("/api/command", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ module: module, action: actionText })
            });
            const data = await res.json();

            // System Response
            const sysDiv = document.createElement("div");
            sysDiv.className = "message system";
            sysDiv.innerHTML = `<div class="msg-bubble"><p>${escapeHtml(data.response)}</p></div>`;
            chatStream.appendChild(sysDiv);
            chatStream.scrollTop = chatStream.scrollHeight;
        } catch (err) {
            console.error("Command execution failed:", err);
        }
    }

    if(sendBtn && mainInput) {
        sendBtn.addEventListener("click", () => sendCommand(mainInput.value));
        mainInput.addEventListener("keydown", (e) => {
            if(e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendCommand(mainInput.value);
            }
        });
    }

    // Prompt Framework Injector
    window.injectFramework = function(type) {
        if(type === 'genius') mainInput.value = "I want to understand [insert topic] as if I were a genius. Break down concept using advanced analogies, real world applications, counterexamples and multiple perspectives.";
        if(type === 'skill') mainInput.value = "Assume you're a master of [insert skill] with 20+ years of experience. Reverse engineer the process and build a day-by-day plan using free/low-cost resources.";
        if(type === 'blocks') mainInput.value = "I have been struggling with [insert personal issue]. Analyze it like a cognitive scientist, identify root causes, and design a habit loop.";
        if(type === 'clarity') mainInput.value = "I don't understand [insert complex concept]. Break it down step-by-step using metaphors and create a permanent mental shortcut.";
        if(type === 'phd') mainInput.value = "Teach me [insert topic] like I'm preparing for a PhD. Start from first principles, foundational theories, and historical evolution.";
        if(type === 'frameworks') mainInput.value = "I'm trying to master [insert skill/topic]. Build me a custom mental model or decision framework.";
        if(type === 'upgrade') mainInput.value = "Design a 30-day brain upgrade program including high IQ thinking routines, memory techniques, and rest habits.";
        mainInput.focus();
    };

    // Tool Registry Toggles
    document.querySelectorAll(".tool-toggle-item input").forEach(checkbox => {
        checkbox.addEventListener("change", async (e) => {
            const item = e.target.closest(".tool-toggle-item");
            const toolName = item.getAttribute("data-tool");
            const category = item.getAttribute("data-category");
            const enabled = e.target.checked;

            await fetch("/api/toggle-tool", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ category: category, tool: toolName, enabled: enabled })
            });
        });
    });
});

function escapeHtml(text) {
    const map = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'};
    return text.replace(/[&<>"']/g, m => map[m]);
}
