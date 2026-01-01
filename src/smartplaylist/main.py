"""Main entry point for the smartplaylist application."""

import logging

from smartplaylist.cli.main import app

logging.basicConfig(level=logging.INFO)


def main():
    """Runs the CLI application."""
    app()


if __name__ == "__main__":
    main()
