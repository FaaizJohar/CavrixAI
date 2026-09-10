from enum import Enum
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field
import datetime
import uuid

class MessageType(str, Enum):
    COMMAND = "COMMAND"
    TOOL_CALL = "TOOL_CALL"
    TOOL_RESULT = "TOOL_RESULT"
    AGENT_STATUS = "AGENT_STATUS"
    DEVICE_STATUS = "DEVICE_STATUS"
    VOICE_START = "VOICE_START"
    VOICE_STOP = "VOICE_STOP"
    SCREEN_CAPTURE = "SCREEN_CAPTURE"
    CAMERA_FRAME = "CAMERA_FRAME"
    FILE_REQUEST = "FILE_REQUEST"
    FILE_RESULT = "FILE_RESULT"
    MEMORY_REQUEST = "MEMORY_REQUEST"
    MEMORY_RESULT = "MEMORY_RESULT"
    CONFIRMATION_REQUEST = "CONFIRMATION_REQUEST"
    CONFIRMATION_RESULT = "CONFIRMATION_RESULT"
    ERROR = "ERROR"
    HEARTBEAT = "HEARTBEAT"
    SESSION_START = "SESSION_START"
    SESSION_END = "SESSION_END"

class BaseMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    timestamp: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    type: MessageType
    payload: Dict[str, Any] = Field(default_factory=dict)

class ToolCallPayload(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

class ToolCallMessage(BaseMessage):
    type: MessageType = MessageType.TOOL_CALL
    payload: ToolCallPayload

class ToolResultPayload(BaseModel):
    tool_name: str
    result: Any
    error: Optional[str] = None

class ToolResultMessage(BaseMessage):
    type: MessageType = MessageType.TOOL_RESULT
    payload: ToolResultPayload

class HeartbeatPayload(BaseModel):
    status: str

class HeartbeatMessage(BaseMessage):
    type: MessageType = MessageType.HEARTBEAT
    payload: HeartbeatPayload

class ErrorPayload(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ErrorMessage(BaseMessage):
    type: MessageType = MessageType.ERROR
    payload: ErrorPayload
