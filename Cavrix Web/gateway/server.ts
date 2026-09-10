import { WebSocketServer, WebSocket } from 'ws';
import { v4 as uuidv4 } from 'uuid';
import http from 'http';
import { PrismaClient } from '@prisma/client';
// For Supabase JWT validation, normally we'd use something like jsonwebtoken
import jwt from 'jsonwebtoken';

const PORT = process.env.PORT || 8080;
const server = http.createServer();
const wss = new WebSocketServer({ server });
const prisma = new PrismaClient();

interface ConnectedClient {
  ws: WebSocket;
  id: string; // Device ID or Session ID
  userId: string;
  type: 'WEB' | 'AGENT';
}

const clients: Map<string, ConnectedClient> = new Map();

wss.on('connection', async (ws, req) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    ws.close(4001, 'Unauthorized');
    return;
  }

  const clientType = req.headers['x-client-type'] === 'WEB' ? 'WEB' : 'AGENT';
  let userId: string | null = null;
  let clientId: string = uuidv4();

  try {
    if (clientType === 'AGENT') {
      // Validate device key for agent
      const device = await prisma.device.findUnique({
        where: { deviceKey: token }
      });
      if (!device) throw new Error('Invalid device key');
      
      userId = device.userId;
      clientId = device.id;
      
      // Update presence
      await prisma.device.update({
        where: { id: device.id },
        data: { status: 'online', lastSeen: new Date() }
      });
    } else {
      // Validate JWT for Web Client (Supabase auth)
      // Note: Needs SUPABASE_JWT_SECRET
      const secret = process.env.SUPABASE_JWT_SECRET || 'dummy-secret';
      const decoded = jwt.verify(token, secret) as { sub: string };
      userId = decoded.sub;
    }
  } catch (err) {
    console.error('Auth failed', err);
    ws.close(4001, 'Unauthorized');
    return;
  }

  if (!userId) {
    ws.close(4001, 'Unauthorized');
    return;
  }

  clients.set(clientId, { ws, id: clientId, userId, type: clientType });
  console.log(`[+] Connected: ${clientType} (${clientId}) for User ${userId}`);

  ws.on('message', async (messageAsString) => {
    try {
      const message = JSON.parse(messageAsString.toString());
      console.log(`Received ${message.type} from ${clientType}`);

      if (message.type === 'HEARTBEAT' && clientType === 'AGENT') {
         await prisma.device.update({
            where: { id: clientId },
            data: { status: message.payload?.status || 'online', lastSeen: new Date() }
         });
         return; // Don't route heartbeats to WEB
      }

      // Routing Logic:
      // Route only to clients belonging to the SAME user, but of the OPPOSITE type
      for (const [id, client] of clients.entries()) {
        if (client.userId === userId && client.type !== clientType && client.ws.readyState === WebSocket.OPEN) {
          client.ws.send(JSON.stringify(message));
        }
      }

    } catch (e) {
      console.error('Failed to parse or route message', e);
    }
  });

  ws.on('close', async () => {
    console.log(`[-] Disconnected: ${clientType} (${clientId})`);
    clients.delete(clientId);
    
    if (clientType === 'AGENT') {
      try {
        await prisma.device.update({
          where: { id: clientId },
          data: { status: 'offline', lastSeen: new Date() }
        });
      } catch (err) {
        console.error('Failed to update device status to offline', err);
      }
    }
  });
});

server.listen(PORT, () => {
  console.log(`Cavrix Realtime Gateway listening on port ${PORT}`);
});
