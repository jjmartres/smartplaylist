"""Pydantic models for the MCP server API.

This module defines the data structures for tool inputs and outputs, ensuring
that all communication with the MCP server is type-safe.
"""

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class Track(BaseModel):
    """Represents a track in the music library.

    Attributes:
        id: The unique identifier for the track.
        title: The title of the track.
        artist: The artist of the track.
        album: The album the track belongs to.
        genre: The genre of the track.
        year: The release year of the track.
        path: The file path of the track.
    """

    id: int
    title: str
    artist: str
    album: str
    genre: str
    year: int
    path: str


class ToolInfo(BaseModel):
    """Provides information about an available tool.

    Attributes:
        name: The name of the tool.
        description: A brief summary of what the tool does.
    """

    name: str = Field(
        ..., description="The name of the tool (e.g., `get_library_statistics`)."
    )
    description: str = Field(..., description="A brief summary of what the tool does.")


class LibraryStatistics(BaseModel):
    """Represents statistics about the music library.

    Attributes:
        total_tracks: The total number of tracks.
        total_albums: The total number of albums.
        total_artists: The total number of unique artists.
        total_genres: The total number of unique genres.
    """

    total_tracks: int = Field(
        ..., description="The total number of tracks in the library."
    )
    total_albums: int = Field(
        ..., description="The total number of albums in the library."
    )
    total_artists: int = Field(
        ..., description="The total number of unique artists in the library."
    )
    total_genres: int = Field(
        ..., description="The total number of unique genres in the library."
    )


class GenreInfo(BaseModel):
    """Represents information about a single genre.

    Attributes:
        name: The name of the genre.
        track_count: The number of tracks in the genre.
    """

    name: str = Field(..., description="The name of the genre.")
    track_count: int = Field(..., description="The number of tracks in the genre.")


class ListGenresResponse(BaseModel):
    """Response model for the `list_genres` tool.

    Attributes:
        genres: A list of genres in the library.
    """

    genres: List[GenreInfo] = Field(..., description="A list of genres in the library.")


class ListPlaylistsResponse(BaseModel):
    """Response model for the `list_playlists` tool.

    Attributes:
        playlists: A list of playlist names.
    """

    playlists: List[str] = Field(..., description="A list of playlist names.")


class CreatePlaylistResponse(BaseModel):
    """Response model for the `create_playlist` tool.

    Attributes:
        status: The status of the playlist creation.
        playlist_path: The path to the created playlist file.
        track_count: The number of tracks in the created playlist.
    """

    status: str = Field(..., description="The status of the playlist creation.")
    playlist_path: str = Field(
        ..., description="The path to the created playlist file."
    )
    track_count: int = Field(
        ..., description="The number of tracks in the created playlist."
    )


class SearchLibraryResponse(BaseModel):
    """Response model for the `search_library` tool.

    Attributes:
        tracks: A list of tracks matching the search query.
        beets_query_used: The underlying beets query that was used for the search.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    tracks: List[Track] = Field(
        ..., description="A list of tracks matching the search query."
    )
    beets_query_used: str = Field(
        ..., description="The underlying beets query that was used for the asearch."
    )
