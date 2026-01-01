# smartplaylist Development Guidelines for AI Agents

This document provides a comprehensive guide for AI agents contributing to the `smartplaylist` repository. Adhering to these guidelines will ensure code consistency, quality, and maintainability.

## 1. Development Environment

To set up your local development environment, run the following command. This will create a virtual environment using `uv` and install all necessary dependencies.

```bash
make setup
```

### Configuration

Create a `.env` file in the root of the project for local configuration. You can use `.env.example` as a template. The most important variable is `SMARTPLAYLIST_CONFIG_PATH`, which should point to your beets `config.yaml` file.

## 2. Core Commands

All development commands are managed through the `Makefile` for consistency.

### Linting and Formatting

- **Check and fix all code**: 
    ```bash
    make check
    ```
    This command runs `ruff format`, `ruff check --fix`, and `mypy` to ensure code is well-formatted, lint-free, and type-safe.

### Testing

- **Run all tests**:
    ```bash
    make test
    ```
- **Run a single test file**:
    ```bash
    uv run pytest tests/test_cli/test_main.py
    ```
- **Run a single test function by name**:
    ```bash
    uv run pytest tests/test_cli/test_main.py -k test_sync_initialization_success
    ```
- **Run tests with coverage**: 
    ```bash
    make test-in-ci
    ```
    This generates an XML coverage report in the `coverage/` directory, which is used by the CI.

## 3. Code Style

We follow standard Python best practices, enforced by `ruff` and `mypy`.

### Formatting

- Code is formatted with `black` conventions via `ruff format`.
- Line length is set to 88 characters, as defined in `pyproject.toml`.
- Always run `make check` before committing.

### Imports

- Imports are automatically sorted by `ruff`.
- Group imports into three sections: standard library, third-party, and first-party (application-specific), separated by a blank line.
- Example:
    ```python
    import logging
    from pathlib import Path

    import pytest
    from smartplaylist.beets_wrapper import models

    from smartplaylist.exceptions import SmartPlaylistError
    ```

### Naming Conventions

- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Modules**: `snake_case`

### Type Hinting

- All functions and methods **must** have type hints for all arguments and return values.
- Use the `typing` module for complex types.
- Run `make check` to verify type correctness with `mypy`.

### Docstrings

- All public modules, classes, and functions **must** have docstrings.
- Use **Google-style docstrings** for clarity and consistency.
- Example:
    ```python
    def my_function(param1: int, param2: str) -> bool:
        """This is a Google-style docstring.

        Args:
            param1: The first parameter.
            param2: The second parameter.

        Returns:
            True if successful, False otherwise.
        """
        return True
    ```

### Error Handling

- Use the custom exception classes defined in `src/smartplaylist/exceptions.py` for application-specific errors.
- Raise specific exceptions instead of generic ones like `Exception`.
- Example:
    ```python
    from smartplaylist.exceptions import SmartPlaylistError

    def do_something():
        if something_bad_happened:
            raise SmartPlaylistError("Something bad happened")
    ```

## 4. Project Structure

- `src/smartplaylist`: Contains the main application code.
- `tests/`: Contains all tests, mirroring the `src` structure.
- `pyproject.toml`: Defines project metadata and dependencies.
- `Makefile`: Contains all development commands.

## 5. Dependency Management

- Dependencies are managed with `uv`.
- Project dependencies are listed in `pyproject.toml` under `[project.dependencies]`.
- To add a new dependency, add it to `pyproject.toml` and run `make setup`.

## 6. External Rules

This repository does not contain any `.cursor` or `.github/copilot` rules. All guidelines are defined in this document.

## 7. Active Technologies

- **Python**: 3.11+
- **CLI**: `typer`, `click`
- **MCP Server**: `mcp` library
- **Configuration**: `pydantic`, `pydantic-settings`
- **Linting/Formatting**: `ruff`
- **Type Checking**: `mypy`
- **Testing**: `pytest`
- **Dependency Management**: `uv`
