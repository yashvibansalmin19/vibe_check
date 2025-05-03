# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("vibe-version")

@mcp.tool()
def commit_changes() -> bool:
    """Show the git status, add all the untracked files, and commit them"""
    import subprocess
    # Show the git status
    subprocess.run(["git", "status"])
    try:
        # Add all untracked files
        subprocess.run(["git", "add", "-A"])
        # Commit the changes
        subprocess.run(["git", "commit", "-m", "Auto-commit by MCP"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error committing changes: {e}")
        return False

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