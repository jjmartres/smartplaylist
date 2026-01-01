# tests/test_settings.py

import pytest
from pydantic import ValidationError

from smartplaylist.settings import Settings, get_settings


def test_default_settings():
    """Test that the default settings are loaded correctly."""
    get_settings.cache_clear()
    settings = Settings()
    assert settings.log_level == "INFO"
    assert settings.mcp_server_host == "127.0.0.1"
    assert settings.mcp_server_port == 8000


def test_environment_variable_override(monkeypatch):
    """Test that environment variables override default settings."""
    monkeypatch.setenv("SMARTPLAYLIST_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("SMARTPLAYLIST_MCP_SERVER_PORT", "9999")
    get_settings.cache_clear()
    settings = Settings()
    assert settings.log_level == "DEBUG"
    assert settings.mcp_server_port == 9999


def test_validation_error_for_incorrect_type(monkeypatch):
    """Test that a ValidationError is raised for incorrect data types."""
    monkeypatch.setenv("SMARTPLAYLIST_MCP_SERVER_PORT", "not-an-integer")
    get_settings.cache_clear()
    with pytest.raises(ValidationError):
        Settings()


def test_playlist_extension_setting(monkeypatch):
    """Test the playlist_extension setting."""
    get_settings.cache_clear()
    settings = Settings()
    assert settings.playlist_extension == "m3u8"

    monkeypatch.setenv("SMARTPLAYLIST_PLAYLIST_EXTENSION", "m3u")
    get_settings.cache_clear()
    settings = Settings()
    assert settings.playlist_extension == "m3u"

    monkeypatch.setenv("SMARTPLAYLIST_PLAYLIST_EXTENSION", "")
    get_settings.cache_clear()
    settings = Settings()
    assert settings.playlist_extension == "m3u8"


def test_mcp_server_aliases(monkeypatch):
    """Test that the aliases for MCP server settings work correctly."""
    monkeypatch.setenv("MCP_HOST", "0.0.0.0")
    monkeypatch.setenv("MCP_PORT", "9999")
    get_settings.cache_clear()
    settings = Settings()
    assert settings.mcp_server_host == "0.0.0.0"
    assert settings.mcp_server_port == 9999


@pytest.mark.parametrize(
    "env_var, env_value, expected_list",
    [
        ("SMARTPLAYLIST_MCP_ALLOWED_HOSTS", "host1,host2", ["host1", "host2"]),
        ("SMARTPLAYLIST_MCP_ALLOWED_HOSTS", '["host1", "host2"]', ["host1", "host2"]),
        ("MCP_ALLOWED_HOSTS", "host3,host4", ["host3", "host4"]),
        ("MCP_ALLOWED_HOSTS", '["host3", "host4"]', ["host3", "host4"]),
    ],
)
def test_allowed_hosts_parsing(monkeypatch, env_var, env_value, expected_list):
    """Test that the allowed hosts are parsed correctly from different env vars."""
    monkeypatch.setenv(env_var, env_value)
    get_settings.cache_clear()
    settings = Settings()
    assert settings.mcp_allowed_hosts == expected_list
