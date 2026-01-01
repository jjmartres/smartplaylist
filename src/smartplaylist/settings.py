"""Configuration settings for the SmartPlaylist application.

This module defines the application's configuration settings using Pydantic's
BaseSettings. It allows for loading configuration from environment variables and
.env files.
"""

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Defines application configuration settings, loaded from environment variables.

    Attributes:
        beets_config_path: Path to the beets configuration file.
        log_level: The logging level for the application.
        mcp_server_host: The host for the MCP server.
        mcp_server_port: The port for the MCP server.
        playlist_extension: The file extension for generated playlists.
        music_library_path_from: The source path prefix to be replaced.
        music_library_path_to: The target path prefix to substitute.
        mcp_allowed_hosts: A list of allowed hosts for the MCP server.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    beets_config_path: Path = Field(
        default=Path("~/.config/smartplaylist/config.yaml").expanduser(),
        alias="SMARTPLAYLIST_CONFIG_PATH",
        description="The path to the SmartPlaylist configuration file.",
    )
    log_level: str = Field(
        default="INFO",
        alias="SMARTPLAYLIST_LOG_LEVEL",
        description="The logging level for SmartPlaylist MCP server.",
    )
    mcp_server_host: str = Field(
        default="127.0.0.1",
        validation_alias=AliasChoices("SMARTPLAYLIST_MCP_SERVER_HOST", "MCP_HOST"),
        description="The SmartPlaylist MCP server host listening on.",
    )
    mcp_server_port: int = Field(
        default=8000,
        validation_alias=AliasChoices("SMARTPLAYLIST_MCP_SERVER_PORT", "MCP_PORT"),
        description="The SmartPlaylist MCP server port listening on.",
    )
    playlist_extension: str = Field(
        default="m3u8",
        alias="SMARTPLAYLIST_PLAYLIST_EXTENSION",
        description="The file extension for generated playlists.",
    )
    music_library_path_from: Path | None = Field(
        default=None,
        alias="SMARTPLAYLIST_MUSIC_LIBRARY_PATH_FROM",
        description="The source path prefix to be replaced in playlist files.",
    )
    music_library_path_to: Path | None = Field(
        default=None,
        alias="SMARTPLAYLIST_MUSIC_LIBRARY_PATH_TO",
        description="The target path prefix to substitute in playlist files.",
    )
    mcp_allowed_hosts: list[str] | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "SMARTPLAYLIST_MCP_ALLOWED_HOSTS", "MCP_ALLOWED_HOSTS"
        ),
        description="A list of allowed hosts for the MCP server.",
    )

    @field_validator("playlist_extension")
    def empty_str_to_default(cls, v: str) -> str:
        """Sets the default value if the environment variable is an empty string."""
        if v == "":
            return "m3u8"
        return v

    @field_validator("mcp_allowed_hosts", mode="before")
    def robust_str_to_list(cls, v: Any) -> Any:
        """Parses a string from an env var into a list of strings."""
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [host.strip() for host in v.split(",")]
        return v


@lru_cache
def get_settings() -> Settings:
    """Provides the application settings as a cached dependency."""
    logging.info("Loading configuration settings.")
    settings = Settings()
    logging.info("Configuration loaded from: .env file, environment variables.")
    return settings
