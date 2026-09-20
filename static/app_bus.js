const masterTools = [
    "ToolJet", "n8n", "AppFlowy", "browser-use", "OpenHands", "PyRIT", "Stirling PDF",
    "Ollama", "vLLM", "SGLang", "LiteLLM", "Pair Router", "DeepSeek", "Qwen 2.5",
    "Whisper", "Piper TTS", "AutoGPT", "CrewAI", "LangChain", "LlamaIndex",
    "ChromaDB", "Qdrant", "FAISS", "Unstructured", "FastAPI", "Docker Engine",
    "Kubernetes", "Playwright", "Selenium", "Postman", "Git Automation", "Tauri Shell",
    "Electron Builder", "Capacitor", "PyInstaller", "WazirX/Binance API", "SQLite Store", "PyPubSub Engine"
];

document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("tool-toggles");
    if (!container) return;
    masterTools.forEach((tool, idx) => {
        const div = document.createElement("div");
        div.className = "flex justify-between items-center text-xs p-2 bg-slate-800/50 rounded border border-slate-700/50";
        div.innerHTML = `<span class="text-slate-300 font-medium">${tool}</span>` +
                        `<input type="checkbox" id="tool-${idx}" checked onchange="toggleTool('${tool}', this.checked)" class="accent-sky-500 cursor-pointer">`;
        container.appendChild(div);
    });
});

function toggleTool(toolName, isEnabled) {
    console.log(`[EventBus] Tool ${toolName} toggled -> ${isEnabled}`);
    fetch("/api/toggle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tool: toolName, enabled: isEnabled })
    }).catch(err => console.log("[Local Sync] Backend state logged."));
}
