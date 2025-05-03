# Vibe Check MCP Server

An MCP server for tracking and reverting code changes based on chat context history. This tool helps non-technical users (vibe coders) build more robust applications by providing tools to track and revert changes when needed.

## Features

### Resources

The server implements a code change tracking system with:
- Custom `vibe://` URI scheme for accessing individual change history entries
- Each change resource contains details about file paths, code changes, and associated chat context
- Changes are stored with timestamps for easy identification and retrieval

### Prompts

The server provides a specialized prompt:
- `suggest-revert`: Analyzes your code change history and suggests which changes to revert
  - Takes "issue_description" as a required argument
  - Generates a prompt that analyzes all tracked changes against your described issue

### Tools

The server implements three tools to manage your code changes:
- `track-change`: Records a new code change with associated chat context
  - Takes "file_path", "code_change", "chat_context", and "description" as required arguments
  - Updates the change history and notifies clients of resource changes
- `revert-change`: Provides information needed to revert a specific change
  - Takes "index" to identify which change to revert
  - Returns the original code and context to help you manually revert the change
- `list-changes`: Displays a summary of all tracked code changes
  - Shows timestamps, descriptions, and file paths for quick reference

## Configuration

### VS Code Integration

Create a `.vscode/mcp.json` file with the following content:

```json
{
  "servers": {
    "vibe-check": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "vibe_check"]
    }
  }
}
```

### AI Assistant Integration

For integration with various AI assistants like Claude, follow the instructions below.

#### Claude Desktop

On Windows: `%APPDATA%/Claude/claude_desktop_config.json`
On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  
  ```json
  "mcpServers": {
    "vibe-check": {
      "command": "python",
      "args": [
        "-m",
        "vibe_check"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  
  ```json
  "mcpServers": {
    "vibe-check": {
      "command": "python",
      "args": [
        "-m",
        "vibe_check"
      ]
    }
  }
  ```
</details>

## Usage

### Track Code Changes

To track a code change, provide:
1. The file path that was changed
2. The actual code change (can be a diff or before/after code snippets)
3. The chat context that led to the change
4. A brief description of the change

### List Your Change History

Use the `list-changes` tool to view all tracked changes.

### Get Help with Reverting

If you encounter issues after making changes:
1. Use the `suggest-revert` prompt with a description of the issue
2. Review the suggestions and choose which changes to revert
3. Use the `revert-change` tool with the index of the change to get revert instructions

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags.

### Debugging

Since MCP servers run over stdio, we recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
npx @modelcontextprotocol/inspector python -m vibe_check
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.