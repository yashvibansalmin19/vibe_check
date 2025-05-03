"""
Implementation of the track-change tool for tracking code changes with chat context.
"""

import time
from typing import Dict, Any, List, Optional, Union

import mcp.types as types

# Reference to the global change_history list (will be set by server.py)
change_history = None

async def track_change(
    server_context: Any,
    arguments: Optional[Dict[str, Any]]
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Track a code change and its associated chat context.
    
    Args:
        server_context: The MCP server context
        arguments: Dictionary with file_path, code_change, chat_context, and description
        
    Returns:
        List with a TextContent response
        
    Raises:
        ValueError: If any required arguments are missing
    """
    if not arguments:
        raise ValueError("Missing arguments")

    file_path = arguments.get("file_path")
    code_change = arguments.get("code_change")
    chat_context = arguments.get("chat_context")
    description = arguments.get("description")

    if not all([file_path, code_change, chat_context, description]):
        raise ValueError("Missing required arguments")

    # Add new entry to change history
    change_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "file_path": file_path,
        "code_change": code_change,
        "chat_context": chat_context,
        "description": description,
    }
    
    if change_history is not None:
        change_history.append(change_entry)

    # Notify clients that resources have changed
    await server_context.session.send_resource_list_changed()

    return [
        types.TextContent(
            type="text",
            text=f"Tracked code change in '{file_path}' with description: {description}",
        )
    ]