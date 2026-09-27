export class WebSocketClient {
    private ws: WebSocket | null = null;
    private url: string;

    constructor(url: string = 'ws://localhost:8000/ws') {
        this.url = url;
    }

    connect(onMessage: (data: any) => void) {
        this.ws = new WebSocket(this.url);
        
        this.ws.onopen = () => console.log('Connected to AI OS Event Bus');
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            onMessage(data);
        };
        
        this.ws.onclose = () => {
            console.log('Disconnected. Attempting reconnect...');
            setTimeout(() => this.connect(onMessage), 3000);
        };
    }

    send(topic: string, payload: any) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ topic, payload }));
        } else {
            console.error('WebSocket is not connected.');
        }
    }
}

export const wsClient = new WebSocketClient();
