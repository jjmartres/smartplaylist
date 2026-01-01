from typer.testing import CliRunner
from smartplaylist.cli.main import app, __version__
from smartplaylist.settings import get_settings

runner = CliRunner()


def test_version_callback():
    """Tests the --version option."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"SmartPlaylist Version: {__version__}" in result.stdout


def test_sync_initialization_success(mocker, tmp_path):
    """Test the sync command's successful initialization path."""
    # Arrange
    music_dir = tmp_path / "music"
    music_dir.mkdir()

    mock_library = mocker.patch("smartplaylist.beets_wrapper.library.Library")
    mock_library.db_exists.return_value = False

    # Act
    result = runner.invoke(app, ["sync", str(music_dir)])

    # Assert
    assert result.exit_code == 0
    assert "No database found. Initializing new database..." in result.stdout
    assert "Successfully imported music" in result.stdout

    mock_library.db_exists.assert_called_once()
    config_path = music_dir / ".smartplaylist" / "config.yaml"

    mock_library.assert_called_once_with(str(config_path.resolve()), get_settings())
    mock_library.return_value.import_dir.assert_called_once_with(
        str(music_dir.resolve())
    )


def test_serve_command(mocker, monkeypatch):
    """Test that the serve command calls the mcp server with the correct settings."""
    mock_mcp_main = mocker.patch("smartplaylist.cli.main.mcp_server_main")

    monkeypatch.setenv("SMARTPLAYLIST_MCP_SERVER_HOST", "testhost")
    monkeypatch.setenv("SMARTPLAYLIST_MCP_SERVER_PORT", "9999")
    monkeypatch.setenv("SMARTPLAYLIST_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("SMARTPLAYLIST_MCP_ALLOWED_HOSTS", '["testhost.local"]')

    get_settings.cache_clear()

    result = runner.invoke(app, ["serve"])

    assert result.exit_code == 0
    mock_mcp_main.assert_called_once()

    args, kwargs = mock_mcp_main.call_args
    passed_settings = kwargs["settings"]

    assert passed_settings.mcp_server_host == "testhost"
    assert passed_settings.mcp_server_port == 9999
    assert passed_settings.log_level == "DEBUG"
    assert passed_settings.mcp_allowed_hosts == ["testhost.local"]
