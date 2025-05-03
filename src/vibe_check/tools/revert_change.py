"""
Implementation of the revert-change tool for reverting previously tracked code changes.
"""

from typing import Dict, Any, List, Optional, Union

import mcp.types as types

# Reference to the global change_history list (will be set by server.py)
change_history = None

async def revert_change(
    server_context: Any,
    arguments: Optional[Dict[str, Any]]
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Provide information to revert a specific code change.
    
    Args:
        server_context: The MCP server context
        arguments: Dictionary with index of the change to revert
        
    Returns:
        List with a TextContent response containing revert instructions
        
    Raises:
        ValueError: If index is missing or invalid
    """
    if not arguments:
        raise ValueError("Missing arguments")

    index = arguments.get("index")
    if index is None or not isinstance(index, int):
        raise ValueError("Missing or invalid index")

    if change_history is None or not change_history:
        raise ValueError("No change history available")
        
    if index < 0 or index >= len(change_history):
        raise ValueError(f"Invalid index: {index}, must be between 0 and {len(change_history) - 1}")

    # Get the change entry
    change_entry = change_history[index]
    
    return [
        types.TextContent(
            type="text",
            text=f"To revert change #{index} in '{change_entry['file_path']}':\n\n"
                 f"1. The original code change was:\n{change_entry['code_change']}\n\n"
                 f"2. This change was made in the context of:\n{change_entry['chat_context']}\n\n"
                 f"3. You should manually revert these changes in your editor.",
        )
    ]