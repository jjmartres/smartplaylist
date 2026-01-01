"""Data models for the beets wrapper.

This module defines the data structures used to represent beets library objects
such as items, albums, and statistics in a Pythonic way.
"""

import dataclasses
from typing import List


@dataclasses.dataclass
class Statistics:
    """Represents library statistics.

    Attributes:
        total_tracks: The total number of tracks in the library.
        total_albums: The total number of albums in the library.
        total_artists: The total number of unique artists in the library.
        total_size: The total size of the library in bytes.
    """

    total_tracks: int
    total_albums: int
    total_artists: int
    total_size: int


@dataclasses.dataclass
class Genre:
    """Represents a genre with its track count.

    Attributes:
        name: The name of the genre.
        count: The number of tracks in this genre.
    """

    name: str
    count: int


@dataclasses.dataclass
class Playlist:
    """Represents a playlist file.

    Attributes:
        name: The name of the playlist file.
    """

    name: str


class BeetsModel:
    """Base class for wrapping beets `Item` and `Album` objects.

    This class provides attribute-style access to the underlying beets data,
    making it easier to work with.

    Attributes:
        _beets_item: The underlying beets object.
    """

    def __init__(self, beets_item):
        """Initializes the BeetsModel.

        Args:
            beets_item: The beets `Item` or `Album` object to wrap.
        """
        super().__setattr__("_beets_item", beets_item)

    def __getattr__(self, name):
        return self._beets_item.get(name)

    def __setattr__(self, name, value):
        self._beets_item[name] = value

    def save(self):
        """Saves the changes to the underlying beets item."""
        self._beets_item.store()


class Item(BeetsModel):
    """Represents a single track (item) in the beets library."""

    pass


class Album(BeetsModel):
    """Represents an album in the beets library."""

    def items(self) -> List[Item]:
        """Returns a list of items (tracks) in the album.

        Returns:
            A list of Item objects belonging to the album.
        """
        return [Item(item) for item in self._beets_item.items()]
