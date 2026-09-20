
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('term-in');
    const output = document.getElementById('term-out');

    // Global Keyboard Shortcut: Focus Terminal on Enter if not focused
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && document.activeElement !== input && document.activeElement.tagName !== 'BUTTON') {
            input.focus();
        }
    });

    input.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            const cmd = input.value.trim();
            if (!cmd) return;
            
            output.innerHTML += `<div><span style="color:#fff">> ${cmd}</span></div>`;
            input.value = '';
            
            try {
                const res = await fetch('/api/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: cmd })
                });
                const data = await res.json();
                
                let outText = data.output || "No output generated.";
                // Format line breaks for HTML
                outText = outText.replace(/\n/g, '<br>');
                output.innerHTML += `<div style="color:var(--text); padding-left:15px; border-left:2px solid var(--border); margin:5px 0;">${outText}</div>`;
            } catch (err) {
                output.innerHTML += `<div style="color:var(--danger)">System Error: ${err.message}</div>`;
            }
            output.scrollTop = output.scrollHeight;
        }
    });
});
