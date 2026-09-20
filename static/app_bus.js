const categorizedTools = {
    "No-Code & Workflows": ["ToolJet", "n8n", "AppFlowy"],
    "Agents & Browsing": ["browser-use", "OpenHands", "AutoGPT", "CrewAI"],
    "Local LLMs & Inference": ["Ollama", "vLLM", "SGLang", "LiteLLM", "DeepSeek", "Qwen 2.5"],
    "Voice & Multimodal": ["Whisper", "Piper TTS", "Stirling PDF"],
    "RAG & Vectors": ["LangChain", "LlamaIndex", "ChromaDB", "Qdrant", "FAISS", "Unstructured"],
    "Core Infrastructure": ["FastAPI", "Docker Engine", "Kubernetes", "Git Automation", "SQLite Store", "PyPubSub Engine"],
    "App Packaging": ["Tauri Shell", "Electron Builder", "Capacitor", "PyInstaller"]
};

document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("tool-toggles");
    const matrix = document.getElementById("matrix-grid");
    let totalTools = 0;

    Object.entries(categorizedTools).forEach(([category, tools]) => {
        // Build Tool Matrix Cards
        const card = document.createElement("div");
        card.className = "bg-slate-900 border border-slate-800 p-4 rounded";
        card.innerHTML = `<h3 class="text-sky-400 font-bold border-b border-slate-700 pb-2 mb-3">${category}</h3>`;
        
        const list = document.createElement("ul");
        list.className = "text-sm text-slate-300 space-y-1";
        
        tools.forEach((tool) => {
            totalTools++;
            // Matrix Listing
            list.innerHTML += `<li><span class="text-emerald-500 mr-2">?</span>${tool}</li>`;
            
            // Sidebar Toggle
            if (sidebar && totalTools <= 15) { // Show first 15 in sidebar for brevity
                const div = document.createElement("div");
                div.className = "flex justify-between items-center text-xs p-2 bg-slate-800/50 rounded border border-slate-700/50";
                div.innerHTML = `<span class="text-slate-300 font-medium">${tool}</span>
                                 <input type="checkbox" checked onchange="toggleTool('${tool}', this.checked)" class="accent-sky-500 cursor-pointer">`;
                sidebar.appendChild(div);
            }
        });
        card.appendChild(list);
        if (matrix) matrix.appendChild(card);
    });

    document.getElementById("dash-tool-count").innerText = `${totalTools} Loaded`;
    
    // Keyboard shortcuts
    document.addEventListener("keydown", function(e) {
        if (e.altKey && e.key === "1") { switchTab("dashboard"); e.preventDefault(); }
        if (e.altKey && e.key === "2") { switchTab("matrix"); e.preventDefault(); }
        if (e.altKey && e.key === "3") { switchTab("terminal"); e.preventDefault(); }
        if (e.key === "Enter" && document.activeElement.id === "cmd-input") {
            document.getElementById("btn-execute").click();
            e.preventDefault();
        }
    });
});

function switchTab(tabName) {
    document.querySelectorAll(".view-section").forEach(el => el.classList.remove("active"));
    document.getElementById("view-" + tabName).classList.add("active");
    
    document.querySelectorAll("button[id^='tab-']").forEach(btn => btn.classList.remove("active-tab"));
    document.getElementById("tab-" + tabName).classList.add("active-tab");
}

function toggleTool(toolName, isEnabled) {
    fetch("/api/toggle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tool: toolName, enabled: isEnabled })
    }).catch(err => console.log("Backend offline."));
}
