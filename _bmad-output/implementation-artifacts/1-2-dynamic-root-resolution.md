---
baseline_commit: f46a5dd108026e68642631fb2a6277636b03bd41
---
# Story 1.2: dynamic-root-resolution

Status: done

## Story

As an operator starting the project board server,
I want the server to dynamically detect the project workspace root directory based on signature markers,
so that it runs correctly without requiring a manual path override from any directory.

## Acceptance Criteria

1. Implement `find_project_root` helper in `project_board_server.py` that walks up directory trees to find a valid workspace.
2. Search for markers: `.agents/` directory, `project-context.md` file, or `_bmad-output/` directory.
3. Check path ancestry starting from:
   - The directory containing `project_board_server.py`.
   - The current working directory (CWD) of the shell.
4. Fallback to current working directory (CWD) if no signature markers are found in the ancestors.
5. Update server configuration paths (like YAML_PATH, ARTIFACTS_DIR, PLANNING_DIR) to resolve relative to the detected workspace root.

## Tasks / Subtasks

- [x] Implement `find_project_root` in `project_board_server.py` (AC: 1, 2, 3, 4)
- [x] Update server initialization path resolvers to use the dynamically resolved root (AC: 5)
- [x] Test resolving root when running the server from a nested subdirectory of the project workspace (AC: 1)

## Dev Notes

- Ensure `Path` from standard library `pathlib` is used.
- Avoid platform-specific libraries. Keep everything standard-library Python.

## Dev Agent Record

### Agent Model Used

Antigravity (Google DeepMind)

### Debug Log References

- Ran new unit tests: `python3 test_project_board_server.py` (Exited with 0, 2 tests passed)
- Verified dynamic workspace path resolution on port 8012 nested: CWD set to `project_board_static/`, ran `python3 ../project_board_server.py --port 8012`, queried `/api/prd`, correctly returned workspace product brief content.

### Completion Notes List

- Implemented `find_project_root` walked up ancestor hierarchy searching for signature markers (`.agents/`, `project-context.md`, or `_bmad-output/`), returning CWD as fallback.
- Configured YAML, planning, and artifacts directories to resolve relative to resolved root.
- Created `test_project_board_server.py` to cover resolution logic.

### File List

- [project_board_server.py](file:///Volumes/T7/src/bmad-method-project-board/project_board_server.py)
- [test_project_board_server.py](file:///Volumes/T7/src/bmad-method-project-board/test_project_board_server.py)

### Review Findings

- [x] [Review][Patch] Flaky test assertions on real filesystem [test_project_board_server.py:14-29]
- [x] [Review][Patch] Conditional test execution silent pass [test_project_board_server.py:22-29]
- [x] [Review][Patch] Shell CWD resolve failure crash risk [project_board_server.py:40]
- [x] [Review][Patch] Lack of strict type validation on signature markers [project_board_server.py:47-51]
- [x] [Review][Defer] Brittle exception handling scope in wildcard searches [project_board_server.py:80-99] — deferred, pre-existing
- [x] [Review][Defer] API masks missing PRD resource with 200 OK [project_board_server.py:99] — deferred, pre-existing
- [x] [Review][Defer] Non-deterministic file selection on glob files [project_board_server.py:73-88] — deferred, pre-existing
- [x] [Review][Defer] API request path trailing slash or query mismatch [project_board_server.py:635] — deferred, pre-existing
