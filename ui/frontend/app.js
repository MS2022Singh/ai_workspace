
document.addEventListener("DOMContentLoaded", () => {
    // Panel Switching Logic
    const navButtons = document.querySelectorAll(".nav-btn");
    const panels = document.querySelectorAll(".workspace-panel");

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            navButtons.forEach(b => b.classList.remove("active"));
            panels.forEach(p => p.classList.add("hidden"));
            
            btn.classList.add("active");
            document.getElementById(btn.dataset.target).classList.remove("hidden");
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
