# MCP Server API Guide

The MCP server gives you programmatic access to your music library through a simple API.

**Run the server:**

The recommended way to run the server is by using the `serve` command from the CLI:

```bash
smartplaylist serve
```

For development, you can use a file watcher to automatically restart the server when code changes are detected.

Make sure your `SMARTPLAYLIST_CONFIG_PATH` is set correctly in your `.env` file or as an environment variable before running the server.

The server exposes a single `/mcp` endpoint for all tool calls. The previous `/` endpoint is no longer available.

**Available Tools:**

To interact with the server, you need a client that supports the Model-Context-Protocol, including its session management and streaming capabilities. Simple `curl` commands are not sufficient as the server expects a stateful, persistent connection.

For guides on connecting specific clients, see the [MCP Server Clients](./MCP_CLIENTS.md) documentation.

Below is a list of available tools. The parameters for each tool can be introspected from the tool's function signature in the source code.

- **`list_tools`**: Retrieves a list of all available tools on the server.
- **`get_library_statistics`**: Retrieves high-level statistics about the music library.
- **`list_genres`**: Lists all genres in the library along with the number of tracks for each.
- **`list_playlists`**: Lists all existing playlists found in the beets configuration.
- **`create_playlist`**: Creates a new playlist file from a beets query.
- **`search_library`**: Searches the library using a beets query.
