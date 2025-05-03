<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Vibe Check MCP Server Development Instructions

This project is a Model Context Protocol (MCP) server called "Vibe Check" that helps non-technical users track and revert code changes based on chat context history.

## Project Purpose

Vibe Check is designed to increase productivity of non-technical "vibe coders" by providing tools to build robust applications with the ability to track and revert changes. The server maintains a history of code changes along with the chat context that led to those changes, allowing users to easily understand and roll back problematic changes when needed.

## Key Components

1. **Change History Tracking**: Store code changes with chat context, file paths, and descriptions
2. **Resource Management**: Implement the MCP resource interface for accessing change history entries
3. **Tool Implementation**: Provide tools for tracking, listing, and reverting code changes
4. **Prompt Generation**: Create prompts that help analyze and identify problematic changes

## Development Guidelines

When modifying or extending this project:

1. Follow the MCP protocol specifications from https://modelcontextprotocol.io/llms-full.txt
2. Maintain backward compatibility for existing tools and resources
3. Use clear, descriptive error messages to help non-technical users understand issues
4. Document new features thoroughly in both code comments and the README.md
5. Implement proper error handling and validation for all user inputs
6. Keep the code modular and well-organized for future extension

You can find more information about the MCP SDK at https://github.com/modelcontextprotocol/python-sdk

## Planned Features

When implementing new features, consider:
1. Persistence of change history between sessions
2. Automatic application of reverts (not just instructions)
3. Change categorization and tagging
4. Integration with version control systems
5. Visualization of change history