# filepath: /Users/harshitchoudhary/Desktop/TBH/vibe_check/src/vibe_check/__main__.py
"""
Entry point for the Vibe Check MCP server.
"""

import asyncio

from .server import main

if __name__ == "__main__":
    asyncio.run(main())