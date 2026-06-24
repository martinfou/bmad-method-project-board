# Story 1.4: dynamic-config-binding

Status: ready-for-dev

## Story

As a developer,
I want the project board server to dynamically bind to the correct configuration and resolve artifact locations from the resolved workspace,
so that the server does not crash when configuration elements are missing or path locations are custom.

## Acceptance Criteria

1. Attempt to load the BMad project configuration (e.g. `_bmad/bmm/config.yaml` or standard config files) from the dynamically resolved project root.
2. If configuration is present, parse it to extract custom paths for implementation and planning artifacts (if defined).
3. If configuration is absent, fall back to standard defaults:
   - Implementation artifacts: `{project_root}/_bmad-output/implementation-artifacts`
   - Planning artifacts: `{project_root}/_bmad-output/planning-artifacts`
4. Ensure the backend handles missing or empty `sprint-status.yaml` files gracefully by serving an empty board response (valid JSON structure with empty lists) rather than raising internal server errors (500).

## Tasks / Subtasks

- [ ] Implement configuration parsing logic (AC: 1, 2)
- [ ] Implement fallback to default directories (AC: 3)
- [ ] Add exception handling for missing status or config files to return graceful default JSON payloads (AC: 4)

## Dev Notes

- Since we are zero-dependency, configuration parsing should be done using simple standard library methods (e.g. standard file reading or yaml/toml-like regex parsers if needed, or simply defaulting to the yaml parser already used for sprint-status).
- A simple key-value parser for basic YAML/TOML config keys is preferred over bringing in heavy libraries.

## Dev Agent Record

### Agent Model Used

Gemini 1.5 Pro

### Debug Log References

### Completion Notes List

### File List
