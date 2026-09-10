import os
import shutil
import subprocess
import tempfile
import logging
from pathlib import Path
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class DevAgentSandbox:
    def __init__(self, base_work_dir: Optional[Path] = None):
        """
        Initializes the sandbox. If no base_work_dir is provided, a temporary directory is used.
        """
        if base_work_dir is None:
            self.work_dir = Path(tempfile.mkdtemp(prefix="cavrix_sandbox_"))
        else:
            self.work_dir = Path(base_work_dir).resolve()
            
        logger.info(f"Initialized DevAgent Sandbox at {self.work_dir}")

    def validate_path(self, target_path: str) -> bool:
        """
        Ensures the target path is strictly within the sandbox directory.
        Prevents path traversal attacks (e.g., '../../Windows/System32').
        """
        try:
            resolved_target = (self.work_dir / target_path).resolve()
            return resolved_target.is_relative_to(self.work_dir)
        except Exception:
            return False

    def write_file(self, relative_path: str, content: str) -> bool:
        if not self.validate_path(relative_path):
            logger.error(f"Path traversal detected or invalid path: {relative_path}")
            return False
            
        target = self.work_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    def execute_script(self, relative_script_path: str, timeout_seconds: int = 15) -> Dict[str, str]:
        """
        Executes a Python script strictly within the sandbox environment.
        Enforces a hard timeout to prevent hanging processes.
        """
        if not self.validate_path(relative_script_path):
            return {"error": "Invalid script path or traversal attempt."}

        target_script = self.work_dir / relative_script_path
        if not target_script.exists():
            return {"error": f"Script {relative_script_path} not found."}

        try:
            # We run the script in a subprocess with the sandbox as the CWD
            result = subprocess.run(
                ["python", str(target_script)],
                cwd=str(self.work_dir),
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": str(result.returncode)
            }
        except subprocess.TimeoutExpired:
            return {"error": f"Execution timed out after {timeout_seconds} seconds."}
        except Exception as e:
            return {"error": str(e)}

    def cleanup(self):
        """
        Deletes the sandbox and all its contents.
        """
        try:
            shutil.rmtree(self.work_dir)
            logger.info("Sandbox cleaned up successfully.")
        except Exception as e:
            logger.error(f"Failed to clean up sandbox: {e}")
