# server.py
from mcp.server.fastmcp import FastMCP
import subprocess
import re
from typing import List, Dict
import subprocess
import openai
from os import environ


# Create an MCP server
mcp = FastMCP("vibe-version")

@mcp.tool()
def commit_changes() -> str:
    """Commit and backup all the changes in the current git repository"""
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
def git_history() -> List[Dict[str, str]]:
    """Get the git history as a list of commits"""
    result = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True)
    log_output = result.stdout.strip()
    commits = []
    for line in log_output.splitlines():
        match = re.match(r"([a-f0-9]+)\s+(.*)", line)
        if match:
            hash = match.group(1)
            description = match.group(2)
            commits.append({"hash": hash, "description": description})
    return commits

@mcp.tool()
def checkout_commit(commit_hash: str) -> str:
    """Checkout a specific git commit"""
    try:
        subprocess.run(["git", "checkout", commit_hash], check=True, capture_output=True, text=True)
        return f"Successfully checked out commit: {commit_hash}"
    except subprocess.CalledProcessError as e:
        return f"Error checking out commit {commit_hash}: {e.stderr}"

@mcp.tool()
def ensure_git_remote() -> str:
    """Check if the current repository has a git remote set. If not, create a repository on GitHub and link it."""
    import subprocess
    import os
    import requests

    try:
        # Check if a remote is set
        result = subprocess.run(["git", "remote"], capture_output=True, text=True)
        if result.stdout.strip():
            return "Git remote is already set."

        # Get GitHub credentials from environment variables
        github_token = os.getenv("GITHUB_TOKEN")
        github_user = os.getenv("GITHUB_USER")
        if not github_token or not github_user:
            return "GitHub credentials (GITHUB_TOKEN and GITHUB_USER) are not set in environment variables."

        # Get the current directory name as the repo name
        repo_name = os.path.basename(os.getcwd())

        # Create a new repository on GitHub
        headers = {"Authorization": f"token {github_token}"}
        data = {"name": repo_name, "private": False}
        response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)

        if response.status_code != 201:
            return f"Failed to create GitHub repository: {response.json().get('message', 'Unknown error')}"

        # Extract the clone URL from the response
        clone_url = response.json().get("clone_url")
        if not clone_url:
            return "Failed to retrieve clone URL from GitHub response."

        # Add the remote to the local repository
        subprocess.run(["git", "remote", "add", "origin", clone_url])
        return f"GitHub repository created and linked: {clone_url}"

    except Exception as e:
        return f"An error occurred: {e}"

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()