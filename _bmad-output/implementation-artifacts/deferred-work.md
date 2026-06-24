## Deferred from: code review of 1-1-plugin-manifest.md (2026-06-24)

- **Mismatched script path for HTTP server launch action** ([.agents/manifest.json:28]): The manifest launch command points to `{skill-root}/scripts/project_board_server.py`, but the script is currently located at the repository root. This is deferred until Story 2.3 directory restructuring.
- **Non-existent script for static dashboard generation render action** ([.agents/manifest.json:23]): The manifest render command references `render_sprint_status.py`, which has not yet been added to the repository. This is deferred until Story 2.3 skill folder packaging.
- **Mismatched skill source path in manifest** ([.agents/manifest.json:17]): The manifest specifies `"path": "skills/bmad-sprint-status-ui"`, but there is no `skills` folder in the repository yet. This is deferred until Story 2.3 directory restructuring.
- **Hardcoded port in server launch command** ([.agents/manifest.json:28]): The launch command defines a hardcoded port `--port 8010` which does not handle port collisions. This is deferred until Story 2.4 where dynamic port collision scanning is implemented.
- **Platform-dependent Python interpreter command** ([.agents/manifest.json:23,28]): The launch and render commands specify `python3` which is not portable to Windows environments where only `python` is available.

## Deferred from: code review of 1-2-dynamic-root-resolution.md (2026-06-24)

- **Brittle exception handling scope in wildcard searches** ([project_board_server.py:80-99]): A try-except block wraps the entire search loop, meaning a single unreadable file halts the entire search. Deferred to Story 1.5.
- **API masks missing PRD resource with 200 OK** ([project_board_server.py:99]): Returning successful JSON placeholder responses for missing PRD resources complicates client-side routing. Deferred to Story 1.5.
- **Non-deterministic file selection on glob files** ([project_board_server.py:73-88]): Glob lists are not sorted, leading to arbitrary selection if multiple files match. Deferred to Story 1.5.
- **API request path trailing slash or query mismatch** ([project_board_server.py:635]): Request paths with trailing slashes or query parameters are not matched correctly by the routing table. Deferred to Story 1.5.
