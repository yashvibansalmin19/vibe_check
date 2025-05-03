from . import server
import asyncio
import sys

def main():
    """Main entry point for the package."""
    # Python 3.7+ supports asyncio.run, but with different error handling
    # across versions
    try:
        asyncio.run(server.main())
    except AttributeError:
        # For older Python versions that don't have asyncio.run
        loop = asyncio.get_event_loop()
        loop.run_until_complete(server.main())
        loop.close()

# Optionally expose other important items at package level
__all__ = ['main', 'server']