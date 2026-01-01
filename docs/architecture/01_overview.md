# Architecture Overview

## Project Purpose

`smartplaylist` is a tool designed to enable human-like interaction with a [beets](https://beets.io/) music library. It provides a flexible and extensible framework for managing and querying your music collection in a natural and intuitive way.

## High-Level Architecture

The project follows a layered architecture, promoting separation of concerns and modularity.

```mermaid
graph TD;
    A[User] --> B{Interaction Layer};
    B --> C[CLI (Typer)];
    B --> D[MCP Server];
    C --> E[Core Library];
    D --> E;
    E --> F[beets-wrapper];
    F --> G[Beets Database];
```

### Layers

1.  **Core `beets-wrapper` Library**: This is the foundation of the project. It provides a Pythonic interface to the beets library, abstracting away the complexities of direct database interaction.

2.  **CLI (`typer`)**: A command-line interface built with `typer` provides a set of tools for developers and users to interact with the `smartplaylist` functionalities from the terminal.

3.  **MCP Server**: A server exposes the core functionalities through a Multi-Call-Platform (MCP) interface, allowing for remote and programmatic interaction.

    The server adheres to the **Model-Context-Protocol (MCP)**, which simplifies client-side interactions by using a single, standardized endpoint (`/mcp`) for all tool executions. This RPC-style (Remote Procedure Call) interaction, where the tool name and its parameters are sent in the request body of a `POST` request, makes `POST` the most suitable HTTP method. It allows for a consistent and predictable API, making it easier for clients and other services to interact with the server.

