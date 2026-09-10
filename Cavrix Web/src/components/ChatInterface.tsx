'use client';
import { useState, useEffect } from 'react';
import { CavrixWebSocket } from '../lib/websocket';

export default function ChatInterface() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState('');
  const [status, setStatus] = useState('disconnected');
  const [ws, setWs] = useState<CavrixWebSocket | null>(null);

  useEffect(() => {
    // Ideally this token comes from Supabase auth session
    const dummyToken = "user-jwt-token";
    const socket = new CavrixWebSocket('ws://localhost:8080', dummyToken);
    
    socket.onStatusChange = (newStatus) => setStatus(newStatus);
    socket.onMessage = (msg) => {
      if (msg.type === 'TOOL_RESULT') {
        setMessages((prev) => [...prev, { role: 'agent', content: `[Tool Result] ${msg.payload.tool_name}: ${msg.payload.result}` }]);
      }
      if (msg.type === 'HEARTBEAT') {
         // Desktop agent is online
      }
    };

    socket.connect();
    setWs(socket);

    return () => socket.disconnect();
  }, []);

  const handleSend = () => {
    if (!input.trim()) return;
    
    setMessages((prev) => [...prev, { role: 'user', content: input }]);
    
    // Simulate sending a command that requires a desktop tool call for demonstration
    if (ws) {
      ws.send({
        type: 'TOOL_CALL',
        payload: {
          tool_name: 'computer_control',
          arguments: { action: 'type', text: input }
        }
      });
    }
    
    setInput('');
  };

  return (
    <div className="flex flex-col h-full bg-gray-900 text-white rounded-lg shadow-xl overflow-hidden border border-gray-700">
      <div className="bg-gray-800 p-4 flex justify-between items-center border-b border-gray-700">
        <h2 className="text-lg font-semibold tracking-wider text-teal-400">CAVRIX AI</h2>
        <div className={`px-2 py-1 rounded text-xs ${status === 'connected' ? 'bg-green-600' : 'bg-red-600'}`}>
          Gateway: {status.toUpperCase()}
        </div>
      </div>
      
      <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-4">
        {messages.map((m, i) => (
          <div key={i} className={`p-3 rounded-lg max-w-[80%] ${m.role === 'user' ? 'bg-teal-700 self-end' : 'bg-gray-700 self-start'}`}>
            {m.content}
          </div>
        ))}
      </div>

      <div className="p-4 bg-gray-800 border-t border-gray-700 flex gap-2">
        <input 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          className="flex-1 bg-gray-700 text-white rounded p-2 outline-none border border-gray-600 focus:border-teal-500"
          placeholder="Ask Cavrix or send a command to your PC..."
        />
        <button onClick={handleSend} className="bg-teal-600 hover:bg-teal-500 text-white font-bold py-2 px-4 rounded transition-colors">
          Send
        </button>
      </div>
    </div>
  );
}
