"""
Implementation of the list-changes tool for displaying all tracked code changes.
"""

from typing import Dict, Any, List, Optional, Union

import mcp.types as types

# Reference to the global change_history list (will be set by server.py)
change_history = None

async def list_changes(
    server_context: Any,
    arguments: Optional[Dict[str, Any]]
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    List all tracked code changes.
    
    Args:
        server_context: The MCP server context
        arguments: Optional arguments (not used for this tool)
        
    Returns:
        List with a TextContent response containing the change history
    """
    if change_history is None or len(change_history) == 0:
        return [
            types.TextContent(
                type="text",
                text="No code changes have been tracked yet.",
            )
        ]
    
    changes_text = "Code Change History:\n\n"
    for i, entry in enumerate(change_history):
        changes_text += f"Change #{i}: {entry['timestamp']}\n"
        changes_text += f"Description: {entry['description']}\n"
        changes_text += f"File: {entry['file_path']}\n"
        changes_text += "-" * 40 + "\n"
    
    return [
        types.TextContent(
            type="text",
            text=changes_text,
        )
    ]