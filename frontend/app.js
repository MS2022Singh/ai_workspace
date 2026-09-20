document.addEventListener('DOMContentLoaded', () => {
    const ingestBtn = document.getElementById('btn-ingest');
    const repoInput = document.getElementById('repo-url');
    const toggles = document.querySelectorAll('.toggle-switch input');

    const executeIngestion = () => {
        const url = repoInput.value.trim();
        if(url) {
            console.log(`[System] Initiating dynamic ingestion for: ${url}`);
            alert(`Initiating ingestion protocol for: ${url}\nSee backend console for build tasks.`);
            repoInput.value = '';
        }
    };

    ingestBtn.addEventListener('click', executeIngestion);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && document.activeElement === repoInput) {
            e.preventDefault();
            executeIngestion();
        }
        if (e.ctrlKey && e.key.toLowerCase() === 'i') {
            e.preventDefault();
            repoInput.focus();
        }
        if (e.ctrlKey && e.key.toLowerCase() === 't') {
            e.preventDefault();
            const firstState = toggles[0].checked;
            toggles.forEach(t => t.checked = !firstState);
            console.log(`[System] All tools set to ${!firstState ? 'Active' : 'Inactive'}`);
        }
    });

    toggles.forEach(toggle => {
        toggle.addEventListener('change', (e) => {
            console.log(`[Permission] Tool state changed: ${e.target.id} -> ${e.target.checked}`);
        });
    });
});