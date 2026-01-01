# MCP Server Clients

This document provides guides for connecting various AI clients to the `smartplaylist` MCP server.

## Gemini CLI

1.  **Run the `smartplaylist` Server**:
    ```bash
    smartplaylist serve
    ```

2.  **Configure Gemini CLI**:
    You can typically configure the Gemini CLI by setting an environment variable. Create a file named `~/.gemini/config.json` and add the following content:
    ```json
    {
      "mcpServers": {
        "smartplaylist": {
          "url": "http://localhost:8000/mcp",
          "name": "SmartPlaylist MCP Server",
          "description": "Manage music playlists with beets library",
          "transport": "http"
        }
      }
    }
    ```

3.  **Usage**:
    You can now call the `smartplaylist` tools from your Opencode.ai agent.

## Claude Code

1.  **Run the `smartplaylist` Server**:
    ```bash
    smartplaylist serve
    ```

2.  **Configure Claude Code**:
    ```json
    {
      "mcpServers": {
        "smartplaylist": {
          "url": "http://localhost:8000/mcp",
          "name": "SmartPlaylist",
          "description": "MCP server for managing music playlists with beets"
        }
      }
    }
    ```
  
3.  **Usage**:
    You can now invoke the `smartplaylist` tools from within the Claude Code extension.

## Opencode

1.  **Run the `smartplaylist` Server**:
    ```bash
    smartplaylist serve
    ```

2.  **Configure OpenCode**:
    ```json
    {
      "mcp": {
        "smartplaylist": {
          "type": "remote",
          "url": "http://personal.local:8000/mcp",
          "enabled": true,
        },
      },
    }
    ```

3.  **Usage**:
    You can now call the `smartplaylist` tools from your Opencode.ai agent.
