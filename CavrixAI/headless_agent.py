import asyncio
import argparse
import logging
import sys
from pathlib import Path
from core.desktop_agent import DesktopAgent
from core.permission_engine import permission_engine

# Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("CavrixAgent")

async def main():
    parser = argparse.ArgumentParser(description="Cavrix Headless Desktop Agent")
    parser.add_argument("--gateway", type=str, required=True, help="URL of the Realtime Gateway (e.g. wss://gateway.cavrix.ai)")
    parser.add_argument("--key", type=str, required=True, help="Device Pairing Key")
    
    args = parser.parse_args()
    
    logger.info("Starting Cavrix Headless Desktop Agent...")
    
    # Initialize the desktop agent
    agent = DesktopAgent(gateway_url=args.gateway, device_key=args.key)
    
    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("Agent stopping...")
        await agent.stop()
    except Exception as e:
        logger.error(f"Fatal error in agent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting.")
