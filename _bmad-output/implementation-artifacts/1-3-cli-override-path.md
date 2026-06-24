---
baseline_commit: f46a5dd108026e68642631fb2a6277636b03bd41
---
# Story 1.3: cli-override-path

Status: review

## Story

As a developer,
I want to be able to explicitly pass a `--project-root` CLI flag to override the automatic directory resolution,
so that I can run the server against any directory of my choice.

## Acceptance Criteria

1. Add argparse argument `--project-root` to `project_board_server.py`.
2. When the flag `--project-root` is supplied (e.g. `--project-root /some/other/path`), the server must resolve this path and use it as the workspace root, bypassing marker-based auto-detection.
3. Keep the `--port` option functional so it can be combined with `--project-root`.

## Tasks / Subtasks

- [x] Add `--project-root` option to `argparse` configuration in `project_board_server.py` (AC: 1)
- [x] Connect `--project-root` input value to `find_project_root()` function override parameter (AC: 2)
- [x] Verify overriding project root runs server successfully with custom path (AC: 3)

## Dev Notes

- Make sure paths are resolved using `.resolve()` to avoid issues with relative overrides like `--project-root .`.

## Dev Agent Record

### Agent Model Used

Antigravity (Google DeepMind)

### Debug Log References

- Executed local tests: `python3 test_project_board_server.py` (5 tests passed, output verified)

### Completion Notes List

- Verified argparse contains `--project-root` option.
- Bypassed automatic root resolution if `--project-root` is provided.
- Kept `--port` functional and combined successfully with `--project-root`.
- Wrote two unit tests checking the command-line interface logic, mocking out the server binding to ensure quick and isolated verification.

### File List

- [project_board_server.py](file:///Volumes/T7/src/bmad-method-project-board/project_board_server.py)
- [test_project_board_server.py](file:///Volumes/T7/src/bmad-method-project-board/test_project_board_server.py)

### Review Findings

- [x] [Review][Dismissed] Out-of-scope Backend Feature Addition — User opted to keep.
- [x] [Review][Dismissed] Out-of-scope Frontend Feature Addition — User opted to keep.
- [x] [Review][Patch] Subtask Implementation Mismatch [project_board_server.py]
- [x] [Review][Patch] Unhandled PermissionError on .agents check [project_board_server.py:27-32]
- [x] [Review][Patch] Robustify PRD/Brief file lookup and error handling (Glob exceptions, arbitrary sorting, magic paths) [project_board_server.py]
- [x] [Review][Patch] Redundant path traversal if cwd == script_dir [project_board_server.py]
- [x] [Review][Patch] Naive Date Parsing Vulnerability and NaN Display Risk [project_board_static/app.js]
- [x] [Review][Patch] Fix custom markdown parser (HTML escaping, blockquote parsing, code blocks) [project_board_static/app.js]
- [x] [Review][Patch] Sloppy Modal Fallback Title [project_board_static/app.js]
- [x] [Review][Patch] Fix test issues (global state mutation leaks, stderr pollution) [test_project_board_server.py]
