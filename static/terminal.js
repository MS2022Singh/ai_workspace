document.addEventListener("DOMContentLoaded", function() {
    const btn = document.getElementById("btn-execute");
    const input = document.getElementById("cmd-input");
    const outputView = document.getElementById("terminal-output");

    btn.addEventListener("click", async () => {
        const cmd = input.value.trim();
        if (!cmd) return;
        
        // Auto-switch to terminal tab on execution
        switchTab('terminal');

        const cmdLine = document.createElement("div");
        cmdLine.className = "text-sky-400 font-mono text-sm mt-3 font-bold";
        cmdLine.innerText = "C:\\AI_Workspace> " + cmd;
        outputView.appendChild(cmdLine);
        
        input.value = ""; 
        outputView.scrollTop = outputView.scrollHeight;
        
        try {
            const res = await fetch("/api/execute", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command: cmd })
            });
            const data = await res.json();
            
            const outLine = document.createElement("div");
            outLine.className = data.status === "success" 
                ? "text-slate-300 font-mono text-sm whitespace-pre-wrap mt-1" 
                : "text-red-400 font-mono text-sm whitespace-pre-wrap mt-1";
            outLine.innerText = data.output || "[Process completed]";
            outputView.appendChild(outLine);
            outputView.scrollTop = outputView.scrollHeight;
        } catch (err) {
            const errLine = document.createElement("div");
            errLine.className = "text-red-500 font-mono text-sm mt-1";
            errLine.innerText = "Error: Could not reach execution server.";
            outputView.appendChild(errLine);
        }
    });
});
