# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("vibe-version")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def git_history() -> str:
    """Get the git history"""
    import subprocess
    result = subprocess.run(["git", "log", "--oneline", "--graph"], capture_output=True, text=True)
    return result.stdout

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()