import asyncio
import json
import time
from typing import Dict, List, Optional, Tuple, Union, Any

# Import typing_extensions for Python 3.8 compatibility
try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

# Import tool implementations
from .tools import track_change, revert_change, list_changes

# Store code changes and chat context
change_history: List[Dict[str, Any]] = []

# Share the change_history with the tool modules
track_change.change_history = change_history
revert_change.change_history = change_history
list_changes.change_history = change_history

server = Server("vibe_check")

@server.list_resources()
async def handle_list_resources() -> List[types.Resource]:
    """
    List available change history resources.
    Each change is exposed as a resource with a custom vibe:// URI scheme.
    """
    return [
        types.Resource(
            uri=AnyUrl(f"vibe://history/{i}"),
            name=f"Change #{i}: {entry['description'][:30]}{'...' if len(entry['description']) > 30 else ''}",
            description=f"Code change from {entry['timestamp']}",
            mimeType="application/json",
        )
        for i, entry in enumerate(change_history)
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific change history entry by its URI.
    The entry index is extracted from the URI path component.
    """
    if uri.scheme != "vibe":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    index_str = uri.path
    if index_str is not None:
        index_str = index_str.lstrip("/")
        try:
            index = int(index_str)
            if 0 <= index < len(change_history):
                return json.dumps(change_history[index], indent=2)
        except ValueError:
            pass
    raise ValueError(f"Change history entry not found: {index_str}")

@server.list_prompts()
async def handle_list_prompts() -> List[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="suggest-revert",
            description="Suggests which changes to revert based on your description",
            arguments=[
                types.PromptArgument(
                    name="issue_description",
                    description="Description of the issue you're experiencing",
                    required=True,
                )
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: Optional[Dict[str, str]]
) -> types.GetPromptResult:
    """
    Generate a prompt for suggesting which changes to revert.
    """
    if name != "suggest-revert":
        raise ValueError(f"Unknown prompt: {name}")

    if not arguments or "issue_description" not in arguments:
        raise ValueError("Missing issue description")
    
    issue_description = arguments["issue_description"]
    
    # Create a prompt that includes all change history
    changes_text = ""
    for i, entry in enumerate(change_history):
        changes_text += f"\nChange #{i}: {entry['timestamp']}\n"
        changes_text += f"Description: {entry['description']}\n"
        changes_text += f"File: {entry['file_path']}\n"
        changes_text += f"Code Change:\n{entry['code_change']}\n"
        changes_text += f"Chat Context: {entry['chat_context']}\n"
        changes_text += "-" * 40 + "\n"

    return types.GetPromptResult(
        description="Suggest changes to revert based on issue description",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"I'm experiencing the following issue: {issue_description}\n\n"
                         f"Here is the history of code changes:\n{changes_text}\n\n"
                         f"Based on my issue description, which changes would you recommend reverting? "
                         f"Please list the change numbers and explain your reasoning.",
                ),
            )
        ],
    )

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    List available tools for tracking and reverting code changes.
    """
    return [
        types.Tool(
            name="track-change",
            description="Track a code change and its associated chat context",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "code_change": {"type": "string"},
                    "chat_context": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["file_path", "code_change", "chat_context", "description"],
            },
        ),
        types.Tool(
            name="revert-change",
            description="Revert a specific code change",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "integer"},
                },
                "required": ["index"],
            },
        ),
        types.Tool(
            name="list-changes",
            description="List all tracked code changes",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Optional[Dict[str, Any]]
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Handle tool execution requests for tracking and reverting code changes.
    Routes requests to the appropriate tool implementation.
    """
    if name == "track-change":
        return await track_change.track_change(server.request_context, arguments)
    
    elif name == "revert-change":
        return await revert_change.revert_change(server.request_context, arguments)
    
    elif name == "list-changes":
        return await list_changes.list_changes(server.request_context, arguments)
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="vibe_check",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )