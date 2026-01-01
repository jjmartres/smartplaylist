"""Tests for the beets wrapper library."""

import subprocess
import unittest.mock
from pathlib import Path

import pytest
import yaml

from smartplaylist.beets_wrapper import exceptions, library
from smartplaylist.settings import Settings


@pytest.fixture
def mock_settings(monkeypatch):
    """Fixture to mock settings."""
    monkeypatch.setenv("SMARTPLAYLIST_CONFIG_PATH", "/dummy/path")
    return Settings()


@pytest.fixture
def mock_beets_config(mocker):
    """Fixture to mock beets config."""
    mock_config = mocker.patch("smartplaylist.beets_wrapper.library.config")
    mocker.patch("smartplaylist.beets_wrapper.library.library")
    return mock_config


def test_library_init_success(mock_beets_config, mock_settings):
    """Test successful library initialization."""
    lib = library.Library(config_path="/fake/config.yaml", settings=mock_settings)
    assert lib.lib is not None


def test_library_init_failure(mock_beets_config, mock_settings):
    """Test library initialization failure."""
    mock_beets_config.set_file.side_effect = Exception("Test error")
    with pytest.raises(exceptions.BeetsWrapperError):
        library.Library(config_path="/fake/config.yaml", settings=mock_settings)


def test_import_dir_success(tmp_path: Path, mock_settings):
    """Test successful directory import."""
    db_path = tmp_path / "test.db"
    config_path = tmp_path / "config.yaml"
    music_path = tmp_path / "music"
    music_path.mkdir()
    (music_path / "track.mp3").touch()

    beets_config = {
        "library": str(db_path.resolve()),
        "directory": str(music_path.resolve()),
        "plugins": [],
    }
    with open(config_path, "w") as f:
        yaml.dump(beets_config, f)

    db_path.touch()
    lib = library.Library(str(config_path.resolve()), settings=mock_settings)
    lib.import_dir(str(music_path.resolve()))


def test_import_dir_failure(tmp_path: Path, mock_settings):
    """Test directory import failure."""
    db_path = tmp_path / "test.db"
    config_path = tmp_path / "config.yaml"
    music_path = tmp_path / "music"

    beets_config = {
        "library": str(db_path.resolve()),
        "directory": str(music_path.resolve()),
        "plugins": [],
    }
    with open(config_path, "w") as f:
        yaml.dump(beets_config, f)

    db_path.touch()
    lib = library.Library(str(config_path.resolve()), settings=mock_settings)
    with pytest.raises(exceptions.ImportError):
        lib.import_dir(str(music_path.resolve()))


def test_items_success(mock_beets_config, mock_settings):
    """Test successful items query."""
    lib = library.Library(config_path="/fake/config.yaml", settings=mock_settings)
    lib.lib.items.return_value = [unittest.mock.Mock()]  # type: ignore
    items = lib.items(query="artist:Test")
    assert len(items) == 1
    lib.lib.items.assert_called_once_with("artist:Test")  # type: ignore


def test_items_failure(mock_beets_config, mock_settings):
    """Test items query failure."""
    lib = library.Library(config_path="/fake/config.yaml", settings=mock_settings)
    lib.lib.items.side_effect = Exception("Test error")  # type: ignore
    with pytest.raises(exceptions.QueryError):
        lib.items(query="artist:Test")


def test_albums_success(mock_beets_config, mock_settings):
    """Test successful albums query."""
    lib = library.Library(config_path="/fake/config.yaml", settings=mock_settings)
    lib.lib.albums.return_value = [unittest.mock.Mock()]  # type: ignore
    albums = lib.albums(query="year:2023")
    assert len(albums) == 1
    lib.lib.albums.assert_called_once_with("year:2023")  # type: ignore


def test_albums_failure(mock_beets_config, mock_settings):
    """Test albums query failure."""
    lib = library.Library(config_path="/fake/config.yaml", settings=mock_settings)
    lib.lib.albums.side_effect = Exception("Test error")  # type: ignore
    with pytest.raises(exceptions.QueryError):
        lib.albums(query="year:2023")


@unittest.mock.patch("builtins.open", new_callable=unittest.mock.mock_open)
def test_create_playlist_success(mock_open, mock_beets_config, mock_settings):
    """Test successful playlist creation."""
    lib = library.Library(config_path="/fake/config.yaml", settings=mock_settings)
    mock_item = unittest.mock.Mock()
    mock_item.path = b"/path/to/music.mp3"
    lib.lib.items.return_value = [mock_item]  # type: ignore

    lib.create_playlist(query="genre:Rock", path="/fake/playlist.m3u")

    mock_open.assert_called_once_with("/fake/playlist.m3u", "w")
    mock_open().write.assert_called_once_with("/path/to/music.mp3\n")


