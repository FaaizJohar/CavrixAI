import json
import logging
from typing import Callable, Any, Dict
from enum import Enum
import os

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    SAFE = "SAFE"
    LOW_RISK = "LOW_RISK"
    CONFIRM = "CONFIRM"
    HIGH_RISK = "HIGH_RISK"
    DENY = "DENY"

class PermissionEngine:
    def __init__(self):
        # Default mapping of actions to their risk levels
        self.action_risks = {
            "weather_report": RiskLevel.SAFE,
            "system_monitor": RiskLevel.SAFE,
            "flight_finder": RiskLevel.SAFE,
            "open_app": RiskLevel.LOW_RISK,
            "youtube_video": RiskLevel.LOW_RISK,
            "computer_settings": RiskLevel.LOW_RISK,
            "desktop": RiskLevel.LOW_RISK,
            "file_processor": RiskLevel.SAFE,  # Reading non-sensitive files
            "file_controller": RiskLevel.CONFIRM, # Moving/deleting files
            "send_message": RiskLevel.CONFIRM,
            "computer_control": RiskLevel.CONFIRM, # Shutdown/Restart
            "browser_control": RiskLevel.LOW_RISK,
            "dev_agent": RiskLevel.CONFIRM, # Require confirm for arbitrary code, then run sandboxed
        }
        
    def check_permission(self, action: str, args: Dict[str, Any], token: str = None) -> bool:
        """
        Check if an action is permitted to run.
        If the action requires confirmation, a valid cryptographic token must be provided.
        """
        risk = self._evaluate_risk(action, args)
        
        logger.info(f"Checking permission for action '{action}' with evaluated risk level {risk.value}")
        
        if risk == RiskLevel.DENY:
            logger.warning(f"Action '{action}' explicitly denied by PermissionEngine.")
            return False
            
        if risk in (RiskLevel.SAFE, RiskLevel.LOW_RISK):
            return True
            
        if risk in (RiskLevel.CONFIRM, RiskLevel.HIGH_RISK):
            if not token:
                logger.info(f"Action '{action}' requires confirmation token.")
                return False
                
            # TODO: Validate the token cryptographically against the paired Web session
            # The token must be signed by the web frontend ensuring the user explicitly clicked "Confirm"
            is_valid = self._validate_token(action, token)
            if not is_valid:
                logger.warning(f"Invalid confirmation token provided for action '{action}'.")
            return is_valid
            
        return False

    def _evaluate_risk(self, action: str, args: Dict[str, Any]) -> RiskLevel:
        base_risk = self.action_risks.get(action, RiskLevel.HIGH_RISK)
        
        if action in ("file_processor", "file_controller"):
            path = args.get("path", "")
            if path:
                return self._evaluate_path_risk(path, base_risk)
                
        return base_risk
        
    def _evaluate_path_risk(self, path: str, base_risk: RiskLevel) -> RiskLevel:
        # Example boundary checks
        path_lower = path.lower()
        if any(x in path_lower for x in [".ssh", "credentials", ".env"]):
            return RiskLevel.DENY
        if any(x in path_lower for x in ["system32", "windows", "program files"]):
            return RiskLevel.HIGH_RISK
        if base_risk == RiskLevel.SAFE and any(x in path_lower for x in ["projects", "appdata"]):
            return RiskLevel.CONFIRM # Reading sensitive areas needs confirm
        return base_risk
        
    def _validate_token(self, action: str, token: str) -> bool:
        # Placeholder for actual cryptographic signature verification
        # The token must have been signed by the Web Backend for this specific action & session
        return len(token) > 16

permission_engine = PermissionEngine()
