#!/bin/sh

set -e

export MUSIC_DIR="${MUSIC_DIR:-/app/data}"
export SMARTPLAYLIST_CONFIG_PATH="${SMARTPLAYLIST_CONFIG_PATH:-/app/data/.smartplaylist/config.yaml}"
export SMARTPLAYLIST_LOG_LEVEL="${SMARTPLAYLIST_LOG_LEVEL:-INFO}"
export SMARTPLAYLIST_MCP_SERVER_HOST="${SMARTPLAYLIST_MCP_SERVER_HOST:-0.0.0.0}"
export SMARTPLAYLIST_MCP_SERVER_PORT="${SMARTPLAYLIST_MCP_SERVER_PORT:-8000}"
export SMARTPLAYLIST_MCP_ALLOWED_HOSTS="${SMARTPLAYLIST_MCP_ALLOWED_HOSTS:-'127.0.0.1,localhost'}"

if [ ! -d "$MUSIC_DIR" ]; then
	echo "Error: Music directory '$MUSIC_DIR' not found." >&2
	echo "Please mount your music library to the '$MUSIC_DIR' volume." >&2
	exit 1
fi

echo "Running smartplaylist sync on '$MUSIC_DIR'..."
smartplaylist sync "$MUSIC_DIR"

echo "Starting MCP server..."
smartplaylist serve
