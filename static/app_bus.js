document.addEventListener('DOMContentLoaded', () => {
    console.log("[EVENT BUS] Initialized UI event bindings.");

    // Ingest Button Binding
    const ingestBtn = document.querySelector('.Ingest\\ &\\ Merge, button:contains("Ingest"), #ingest-btn') || document.querySelectorAll('button')[0];
    const ingestInput = document.querySelector('input[placeholder*="Paste GitHub URL"]');

    // Cognitive Framework Quick Prompt Buttons
    const cognitiveBtns = document.querySelectorAll('.COGNITIVE\\ FRAMEWORKS button, button');

    cognitiveBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const text = btn.innerText.toLowerCase();
            let key = 'genius';
            if (text.includes('master')) key = 'master';
            if (text.includes('mental blocks')) key = 'blocks';
            if (text.includes('clarity')) key = 'clarity';
            if (text.includes('phd')) key = 'phd';
            if (text.includes('framework')) key = 'framework';

            const termInput = document.querySelector('input[placeholder*="Enter cmd"]');
            const topic = termInput ? termInput.value : '';

            const res = await fetch('/api/cognitive', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ framework: key, topic: topic })
            });
            const data = await res.json();
            
            const termOutput = document.querySelector('.EVENT\\ BUS\\ \\/\\ I-O\\ TERMINAL, pre, code, .terminal-body') || document.body;
            console.log(data);
        });
    });
});
