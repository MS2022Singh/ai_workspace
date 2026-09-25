let socket = null;

function connectWebSocket() {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUri = ${wsProtocol}//:8000/ws/stream;
    
    socket = new WebSocket(wsUri);

    socket.onopen = function(e) {
        console.log("[AI Workspace] WebSocket connection established.");
    };

    socket.onmessage = function(event) {
        const message = JSON.parse(event.data);
        handleServerEvent(message);
    };

    socket.onclose = function(event) {
        console.warn("[AI Workspace] WebSocket disconnected. Reconnecting in 3s...");
        setTimeout(connectWebSocket, 3000);
    };

    socket.onerror = function(error) {
        console.error("[AI Workspace] WebSocket error:", error);
    };
}

document.addEventListener('DOMContentLoaded', () => {
    connectWebSocket();
    
    const executeBtn = document.getElementById('execute-btn');
    if (executeBtn) {
        executeBtn.addEventListener('click', submitTask);
    }
    
    const userInput = document.getElementById('user-input');
    if (userInput) {
        userInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                submitTask();
            }
        });
    }
});

function submitTask() {
    const inputField = document.getElementById('user-input');
    if (!inputField) return;
    const taskText = inputField.value.trim();
    if (!taskText) return;

    appendMessage('user', taskText);
    inputField.value = '';

    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ task: taskText }));
    } else {
        appendMessage('system', 'Error: WebSocket connection not active. Please ensure backend server is running.');
    }
}

function handleServerEvent(event) {
    const type = event.type;
    const data = event.data;

    if (type === 'TASK_STARTED') {
        appendMessage('system', 🚀 Task Started: );
    } else if (type === 'AGENT_ACTION') {
        appendMessage(data.agent, ⚙️ );
    } else if (type === 'TASK_COMPLETED') {
        appendMessage('system', ✅ Task Completed Successfully: );
    }
}

function appendMessage(sender, text) {
    const chatContainer = document.getElementById('chat-stream-container');
    if (!chatContainer) return;
    
    const msgDiv = document.createElement('div');
    if (sender === 'user') {
        msgDiv.className = 'ml-auto bg-blue-600 p-3 rounded-lg max-w-xl text-white shadow';
        msgDiv.innerHTML = <p class="text-xs text-blue-200 font-semibold mb-1">YOU</p><p></p>;
    } else if (sender === 'system') {
        msgDiv.className = 'bg-slate-800 p-3 rounded-lg border border-slate-700 text-slate-200 shadow';
        msgDiv.innerHTML = <p class="text-xs text-blue-400 font-semibold mb-1">WORKSPACE OS</p><p></p>;
    } else {
        // Agent messages
        msgDiv.className = 'bg-slate-900 p-3 rounded-lg border border-slate-800 text-slate-200 shadow';
        msgDiv.innerHTML = <p class="text-xs text-emerald-400 font-semibold mb-1"></p><p></p>;
    }
    
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
