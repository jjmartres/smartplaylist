"""Beets library wrapper for SmartPlaylist.

This module provides a `Library` class that acts as a high-level API for
interacting with a beets music library. It abstracts away the direct use of the
beets internal API and CLI commands.
"""

import os
import shutil
import subprocess
from typing import Dict, Optional

from beets import config, library  # type: ignore

from smartplaylist.settings import Settings
from . import exceptions, models


class Library:
    """A wrapper for interacting with a beets music library.

    This class provides methods for importing music, updating the library,
    querying items and albums, and creating playlists.

    Attributes:
        config_path: Path to the beets configuration file.
        settings: The application settings object.
        lib: An instance of the beets `Library` class.
    """

    def __init__(self, config_path: str, settings: Settings):
        """Initializes the Library wrapper.

        Args:
            config_path: Path to the beets configuration file.
            settings: The application settings object.

        Raises:
            exceptions.BeetsWrapperError: If the library cannot be initialized.
        """
        self.config_path = config_path
        self.settings = settings
        try:
            config.set_file(config_path)
            self.lib = library.Library(config["library"].as_filename())
        except Exception as e:
            raise exceptions.BeetsWrapperError(
                f"Failed to initialize beets library: {e}"
            ) from e

    def import_dir(self, path: str):
        """Imports music from a directory into the beets library.

        Args:
            path: Path to the directory to import.

        Raises:
            exceptions.ImportError: If the import fails.
        """
        beet_executable = shutil.which("beet") or ".venv/bin/beet"
        try:
            subprocess.run(
                [
                    beet_executable,
                    "-c",
                    self.config_path,
                    "import",
                    "-q",
                    path,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise exceptions.ImportError(
                f"Failed to import music from {path}: {e}"
            ) from e

    def update_library(self):
        """Updates the beets library by scanning for new and changed files.

        Raises:
            exceptions.UpdateError: If the update fails.
        """
        beet_executable = shutil.which("beet") or ".venv/bin/beet"
        try:
            subprocess.run(
                [
                    beet_executable,
                    "-c",
                    self.config_path,
                    "update",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            raise exceptions.UpdateError(
                f"Failed to update the library. stdout: {e.stdout}, stderr: {e.stderr}"
            ) from e

    def items(self, query: Optional[str] = None) -> list[models.Item]:
        """Fetches a list of items from the library matching a query.

        Args:
            query: The beets query to execute.

        Returns:
            A list of items matching the query.

        Raises:
            exceptions.QueryError: If the query fails.
        """
        try:
            return [models.Item(item) for item in self.lib.items(query)]
        except Exception as e:
            raise exceptions.QueryError(
                f"Failed to query items with '{query}': {e}"
            ) from e

    def albums(self, query: Optional[str] = None) -> list[models.Album]:
        """Fetches a list of albums from the library matching a query.

        Args:
            query: The beets query to execute.

        Returns:
            A list of albums matching the query.

        Raises:
            exceptions.QueryError: If the query fails.
        """
        try:
            return [models.Album(album) for album in self.lib.albums(query)]
        except Exception as e:
            raise exceptions.QueryError(
                f"Failed to query albums with '{query}': {e}"
            ) from e

    def create_playlist(self, query: str, path: str):
        """Creates a playlist file from a query, with optional path rewriting.

        Args:
            query: The beets query to use to generate the playlist.
            path: The path to the playlist file.

        Raises:
            exceptions.BeetsWrapperError: If the playlist creation fails.
        """
        try:
            items = self.lib.items(query)
            rewrite_from = self.settings.music_library_path_from
            rewrite_to = self.settings.music_library_path_to
            with open(path, "w") as f:
                for item in items:
                    item_path = item.path.decode("utf-8")
                    if rewrite_from and rewrite_to:
                        item_path = item_path.replace(
                            str(rewrite_from), str(rewrite_to)
                        )
                    f.write(f"{item_path}\n")
        except Exception as e:
            raise exceptions.BeetsWrapperError(f"Failed to create playlist: {e}") from e

    def get_statistics(self) -> models.Statistics:
        """Returns high-level statistics for the library.

        Returns:
            An object containing library statistics.

        Raises:
            exceptions.BeetsWrapperError: If fetching statistics fails.
        """
        try:
            total_tracks = len(self.lib.items())
            total_albums = len(self.lib.albums())
            total_artists = len(set(i.artist for i in self.lib.items()))
            total_size = sum(i.filesize for i in self.lib.items())
            return models.Statistics(
                total_tracks=total_tracks,
                total_albums=total_albums,
                total_artists=total_artists,
                total_size=total_size,
            )
        except Exception as e:
            raise exceptions.BeetsWrapperError(f"Failed to get statistics: {e}") from e

    def list_genres(self) -> list[models.Genre]:
        """Returns a list of all genres in the library with their track counts.

        Returns:
            A list of Genre objects.

        Raises:
            exceptions.BeetsWrapperError: If listing genres fails.
        """
        try:
            all_items = self.lib.items()
            genre_counts: Dict[str, int] = {}
            for item in all_items:
                genre = item.get("genre")
                if genre:
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
            return [
                models.Genre(name=genre, count=count)
                for genre, count in genre_counts.items()
            ]
        except Exception as e:
            raise exceptions.BeetsWrapperError(f"Failed to list genres: {e}") from e

    @staticmethod
    def db_exists(config_path: str) -> bool:
        """Checks if the beets database file exists.

        Args:
            config_path: Path to the beets configuration file.

        Returns:
            True if the database exists, False otherwise.

        Raises:
            exceptions.BeetsWrapperError: If the check fails due to an unexpected error.
        """
        if not os.path.exists(config_path):
            return False
        try:
            config.set_file(config_path)
            db_path = config["library"].as_filename()
            return os.path.exists(db_path)
        except PermissionError:
            raise
        except Exception as e:
            raise exceptions.BeetsWrapperError(
                f"Failed to check for beets database: {e}"
            ) from e

    def list_playlists(self, playlist_extension: str) -> list[models.Playlist]:
        """Returns a list of all found playlist files.

        Args:
            playlist_extension: The file extension for playlists (e.g., "m3u8").

        Returns:
            A list of Playlist objects.

        Raises:
            exceptions.BeetsWrapperError: If listing playlists fails.
        """
        try:
            playlist_dir = config["smartplaylist"]["playlist_dir"].get(str)
            if not os.path.isdir(playlist_dir):
                return []

            playlists = []
            for filename in os.listdir(playlist_dir):
                if filename.endswith(playlist_extension):
                    playlists.append(models.Playlist(name=filename))
            return playlists
        except Exception as e:
            raise exceptions.BeetsWrapperError(f"Failed to list playlists: {e}") from e
