export class CavrixWebSocket {
  private ws: WebSocket | null = null;
  private url: string;
  private token: string;
  public onMessage: (msg: any) => void = () => {};
  public onStatusChange: (status: 'connected' | 'disconnected') => void = () => {};

  constructor(url: string, token: string) {
    this.url = url;
    this.token = token;
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.onStatusChange('connected');
      // Send initial auth message if not using headers (browsers don't support custom headers in WebSocket easily)
      // For this implementation, we might send an auth packet first.
      this.ws?.send(JSON.stringify({ type: 'AUTH', token: this.token, clientType: 'WEB' }));
    };

    this.ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        this.onMessage(msg);
      } catch (e) {
        console.error('Failed to parse WebSocket message', e);
      }
    };

    this.ws.onclose = () => {
      this.onStatusChange('disconnected');
      setTimeout(() => this.connect(), 5000); // Auto-reconnect
    };
  }

  send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