@unittest.mock.patch("builtins.open", new_callable=unittest.mock.mock_open)
def test_create_playlist_with_rewrite(mock_open, mock_beets_config, monkeypatch):
    """Test successful playlist creation with path rewriting."""
    monkeypatch.setenv("SMARTPLAYLIST_MUSIC_LIBRARY_PATH_FROM", "/path/to")
    monkeypatch.setenv("SMARTPLAYLIST_MUSIC_LIBRARY_PATH_TO", "/new/path")
    settings = Settings()
    lib = library.Library(config_path="/fake/config.yaml", settings=settings)
    mock_item = unittest.mock.Mock()
    mock_item.path = b"/path/to/music.mp3"
    lib.lib.items.return_value = [mock_item]  # type: ignore

    lib.create_playlist(query="genre:Rock", path="/fake/playlist.m3u")

    mock_open.assert_called_once_with("/fake/playlist.m3u", "w")
    mock_open().write.assert_called_once_with("/new/path/music.mp3\n")


def test_get_statistics_success(mock_beets_config, mock_settings):
    """Test successful statistics retrieval."""
    lib = library.Library(config_path="/fake/config.yaml", settings=mock_settings)
    mock_item1 = unittest.mock.Mock()
    mock_item1.artist = "Artist1"
    mock_item1.filesize = 1000
    mock_item2 = unittest.mock.Mock()
    mock_item2.artist = "Artist2"
    mock_item2.filesize = 2000

    lib.lib.items.return_value = [mock_item1, mock_item2]  # type: ignore
    lib.lib.albums.return_value = [unittest.mock.Mock()]  # type: ignore

    stats = lib.get_statistics()

    assert stats.total_tracks == 2
    assert stats.total_albums == 1
    assert stats.total_artists == 2
    assert stats.total_size == 3000


def test_list_genres_success(mock_beets_config, mock_settings):
    """Test successful genre listing."""
    lib = library.Library(config_path="/fake/config.yaml", settings=mock_settings)
    mock_item1 = unittest.mock.Mock()
    mock_item1.get.return_value = "Rock"
    mock_item2 = unittest.mock.Mock()
    mock_item2.get.return_value = "Pop"
    mock_item3 = unittest.mock.Mock()
    mock_item3.get.return_value = "Rock"
    lib.lib.items.return_value = [mock_item1, mock_item2, mock_item3]  # type: ignore

    genres = lib.list_genres()

    assert len(genres) == 2

    # The order is not guaranteed, so we need to sort the genres by name
    sorted_genres = sorted(genres, key=lambda x: x.name)

    assert sorted_genres[0].name == "Pop"
    assert sorted_genres[0].count == 1
    assert sorted_genres[1].name == "Rock"
    assert sorted_genres[1].count == 2


@unittest.mock.patch("smartplaylist.beets_wrapper.library.os")
def test_list_playlists_success(mock_os, mock_beets_config, mock_settings):
    """Test successful playlist listing."""
    mock_beets_config["smartplaylist"][
        "playlist_dir"
    ].get.return_value = "/fake/playlists"
    mock_os.path.isdir.return_value = True
    mock_os.listdir.return_value = ["Rock Classics.m3u8", "Pop Hits.m3u8"]
    lib = library.Library(config_path="/fake/config.yaml", settings=mock_settings)

    playlists = lib.list_playlists(playlist_extension=".m3u8")

    assert len(playlists) == 2
    assert playlists[0].name == "Rock Classics.m3u8"


def test_update_library_success(mocker, tmp_path: Path, mock_settings):
    """Test successful library update."""
    db_path = tmp_path / "test.db"
    config_path = tmp_path / "config.yaml"
    music_path = tmp_path / "music"
    music_path.mkdir()

    beets_config = {
        "library": str(db_path.resolve()),
        "directory": str(music_path.resolve()),
        "plugins": [],
    }
    with open(config_path, "w") as f:
        yaml.dump(beets_config, f)

    db_path.touch()
    lib = library.Library(str(config_path.resolve()), settings=mock_settings)
    mock_run = mocker.patch("subprocess.run")
    lib.update_library()
    mock_run.assert_called_once()


def test_update_library_failure(mocker, tmp_path: Path, mock_settings):
    """Test library update failure."""
    db_path = tmp_path / "test.db"
    config_path = tmp_path / "config.yaml"
    music_path = tmp_path / "music"
    music_path.mkdir()

    beets_config = {
        "library": str(db_path.resolve()),
        "directory": str(music_path.resolve()),
        "plugins": [],
    }
    with open(config_path, "w") as f:
        yaml.dump(beets_config, f)

    db_path.touch()
    lib = library.Library(str(config_path.resolve()), settings=mock_settings)
    mock_run = mocker.patch("subprocess.run")
    mock_run.side_effect = subprocess.CalledProcessError(1, "beet", "stdout", "stderr")
    with pytest.raises(exceptions.UpdateError):
        lib.update_library()
