"""Unit tests for the MCP server tools."""

from unittest.mock import MagicMock, patch

import pytest

from smartplaylist.beets_wrapper import models as beets_models
from smartplaylist.mcp_server import main
from smartplaylist.settings import get_settings


@pytest.fixture(autouse=True)
def clear_get_settings_cache():
    get_settings.cache_clear()


class TestMCPServerTools:
    def test_list_tools(self):
        """Tests that the list_tools tool returns the expected list of tools."""
        tools = main.list_tools()
        tool_names = [tool.name for tool in tools]

        assert len(tools) == len(main.TOOL_DEFINITIONS)
        assert main.TOOL_DEFINITIONS[0]["name"] in tool_names

    @patch("smartplaylist.mcp_server.main.BeetsLibrary")
    def test_get_library_statistics(self, mock_beets_library, monkeypatch):
        """Tests that the get_library_statistics tool returns the expected statistics."""
        monkeypatch.setenv("SMARTPLAYLIST_CONFIG_PATH", "/dummy/path")

        mock_instance = mock_beets_library.return_value
        mock_instance.get_statistics.return_value = beets_models.Statistics(
            total_tracks=100, total_albums=10, total_artists=20, total_size=12345
        )
        mock_instance.list_genres.return_value = [beets_models.Genre("Rock", 10)]

        stats = main.get_library_statistics()

        assert stats.total_tracks == 100
        assert stats.total_albums == 10
        assert stats.total_artists == 20
        assert stats.total_genres == 1

    @patch("smartplaylist.mcp_server.main.BeetsLibrary")
    def test_list_genres(self, mock_beets_library, monkeypatch):
        """Tests that the list_genres tool returns the expected list of genres."""
        monkeypatch.setenv("SMARTPLAYLIST_CONFIG_PATH", "/dummy/path")
        mock_instance = mock_beets_library.return_value
        mock_instance.list_genres.return_value = [
            beets_models.Genre("Rock", 10),
            beets_models.Genre("Pop", 20),
        ]

        response = main.list_genres()

        assert len(response.genres) == 2
        assert response.genres[0].name == "Rock"
        assert response.genres[0].track_count == 10

    @patch("smartplaylist.mcp_server.main.BeetsLibrary")
    def test_list_playlists(self, mock_beets_library, monkeypatch):
        """Tests that the list_playlists tool returns the expected list of playlists."""
        monkeypatch.setenv("SMARTPLAYLIST_CONFIG_PATH", "/dummy/path")
        mock_instance = mock_beets_library.return_value
        mock_instance.list_playlists.return_value = [
            beets_models.Playlist("My Playlist"),
            beets_models.Playlist("Another Playlist"),
        ]

        response = main.list_playlists()

        assert len(response.playlists) == 2
        assert response.playlists[0] == "My Playlist"

    @patch("smartplaylist.mcp_server.main.config")
    @patch("smartplaylist.mcp_server.main.BeetsLibrary")
    def test_create_playlist(self, mock_beets_library, mock_config, monkeypatch):
        """Tests that the create_playlist tool returns the expected response."""
        monkeypatch.setenv("SMARTPLAYLIST_CONFIG_PATH", "/dummy/path")
        mock_config.__getitem__.return_value = {
            "playlist_dir": MagicMock(get=lambda T: "/playlists")
        }

        mock_instance = mock_beets_library.return_value
        mock_instance.items.return_value = [MagicMock()] * 10  # 10 tracks

        response = main.create_playlist("My Playlist", "artist:Test Artist")

        mock_instance.create_playlist.assert_called_with(
            "artist:Test Artist", "/playlists/My Playlist.m3u8"
        )
        assert response.status == "Playlist created successfully"
        assert response.playlist_path == "/playlists/My Playlist.m3u8"
        assert response.track_count == 10

    @patch("smartplaylist.mcp_server.main.BeetsLibrary")
    def test_search_library(self, mock_beets_library, monkeypatch):
        """Tests that the search_library tool returns the expected response."""
        monkeypatch.setenv("SMARTPLAYLIST_CONFIG_PATH", "/dummy/path")

        mock_instance = mock_beets_library.return_value
        mock_item = MagicMock()
        mock_item.id = 1
        mock_item.title = "Track 1"
        mock_item.artist = "Artist 1"
        mock_item.album = "Album 1"
        mock_item.genre = "Rock"
        mock_item.year = 2023
        mock_item.path = b"/path/1"

        mock_instance.items.return_value = [mock_item]

        response = main.search_library("genre:rock")

        assert len(response.tracks) == 1
        assert response.tracks[0].title == "Track 1"
        assert response.beets_query_used == "genre:rock"
