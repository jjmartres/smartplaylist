<!--
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- List of modified principles: N/A (initial version)
- Added sections: Core Principles, Non-Negotiables, Tool Design Principles, Data Integrity Rules, Governance
- Removed sections: N/A
- Templates requiring updates:
  - .specify/templates/plan-template.md (⚠ pending)
  - .specify/templates/spec-template.md (⚠ pending)
  - .specify/templates/tasks-template.md (⚠ pending)
- Follow-up TODOs: None
-->
# SmartPlaylist Constitution

## Core Principles

### 1. Read-Only First
All operations treat the music library as **immutable by default**.
- Never modify source FLAC files
- Never rewrite metadata without explicit consent
- Database operations are read-only unless explicitly requested
- Playlists are generated outputs, not destructive operations

### 2. Query-Driven Architecture
All music discovery flows through **beets query language**.
- Natural language prompts convert to beets queries
- Direct beets queries are first-class citizens
- Query validation happens before execution
- Results are always projections, never mutations

### 3. MCP as Thin Adapter
The MCP server is a **protocol adapter only**.
- No business logic in tool handlers
- Tools delegate to library functions immediately
- Server layer handles serialization/deserialization only
- Keep tool handlers under 10 lines

### 4. Playlist as Pure Output
Playlists are **generated artifacts, not state**.
- Playlist generation is idempotent
- Same query always produces same playlist
- Playlists reference music, never copy
- M3U8 format for UTF-8 French artist support

## Non-Negotiables

### What We Never Do
❌ Modify source music files
❌ Write business logic in MCP tool handlers
❌ Auto-tag or fetch metadata without explicit request
❌ Move or rename music files
❌ Store mutable state between queries

### What We Always Do
✅ Validate queries before execution
✅ Use relative paths in playlists
✅ Support natural language through LLM conversion
✅ Keep beets library database separate from music files
✅ Generate playlists in dedicated output directory

## Tool Design Principles

### Every Tool Must
1. Accept minimal required parameters
2. Return structured JSON or file paths
3. Handle errors gracefully with context
4. Execute in under 3 seconds for typical queries
5. Work with 14k+ track libraries efficiently

### Natural Language Support
- LLM converts prompts to beets queries
- Original prompt and generated query both logged
- User can see and learn beets query syntax
- Failed conversions suggest query syntax examples

## Data Integrity Rules
1. **Source of Truth**: Music files and their embedded metadata
2. **Beets Database**: Cached index for fast queries (disposable)
3. **Playlists**: Generated outputs (regeneratable)
4. **No Writes**: Unless explicitly in "update mode" (future feature)

**When in doubt: Query, don't modify. Generate, don't mutate.**

## Governance

This Constitution is the source of truth for all development practices. All code, tools, and processes must adhere to these principles. Amendments require review, documentation, and a clear migration plan for existing systems.

**Version**: 1.0.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-25
