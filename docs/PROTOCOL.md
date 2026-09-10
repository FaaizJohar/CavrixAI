# Cavrix AI — Shared Protocol

The Web app and Desktop Agent communicate using a unified JSON protocol over WebSockets. Every message adheres to the following envelope:

```json
{
  "message_id": "uuid-v4",
  "session_id": "uuid-v4",
  "timestamp": "2026-09-09T12:00:00Z",
  "type": "MESSAGE_TYPE",
  "payload": { ... }
}
```

## Core Message Types

### 1. Agent Status & Heartbeat
- `HEARTBEAT`: Sent by the Agent every 30 seconds to maintain connection.
- `AGENT_STATUS`: Reports system telemetry (CPU, RAM) and online status.

### 2. Tool Execution
- `TOOL_CALL`: Sent from Web to Agent requesting an action.
  - Payload: `{"action": "open_app", "args": {"app_name": "Spotify"}}`
- `TOOL_RESULT`: Sent from Agent to Web containing the outcome.
  - Payload: `{"action": "open_app", "status": "success", "data": "Opened Spotify"}`

### 3. Voice & Media
- `VOICE_START` / `VOICE_STOP`: Signals audio streaming initiation/termination.
- `SCREEN_CAPTURE` / `CAMERA_FRAME`: Streams binary or base64 visual data from Agent to Web for Vision models.

### 4. Permissions & Confirmations
- `CONFIRMATION_REQUEST`: Sent by Agent to Web when a `CONFIRM` action is intercepted.
- `CONFIRMATION_RESULT`: Sent by Web to Agent containing the user's cryptographic approval token.

### 5. Memory Sync
- `MEMORY_REQUEST` / `MEMORY_RESULT`: Synchronizes local long-term memory to the Web view.

### 6. Errors
- `ERROR`: Standardized error reporting.
  - Payload: `{"code": "PERMISSION_DENIED", "message": "Access to private folder blocked."}`
