"""Command-line interface for smartplaylist."""

import typer
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from smartplaylist.beets_wrapper import library, exceptions
from smartplaylist.settings import get_settings
from smartplaylist.mcp_server.main import main as mcp_server_main
import importlib.metadata


app = typer.Typer()

__version__ = importlib.metadata.version("smartplaylist")


def version_callback(value: bool):
    """Prints the application version and exits.

    Args:
        value: If True, prints the version and exits.
    """
    if value:
        typer.echo(f"SmartPlaylist Version: {__version__}")
        raise typer.Exit()


@app.command()
def sync(
    music_library_path: Path = typer.Argument(
        ...,
        help="The path to your music library directory.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
    force_init: bool = typer.Option(
        False,
        "--force-init",
        help="Force re-initialization, deleting the existing database.",
    ),
):
    """Initializes or updates the smartplaylist database.

    This command intelligently handles the database by either initializing it
    (if it doesn't exist or --force-init is used) or updating it.

    Args:
        music_library_path: The path to the user's music library.
        force_init: If True, deletes and re-initializes the database.
    """
    settings = get_settings()
    try:
        data_dir = music_library_path / ".smartplaylist"
        data_dir.mkdir(exist_ok=True)

        db_path = data_dir / "smartplaylist.db"
        config_path = data_dir / "config.yaml"

        should_init = force_init or not library.Library.db_exists(str(config_path))

        if should_init:
            if force_init:
                typer.echo("Forcing re-initialization of the database...")
            else:
                typer.echo("No database found. Initializing new database...")
            if db_path.exists():
                db_path.unlink()

            env = Environment(loader=FileSystemLoader(Path(__file__).parent.resolve()))
            template = env.get_template("config.yaml.j2")

            playlist_dir = data_dir / "playlists"
            playlist_dir.mkdir(exist_ok=True)
            rendered_config = template.render(
                library=str(db_path.resolve()),
                directory=str(music_library_path.resolve()),
                playlist_dir=str(playlist_dir.resolve()),
            )

            with open(config_path, "w") as f:
                f.write(rendered_config)

            typer.echo(f"Configuration file created at {config_path}")
            lib = library.Library(str(config_path.resolve()), settings)
            lib.import_dir(str(music_library_path.resolve()))
            typer.echo(f"Successfully imported music from {music_library_path}")
            typer.echo(f"Beets database created at {db_path}")
        else:
            typer.echo("Database exists. Updating library...")
            lib = library.Library(str(config_path.resolve()), settings)
            lib.update_library()
            typer.echo("Library updated successfully.")

    except exceptions.BeetsWrapperError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    except PermissionError as e:
        typer.echo(f"Permission Error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def serve():
    """Starts the MCP server using the configured settings."""
    import os
    import pprint

    pprint.pprint(dict(os.environ))

    settings = get_settings()
    try:
        typer.echo(
            f"Starting MCP server on {settings.mcp_server_host}:{settings.mcp_server_port}"
        )
        mcp_server_main(settings=settings)
    except KeyboardInterrupt:
        typer.echo("Server stopped.")


@app.callback()
def callback(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the application's version and exit.",
    ),
):
    """Main callback for the SmartPlaylist CLI application.

    This callback handles top-level options like --version.
    """


if __name__ == "__main__":
    app()
