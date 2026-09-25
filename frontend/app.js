document.getElementById('execute-btn').addEventListener('click', submitTask);
document.getElementById('user-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submitTask();
    }
});

function submitTask() {
    const inputField = document.getElementById('user-input');
    const taskText = inputField.value.trim();
    if (!taskText) return;

    appendMessage('user', taskText);
    inputField.value = '';

    streamAgentResponse(taskText);
}

function appendMessage(sender, text) {
    const chatContainer = document.getElementById('chat-stream-container');
    const msgDiv = document.createElement('div');
    msgDiv.className = sender === 'user' ? 'ml-auto bg-blue-600 p-3 rounded-lg max-w-xl text-white' : 'bg-slate-800 p-4 rounded-lg border border-slate-700 text-slate-200';
    msgDiv.innerHTML = <p class="text-xs text-slate-400 font-semibold mb-1"></p><p></p>;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
