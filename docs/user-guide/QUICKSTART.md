# Quickstart Guide

This guide provides a quick overview of how to get started with the `smartplaylist` command-line tool and server.

## Configuration

SmartPlaylist is configured through environment variables or a `.env` file in the project root. Environment variables always take precedence.

### Available Environment Variables

| Variable | Alias | Description | Default |
|---|---|---|---|
| `SMARTPLAYLIST_CONFIG_PATH` | - | Path to the beets configuration file. | `~/.config/smartplaylist/config.yaml` |
| `SMARTPLAYLIST_LOG_LEVEL` | - | The logging level for the application. | `INFO` |
| `SMARTPLAYLIST_MCP_SERVER_HOST` | `MCP_HOST` | The host for the MCP server. | `127.0.0.1` |
| `SMARTPLAYLIST_MCP_SERVER_PORT` | `MCP_PORT` | The port for the MCP server. | `8000` |
| `SMARTPLAYLIST_MCP_ALLOWED_HOSTS` | `MCP_ALLOWED_HOSTS` | Comma-separated list of trusted hostnames. | `None` |
| `SMARTPLAYLIST_PLAYLIST_EXTENSION`| - | File extension for generated playlists. | `m3u8` |
| `SMARTPLAYLIST_MUSIC_LIBRARY_PATH_FROM` | - | Source path prefix to be replaced in playlists. | `None` |
| `SMARTPLAYLIST_MUSIC_LIBRARY_PATH_TO` | - | Target path prefix to substitute in playlists. | `None` |

### Example `.env` file

```dotenv
# .env

# The path to the beets configuration file.
SMARTPLAYLIST_CONFIG_PATH="/Users/yourname/.config/smartplaylist/config.yaml"

# The logging level for the application.
SMARTPLAYLIST_LOG_LEVEL="DEBUG"

# The host and port for the MCP server.
SMARTPLAYLIST_MCP_SERVER_HOST="0.0.0.0"
SMARTPLAYLIST_MCP_SERVER_PORT=9000

# Optional: Rewrite playlist file paths for portability.
# SMARTPLAYLIST_MUSIC_LIBRARY_PATH_FROM="/path/on/this/machine"
# SMARTPLAYLIST_MUSIC_LIBRARY_PATH_TO="/path/on/target/device"
```

## Installation

To get started, clone the repository and use `make setup` to create a virtual environment and install all dependencies:

```bash
git clone https://github.com/jjmartres/smartplaylist.git
cd smartplaylist
make setup
```

## CLI Commands

### Global Options

- `--version`: Show the application version and exit.

### `sync`

The `sync` command initializes a new beets database or updates an existing one.

**Usage:**
```bash
smartplaylist sync [OPTIONS] MUSIC_LIBRARY_PATH
```

**Example:**
```bash
smartplaylist sync /path/to/my/music
```

On the first run, this will create a `.smartplaylist` directory inside your music library path with the following files:
- `smartplaylist.db`: The beets database.
- `config.yaml`: The beets configuration file.

On subsequent runs, it will update the existing database.

**Important**: After the first run, you should update your `.env` file or set the `SMARTPLAYLIST_CONFIG_PATH` environment variable to point to the newly created `config.yaml`.

---

### `serve`

The `serve` command starts the MCP server.

**Usage:**
```bash
smartplaylist serve [OPTIONS]
```

**Example:**
```bash
# Start the server
smartplaylist serve

```

The server will start using the host and port defined in your configuration.

## Troubleshooting

### Command not found

If you get an error like `command not found: smartplaylist`, ensure you have activated the virtual environment created by `make setup`:

```bash
source .venv/bin/activate
```

### Invalid Host Header

If you see a `WARNING:mcp.server.transport_security:Invalid Host header` message in the server logs, it means you are trying to access the server from a hostname that is not explicitly trusted.

This is a security feature. To fix this, you can set the `SMARTPLAYLIST_MCP_ALLOWED_HOSTS` environment variable to a comma-separated list of hostnames you want to allow.

For example, in your `.env` file:

```dotenv
# Allow connections from 'localhost' and 'personal.local'
SMARTPLAYLIST_MCP_ALLOWED_HOSTS="localhost,personal.local"
```

## Running with Docker

The easiest way to run `smartplaylist` is with Docker.

### Building the Image

```bash
docker build -t smartplaylist:latest .
```

### Running the Container

```bash
docker run -d --name smartplaylist -p 8000:8000 \
  -v /path/to/your/music:/app/data \
  smartplaylist:latest
```

This will start the container, sync your music library, and start the MCP server on port 8000.

### Running with Docker Compose

A `docker-compose.yml` file is also provided for a more streamlined experience.

1.  **Edit `docker-compose.yml`**: Change the volume mapping to point to your music library:

    ```yaml
    volumes:
      - /path/to/your/music:/app/data
    ```

2.  **Run Docker Compose**:

    ```bash
    docker-compose up -d --build
    ```

This will build the image, create a container, and start the `smartplaylist` server. The `SMARTPLAYLIST_PLAYLIST_EXTENSION` is set to `playlist.m3u8` by default in the `docker-compose.yml` file.
