# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("vibe-version")

@mcp.tool()
def commit_changes() -> str:
    """Commit and backup all the changes in the current git repository"""
    import subprocess
    import openai
    from os import environ

    print("Starting commit_changes function...")
    # Show the git status
    git_status = subprocess.run(["git", "status"], capture_output=True, text=True)
    # Check if there are any changes to commit
    if git_status.returncode != 0:
        print("No changes to commit.")
        return False
    if "nothing to commit" in git_status.stdout:
        print("No changes to commit.")
        return False
    # Get the git diff to summarize changes
    result = subprocess.run(["git", "diff"], capture_output=True, text=True)
    diff_output = result.stdout

    # Use an LLM to summarize the changes
    openai.api_key = environ.get("OPENAI_API_KEY")
    print("OpenAI API Key:", openai.api_key)
    if not openai.api_key:
        raise ValueError("OpenAI API key is not set in the environment variables.")
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or another compatible chat model
        messages=[
            {"role": "user", "content": f"Summarize the following git diff for a commit message:\n{diff_output}"}
        ],
        max_tokens=50
    )
    commit_message = response.choices[0].message.content.strip()

    # Add all untracked files
    subprocess.run(["git", "add", "-A"])
    # Commit the changes with the generated message
    subprocess.run(["git", "commit", "-m", commit_message])

    committed_diff_stat = subprocess.run(["git", "diff", "HEAD^", "--stat"], capture_output=True, text=True)
    return f"The following changes were backed up in the version history: {committed_diff_stat.stdout}"

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