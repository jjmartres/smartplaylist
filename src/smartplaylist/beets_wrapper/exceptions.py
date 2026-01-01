"""Custom exceptions for the beets wrapper.

These exceptions are raised for errors specific to the beets library interaction.
"""


class BeetsWrapperError(Exception):
    """Base exception for errors raised by the beets wrapper."""

    pass


class ImportError(BeetsWrapperError):
    """Raised when an error occurs during music import."""

    pass


class QueryError(BeetsWrapperError):
    """Raised when an error occurs during a library query."""

    pass


class UpdateError(BeetsWrapperError):
    """Raised when an error occurs during a library update."""

    pass
