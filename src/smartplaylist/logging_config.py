"""Logging configuration for the SmartPlaylist application."""

import logging
from rich.logging import RichHandler


def setup_logging():
    """Configures logging for the application to use rich for pretty output."""
    # Configure the root logger for application logs
    logging.basicConfig(
        level="INFO", handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
    )

    # Intercept uvicorn's loggers to use RichHandler as well
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.handlers = [RichHandler(rich_tracebacks=True, show_path=False)]
    uvicorn_error_logger.propagate = False

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = [
        RichHandler(rich_tracebacks=True, show_path=False)
    ]
    uvicorn_access_logger.propagate = False
