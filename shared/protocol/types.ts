export enum MessageType {
  COMMAND = "COMMAND",
  TOOL_CALL = "TOOL_CALL",
  TOOL_RESULT = "TOOL_RESULT",
  AGENT_STATUS = "AGENT_STATUS",
  DEVICE_STATUS = "DEVICE_STATUS",
  VOICE_START = "VOICE_START",
  VOICE_STOP = "VOICE_STOP",
  SCREEN_CAPTURE = "SCREEN_CAPTURE",
  CAMERA_FRAME = "CAMERA_FRAME",
  FILE_REQUEST = "FILE_REQUEST",
  FILE_RESULT = "FILE_RESULT",
  MEMORY_REQUEST = "MEMORY_REQUEST",
  MEMORY_RESULT = "MEMORY_RESULT",
  CONFIRMATION_REQUEST = "CONFIRMATION_REQUEST",
  CONFIRMATION_RESULT = "CONFIRMATION_RESULT",
  ERROR = "ERROR",
  HEARTBEAT = "HEARTBEAT",
  SESSION_START = "SESSION_START",
  SESSION_END = "SESSION_END"
}

export interface BaseMessage {
  message_id: string;
  session_id: string;
  timestamp: string; // ISO 8601 string
  type: MessageType;
}

export interface ToolCallPayload {
  tool_name: string;
  arguments: Record<string, any>;
}

export interface ToolCallMessage extends BaseMessage {
  type: MessageType.TOOL_CALL;
  payload: ToolCallPayload;
}

export interface ToolResultPayload {
  tool_name: string;
  result: any;
  error?: string;
}

export interface ToolResultMessage extends BaseMessage {
  type: MessageType.TOOL_RESULT;
  payload: ToolResultPayload;
}

export interface HeartbeatMessage extends BaseMessage {
  type: MessageType.HEARTBEAT;
  payload: {
    status: 'online' | 'offline' | 'idle';
  };
}

export interface ErrorMessage extends BaseMessage {
  type: MessageType.ERROR;
  payload: {
    code: string;
    message: string;
    details?: any;
  };
}

// Add other specific payload types as needed
export type CavrixMessage = 
  | ToolCallMessage 
  | ToolResultMessage 
  | HeartbeatMessage 
  | ErrorMessage
  | (BaseMessage & { payload: any }); // Fallback for now
