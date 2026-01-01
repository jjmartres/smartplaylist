# Project Changelog (Memory Bank)

This file serves as a memory bank to track significant changes and learnings during the development process.

## Session starting 2025-12-30

### 1. Configuration Refactoring

- **Centralized MCP Server Configuration**: The MCP server startup logic was refactored. The `smartplaylist serve` CLI command now sources its configuration (host, port, log level) directly from the `pydantic-settings` `Settings` object, ensuring a single source of truth for configuration.
- **Configuration Aliases**: Added shorter aliases (`MCP_HOST`, `MCP_PORT`) for the MCP server host and port environment variables to improve developer experience.
- **Consistent Naming**: Renamed path rewriting environment variables to `SMARTPLAYLIST_MUSIC_LIBRARY_PATH_FROM` and `SMARTPLAYLIST_MUSIC_LIBRARY_PATH_TO` to align with the project's naming convention.

### 2. Testing Improvements

- **Fixed Existing Tests**: Corrected several tests in `tests/test_settings.py` that were using incorrect environment variable names.
- **Added New Tests**: Implemented new tests for the configuration aliases and for the refactored `serve` command to ensure it correctly passes the configuration to the server.
- **Verified Test Suite**: Confirmed that the entire test suite (33 tests) passes after all changes.

### 3. Documentation Overhaul

- **Google-Style Docstrings**: Performed a full-codebase update to convert all Python docstrings in the `src/` directory to the Google style guide for consistency and readability.
- **Comprehensive Configuration Guide**: Significantly updated `docs/user-guide/QUICKSTART.md` with a detailed table of all environment variables, their aliases, descriptions, and default values.
- **New Documentation**: Created a new document, `docs/user-guide/MCP_CLIENTS.md`, to explain how to connect external clients like Gemini, Claude, and Opencode.ai to the MCP server.
- **Architecture & Developer Docs**: Updated architecture diagrams and the developer guide to reflect the refactored server logic and new configuration patterns.
- **Consistency Review**: Performed a full review of all documentation to ensure accuracy and consistency with the current state of the code.

### 4. "Invalid Host Header" Fix

- **Identified Root Cause**: Diagnosed the `Invalid Host header` error as a security feature of the underlying MCP server library.
- **Implemented `TransportSecuritySettings`**: Based on user feedback, adopted the use of `TransportSecuritySettings` in `mcp_server/main.py` to correctly configure trusted hosts.
- **Added New Configuration**: Introduced the `SMARTPLAYLIST_MCP_ALLOWED_HOSTS` environment variable to allow users to specify a list of trusted hostnames.
- **Updated Tests and Documentation**: Updated all relevant tests and documentation (`QUICKSTART.md`, `.env.example`) to reflect the new configuration for trusted hosts.

### 5. Final Polish & Debugging

- **Robust Configuration Parsing**: Added a `field_validator` to `settings.py` to ensure that comma-separated strings for `SMARTPLAYLIST_MCP_ALLOWED_HOSTS` are correctly parsed into a list, making the configuration more robust.
- **Added Debug Logging**: Added a log statement on server startup to print the configured `mcp_allowed_hosts`, aiding in future debugging efforts.
- **Committed Final Changes**: Created a final, well-documented commit for the "Invalid Host header" fix and all associated refactoring and documentation updates.

### 6. Root Cause Discovery & Final Fix

- **Identified True Root Cause**: With the user's help, discovered that the `docker/entrypoint.sh` script was incorrectly overwriting the `SMARTPLAYLIST_MCP_ALLOWED_HOSTS` environment variable with a hardcoded default.
- **Corrected Entrypoint Script**: Fixed the shell script logic to correctly prioritize environment variables passed from `docker-compose.yml`, ensuring the user's configuration is respected.

### 7. Test Coverage Improvement

- Improved test coverage for `src/smartplaylist/cli/main.py` from 39% to 74%.
- Added a test case for the `version_callback` to ensure the `--version` flag works as expected.
- Added a test case for the `sync` command to cover the initialization path.
- Overall project test coverage increased from 87% to 91%.
