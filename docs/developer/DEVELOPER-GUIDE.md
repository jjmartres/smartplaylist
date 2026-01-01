# Developer Guide

This guide provides instructions for developers who want to contribute to the `smartplaylist` project.

## Development Setup

1.  Clone the repository:

    ```bash
    git clone https://github.com/jjmartres/smartplaylist.git
    cd smartplaylist
    ```

2.  Set up the development environment and install dependencies:
    ```bash
    make setup
    ```

## Key Commands

The `Makefile` contains the primary commands for development:

- **`make check`**: Formats the code, runs linting and type checking.
- **`make test`**: Runs the test suite with `pytest`.
- **`make test-in-ci`**: Runs tests and generates a coverage report for CI.
- **`make clean`**: Cleans up temporary files and directories.
- **`make docker-run`**: Builds and runs the Docker container.
- **`make update-version`**: Updates the version in `pyproject.toml` to match the latest git tag.

## Project Structure

The main source code is located in the `src/` directory, organized as follows:

- **`src/smartplaylist/beets_wrapper/`**: The core library for interacting with the `beets` database.
- **`src/smartplaylist/cli/`**: The `typer`-based command-line interface.
- **`src/smartplaylist/mcp_server/`**: The `mcp`-based MCP server.
- **`src/smartplaylist/settings.py`**: The `pydantic-settings` based configuration management.

## Configuration Management

The application uses `pydantic-settings` for configuration. All settings are defined in the `Settings` class in `src/smartplaylist/settings.py`.

To access settings, use the `get_settings()` dependency. This ensures that settings are loaded once and cached.

### Adding a New Setting

1.  Add a new attribute with a type hint to the `Settings` class.
2.  Provide a `Field` with a default value and a description.
3.  If the setting should be loaded from a specific environment variable, provide an `alias`.
4.  If multiple aliases are needed, use `validation_alias=AliasChoices("ALIAS_1", "ALIAS_2")`.

### Accessing Settings

- **MCP Server Tools**: Call `get_settings()` directly inside the tool function.
- **CLI / Other parts**: Call `get_settings()` directly.

## CI/CD Workflows

The project uses GitHub Actions for Continuous Integration and Continuous Deployment. The workflows are defined in the `.github/workflows` directory.

### CI Workflow (`ci.yml`)

This workflow runs on every pull request to `main` and every push to `main`. It ensures that all code meets quality standards.

**Jobs**:
- **`check`**: Runs linting (`ruff`), formatting (`ruff format`), and static type checking (`mypy`).
- **`hadolint`**: Lints the `Dockerfile` for best practices.
- **`test`**: Runs the entire test suite using `pytest` across multiple Python versions (3.11, 3.12).
- **`upload-coverage`**: On pushes to `main`, this job uploads the test coverage report to Codecov.

All checks must pass for a pull request to be mergeable.

### Release Workflow (`release.yml`)

This workflow handles the release process. It is triggered when a new tag in the format `v*.*.*` (e.g., `v1.2.3`) is pushed to the repository.

**Process**:
1.  The workflow extracts the version number from the Git tag.
2.  It updates the `version` field in `pyproject.toml`.
3.  It commits and pushes the updated `pyproject.toml` file back to the `main` branch.
4.  It creates a new GitHub Release with auto-generated release notes based on the conventional commits since the last release.

#### How to Create a Release

1.  Ensure your `main` branch is up to date.
2.  Create and push a new tag:

    ```bash
    git tag -a v1.2.3 -m "Release v1.2.3"
    git push origin v1.2.3
    ```

The release workflow will then run automatically.
