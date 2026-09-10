import asyncio
import websockets
import json
import logging
from uuid import uuid4
from packages.shared.protocol.models import (
    BaseMessage, HeartbeatPayload
)

logger = logging.getLogger(__name__)

class AgentClient:
    def __init__(self, gateway_url: str, device_key: str):
        self.gateway_url = gateway_url
        self.device_key = device_key
        self.session_id = uuid4()
        self.websocket = None
        self._running = False
        
    async def connect(self):
        self._running = True
        while self._running:
            try:
                headers = {"Authorization": f"Bearer {self.device_key}"}
                logger.info(f"Connecting to Gateway at {self.gateway_url}...")
                async with websockets.connect(self.gateway_url, additional_headers=headers) as ws:
                    self.websocket = ws
                    logger.info("Connected securely to Gateway.")
                    
                    # Start background tasks
                    heartbeat_task = asyncio.create_task(self._heartbeat_loop())
                    receive_task = asyncio.create_task(self._receive_loop())
                    
                    # Wait until connection drops
                    done, pending = await asyncio.wait(
                        [heartbeat_task, receive_task],
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    
                    # Cancel pending tasks if one fails
                    for task in pending:
                        task.cancel()
                        
            except Exception as e:
                logger.error(f"Connection error: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)
                
    async def stop(self):
        self._running = False
        if self.websocket:
            await self.websocket.close()

    async def _heartbeat_loop(self):
        while self._running and self.websocket:
            try:
                msg = BaseMessage(
                    message_id=uuid4(),
                    session_id=self.session_id,
                    type="HEARTBEAT",
                    payload=HeartbeatPayload(status="online").model_dump()
                )
                await self.websocket.send(msg.model_dump_json())
                await asyncio.sleep(30)
            except Exception as e:
                logger.error(f"Heartbeat failed: {e}")
                break

    async def _receive_loop(self):
        while self._running and self.websocket:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)
                await self._handle_message(data)
            except websockets.ConnectionClosed:
                logger.warning("Gateway connection closed by remote.")
                break
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                
    async def _handle_message(self, data: dict):
        msg_type = data.get("type")
        logger.info(f"Received message: {msg_type}")
        
        if msg_type == "TOOL_CALL":
            from core.permission_engine import permission_engine
            from packages.shared.protocol.models import ToolResultMessage, ToolResultPayload, MessageType
            
            payload = data.get("payload", {})
            tool_name = payload.get("tool_name")
            args = payload.get("arguments", {})
            token = data.get("token") # Assuming a token is passed alongside for confirmation
            
            # Check permissions
            is_permitted = permission_engine.check_permission(tool_name, args, token)
            
            if not is_permitted:
                logger.warning(f"Tool call '{tool_name}' blocked by Permission Engine.")
                error_msg = ToolResultMessage(
                    session_id=str(self.session_id),
                    payload=ToolResultPayload(
                        tool_name=tool_name,
                        result=None,
                        error="Blocked by Permission Engine. Confirmation required."
                    )
                )
                await self.websocket.send(error_msg.model_dump_json())
                return
                
            logger.info(f"Executing tool '{tool_name}'...")
            
            # TODO: Import and execute the actual tool from actions/
            # For now, simulate success
            success_msg = ToolResultMessage(
                session_id=str(self.session_id),
                payload=ToolResultPayload(
                    tool_name=tool_name,
                    result=f"Simulated execution of {tool_name}",
                    error=None
                )
            )
            await self.websocket.send(success_msg.model_dump_json())
