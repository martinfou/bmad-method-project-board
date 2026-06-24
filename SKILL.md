---
name: bmad-sprint-status-ui
description: Generate a rich visual Markdown dashboard or launch the interactive, web-based BMad local project board.
---

# BMad Sprint Status UI

Run the local server to view the project board:

```bash
python3 .agents/skills/bmad-sprint-status-ui/project_board_server.py
```

## Description
This skill provides a full UI dashboard to view and manage Epics and Stories using the BMad Method.

## Agent Instructions (Launch Intent)
When the user asks to "open project board", "start dashboard", or "view board":
1. Execute the server script (`.agents/skills/bmad-sprint-status-ui/project_board_server.py`) as a background task. The server automatically scans for an open port starting at `8010` and handles collisions gracefully.
2. Read the console output from the background task to identify which port the server actually bound to (e.g., "running on http://localhost:8010").
3. Respond to the user with a clickable markdown link to that specific URL (e.g. `[Open Dashboard](http://localhost:8010)`).
4. Do not attempt to use terminal commands to open the browser unless explicitly requested. Provide the URL and allow the user to click it.
