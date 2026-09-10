# Cavrix AI

**Cavrix AI** is a futuristic, modular AI orchestrator and personal agent. This repository contains the next-generation architecture split into a Web Interface, a Realtime Gateway, and a local Desktop Agent capable of running code and controlling your PC.

## Repository Architecture

```text
Cavrix AI
├── CavrixAI/               # The Desktop Agent (Python)
│   └── Local tool runtime, memory, system control, DevAgent sandbox.
├── Cavrix Web/             # The Web Application (Next.js)
│   ├── app/                # UI, Chat, Settings
│   └── gateway/            # Secure Realtime WebSocket Router
├── shared/                 # Shared Protocol & Schemas
│   └── TypeScript & Python protocol types
└── docs/                   # Architecture & Development Documentation
```

## Getting Started

### 1. Cavrix Web (Frontend)
The primary user interface for Cavrix AI. Built with Next.js, Tailwind CSS, and TypeScript. Deployable directly to Vercel.

**To run locally:**
```bash
cd "Cavrix Web"
npm install
npm run dev
```

### 2. Realtime Gateway (Backend)
The Gateway handles connection routing and device pairing using Supabase authentication and PostgreSQL.

**To run locally:**
```bash
cd "Cavrix Web/gateway"
npm install
npm run start
```
*Requires `SUPABASE_JWT_SECRET` and `DATABASE_URL` in `.env`.*

### 3. CavrixAI (Desktop Agent)
The Windows application that executes high-risk operations, local shell commands, DevAgent sandboxing, and UI automation.

**To run locally:**
```bash
cd CavrixAI
pip install -r requirements.txt
python headless_agent.py --gateway wss://your-gateway-url.com --key YOUR_DEVICE_KEY
```

## Security & Device Pairing

CavrixAI establishes a secure **OUTBOUND** WebSocket connection to the Realtime Gateway. Your PC is never exposed directly to the public internet. 

**Pairing Flow:**
1. Login to **Cavrix Web**.
2. Click "Connect Desktop" to generate a pairing code.
3. Enter the code in the **CavrixAI** Desktop Agent.
4. The Gateway securely associates your device with your user account.

### Permission Engine
All commands sent from the Web UI to the Desktop Agent are evaluated by the local `PermissionEngine`. The Desktop Agent remains the FINAL AUTHORITY for any action. Levels include: `SAFE`, `LOW_RISK`, `CONFIRM`, `HIGH_RISK`, and `DENY`.

## Deployment

**Cavrix Web**: Deploy directly to Vercel. 
**Cavrix Gateway**: Deploy to any Node.js hosting (e.g. Render, Railway) as a persistent websocket server.
**CavrixAI**: Runs as a local background service on your Windows PC.
