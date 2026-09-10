import asyncio
import logging
from typing import Dict, Any
from core.agent_client import AgentClient
from core.permission_engine import permission_engine

logger = logging.getLogger(__name__)

class DesktopAgent:
    """
    The main shell for the Cavrix Desktop Agent.
    Responsible for connecting to the Realtime Gateway and routing tool calls
    from the Web frontend to the local Python action handlers.
    """
    def __init__(self, gateway_url: str, device_key: str):
        self.client = AgentClient(gateway_url, device_key)
        self.tools_registry = self._initialize_tools()
        
        # Override the default handle_message to use our registry if needed,
        # but agent_client.py's _handle_message already uses PermissionEngine.
        # Ideally, we inject our execution logic into it.
        self._inject_tool_executor()
        
    def _initialize_tools(self) -> Dict[str, callable]:
        """
        Maps tool names to their actual Python functions.
        """
        # Lazy imports to avoid circular dependencies
        from actions.computer_control import computer_control
        from actions.open_app import open_app
        from actions.weather_report import weather_action
        
        return {
            "computer_control": computer_control,
            "open_app": open_app,
            "weather_report": weather_action,
            # TODO: Map all other tools here
        }
        
    def _inject_tool_executor(self):
        """
        Replaces the placeholder execution logic in AgentClient 
        with the actual tool execution routing.
        """
        original_handle_message = self.client._handle_message
        
        async def new_handle_message(data: dict):
            # First, let the default handle_message do permission checks
            # In a real implementation, we would structure this better.
            await original_handle_message(data)
            
            # If we need to actually execute it here:
            msg_type = data.get("type")
            if msg_type == "TOOL_CALL":
                payload = data.get("payload", {})
                tool_name = payload.get("tool_name")
                args = payload.get("arguments", {})
                token = data.get("token")
                
                if permission_engine.check_permission(tool_name, args, token):
                    func = self.tools_registry.get(tool_name)
                    if func:
                        try:
                            # Many existing actions are sync, some are async. 
                            # Need to run in executor if sync.
                            if asyncio.iscoroutinefunction(func):
                                result = await func(args)
                            else:
                                result = await asyncio.to_thread(func, args)
                                
                            logger.info(f"Tool {tool_name} executed successfully. Result: {result}")
                            # TODO: Send actual result back
                        except Exception as e:
                            logger.error(f"Error executing {tool_name}: {e}")
                            
        # Override
        # self.client._handle_message = new_handle_message
        pass

    async def start(self):
        logger.info("Starting Desktop Agent...")
        await self.client.connect()

    async def stop(self):
        logger.info("Stopping Desktop Agent...")
        await self.client.stop()
