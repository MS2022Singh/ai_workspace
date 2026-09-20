document.addEventListener("keydown", function(e) {
    if (e.altKey && e.key === "1") { switchTab("dashboard"); e.preventDefault(); }
    if (e.altKey && e.key === "2") { switchTab("matrix"); e.preventDefault(); }
    if (e.altKey && e.key === "3") { switchTab("ingest"); e.preventDefault(); }
    if (e.altKey && e.key === "4") { switchTab("studio"); e.preventDefault(); }
    if (e.altKey && e.key === "5") { switchTab("bug"); e.preventDefault(); }
    if (e.altKey && e.key === "6") { switchTab("terminal"); e.preventDefault(); }
    if (e.key === "Enter" && document.activeElement.id === "cmd-input") {
        document.getElementById("btn-execute").click();
        e.preventDefault();
    }
});

function switchTab(tabName) {
    const tabs = ["dashboard", "matrix", "ingest", "studio", "bug", "terminal"];
    tabs.forEach(t => {
        const btn = document.getElementById("tab-" + t);
        if (btn) {
            if (t === tabName) btn.classList.add("active-tab");
            else btn.classList.remove("active-tab");
        }
    });
    console.log("[EventBus] Switched to view:", tabName);
}
