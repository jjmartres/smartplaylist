"""Tests for the beets wrapper models."""

import unittest.mock

from smartplaylist.beets_wrapper import models


def test_item_save():
    """Test saving an item."""
    mock_beets_item = unittest.mock.MagicMock()
    item = models.Item(mock_beets_item)
    item.genre = "Rock"
    item.save()

    mock_beets_item.store.assert_called_once()
    mock_beets_item.__setitem__.assert_called_with("genre", "Rock")
