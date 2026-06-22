# BMAD Method Project Board

A zero-dependency, lightweight Kanban board and task inspector to manage BMAD Method project sprints and epic specifications.

## Features

- **Dynamic Kanban Swimlanes**: Manage stories through Backlog, Ready for Dev, In Progress, Blocked, Review, and Done states.
- **Task Inspector**: Check or uncheck subtasks inside story files, toggle story active pinning, and view/regenerate specifications.
- **Epic Specifications**: Dynamically read and render Epic scopes and child stories directly from workspace planning documents.
- **Copyable CLI Commands**: Easily copy the correct Antigravity command (e.g. `dev this story`) for your active coding task.
- **Persistent State Trace**: Atomically writes the active story key to `_bmad-output/last-active-story.txt` on status transition or selection.

## Local Usage

Run the server from your terminal inside any project workspace directory containing `_bmad-output/implementation-artifacts/sprint-status.yaml`:

```bash
python3 project_board_server.py --project-root /path/to/your/project --port 8010
```

Open your browser to `http://localhost:8010`.

## Global Gemini Skill Integration

To run this as a global Gemini skill on your machine:

1. Copy or symlink this folder to your global config directory:
   ```bash
   cp -r . /Users/martinfou/.gemini/config/skills/bmad-sprint-status-ui
   ```
2. Trigger the board inside Antigravity by saying:
   - `show sprint status` or `open project board`
