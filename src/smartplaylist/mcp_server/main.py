"""Main MCP server application for SmartPlaylist.

This module defines the MCP tools for interacting with the beets library and
manages the server lifecycle.
"""

import logging
import os

from beets import config
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from smartplaylist.beets_wrapper import exceptions as beets_exceptions
from smartplaylist.beets_wrapper.library import Library as BeetsLibrary
from smartplaylist.logging_config import setup_logging
from smartplaylist.mcp_server import models
from smartplaylist.settings import Settings, get_settings

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP(name="smartplaylist-mcp-server")

TOOL_DEFINITIONS: list[dict[str, str]] = [
    {
        "name": "list_tools",
        "description": "Retrieves a list of all available tools on the server.",
    },
    {
        "name": "get_library_statistics",
        "description": "Retrieves high-level statistics about the music library.",
    },
    {
        "name": "list_genres",
        "description": "Lists all genres in the library along with the number of tracks for each.",
    },
    {
        "name": "list_playlists",
        "description": "Lists all existing playlists found in the beets configuration.",
    },
    {
        "name": "create_playlist",
        "description": "Creates a new playlist file from a beets query.",
    },
    {
        "name": "search_library",
        "description": "Searches the library using a beets query.",
    },
]


def _get_library(settings: Settings) -> BeetsLibrary:
    """Initializes and returns a BeetsLibrary instance.

    Args:
        settings: The application settings.

    Returns:
        A BeetsLibrary instance.

    Raises:
        beets_exceptions.BeetsWrapperError: If the library cannot be initialized.
    """
    config_path = str(settings.beets_config_path)
    try:
        return BeetsLibrary(config_path, settings)
    except beets_exceptions.BeetsWrapperError as e:
        logger.error(f"Error accessing beets library with config at {config_path}: {e}")
        raise


@mcp.tool()
def list_tools() -> list[models.ToolInfo]:
    """Retrieves a list of all available tools on the server.

    Returns:
        A list of ToolInfo objects, each describing a tool.
    """
    return [models.ToolInfo(**tool) for tool in TOOL_DEFINITIONS]


@mcp.tool()
def get_library_statistics() -> models.LibraryStatistics:
    """Retrieves high-level statistics about the music library.

    Returns:
        An object containing library statistics.
    """
    settings = get_settings()
    library = _get_library(settings)
    stats = library.get_statistics()
    genres = library.list_genres()
    return models.LibraryStatistics(
        total_tracks=stats.total_tracks,
        total_albums=stats.total_albums,
        total_artists=stats.total_artists,
        total_genres=len(genres),
    )


@mcp.tool()
def list_genres() -> models.ListGenresResponse:
    """Lists all genres in the library along with the number of tracks for each.

    Returns:
        A response object containing a list of genres.
    """
    settings = get_settings()
    library = _get_library(settings)
    genres = library.list_genres()
    return models.ListGenresResponse(
        genres=[models.GenreInfo(name=g.name, track_count=g.count) for g in genres]
    )


@mcp.tool()
def list_playlists() -> models.ListPlaylistsResponse:
    """Lists all existing playlists found in the beets configuration.

    Returns:
        A response object containing a list of playlist names.
    """
    settings = get_settings()
    library = _get_library(settings)
    playlists = library.list_playlists(settings.playlist_extension)
    return models.ListPlaylistsResponse(playlists=[p.name for p in playlists])


@mcp.tool()
def create_playlist(playlist_name: str, query: str) -> models.CreatePlaylistResponse:
    """Creates a new playlist file from a beets query.

    Args:
        playlist_name: The name of the playlist to create.
        query: The beets query to use to generate the playlist.

    Returns:
        A response object with the status of the operation and the path to the
        created playlist.
    """
    settings = get_settings()
    library = _get_library(settings)
    try:
        playlist_dir = config["smartplaylist"]["playlist_dir"].get(str)
        playlist_path = os.path.join(
            playlist_dir, f"{playlist_name}.{settings.playlist_extension}"
        )
        library.create_playlist(query, playlist_path)
        track_count = len(library.items(query))
        return models.CreatePlaylistResponse(
            status="Playlist created successfully",
            playlist_path=playlist_path,
            track_count=track_count,
        )
    except beets_exceptions.BeetsWrapperError as e:
        logger.error(f"Error creating playlist: {e}")
        raise


@mcp.tool()
def search_library(query: str) -> models.SearchLibraryResponse:
    """Searches the library using a beets query.

    Note:
        The natural language to beets query translation has been removed as part
        of the refactoring. The client is now expected to provide a valid beets
        query.

    Args:
        query: The beets query to execute.

    Returns:
        A response object containing a list of matching tracks.
    """
    settings = get_settings()
    library = _get_library(settings)
    try:
        beets_tracks = library.items(query)
        tracks = [
            models.Track(
                id=track.id,
                title=track.title,
                artist=track.artist,
                album=track.album,
                genre=track.genre,
                year=track.year,
                path=track.path.decode("utf-8"),
            )
            for track in beets_tracks
        ]
        return models.SearchLibraryResponse(tracks=tracks, beets_query_used=query)
    except beets_exceptions.BeetsWrapperError as e:
        logger.error(f"Error searching library: {e}")
        raise


def main(settings: Settings):
    """Runs the SmartPlaylist MCP Server with the given settings.

    Args:
        settings: The application settings.
    """
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger.info(f"Starting SmartPlaylist MCP Server on port {settings.mcp_server_port}")
    logger.info(
        f"Endpoint will be: http://{settings.mcp_server_host}:{settings.mcp_server_port}/mcp"
    )
    logger.info(f"Allowed hosts: {settings.mcp_allowed_hosts}")

    mcp.settings.host = settings.mcp_server_host
    mcp.settings.port = settings.mcp_server_port

    allowed_hosts = settings.mcp_allowed_hosts or [
        "127.0.0.1:*",
        "localhost:*",
        "[::1]:*",
    ]

    mcp.settings.transport_security = TransportSecuritySettings(
        allowed_hosts=allowed_hosts
    )

    mcp.run(transport="streamable-http")
