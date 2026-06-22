# Development Guide

This guide provides instructions for setting up, running, and developing the BMAD Method Project Board locally.

---

## Prerequisites
- **Python 3.10+** (standard library only)
- A modern web browser (Chrome, Firefox, Safari, Edge)

---

## Installation & Setup
No additional library installation is required since the codebase has zero external dependencies.

To clone the repository and prepare the directories:
```bash
git clone https://github.com/martinfou/bmad-method-project-board.git
cd bmad-method-project-board
```

To configure the project with the **BMAD Method** agentic workflow support:
```bash
npx bmad-method install
```

---

## Running Locally
To launch the Project Board server, execute the python script in your terminal:
```bash
python3 project_board_server.py --project-root /path/to/your/project --port 8010
```

- `--project-root`: Absolute path to your active coding workspace (default: current working directory).
- `--port`: The local port to run the server on (default: `8010`).

Open your browser and navigate to `http://localhost:8010`.

---

## Workspace Structure & Setup
For the board to render cards, the project root must contain the following file:
`_bmad-output/implementation-artifacts/sprint-status.yaml`

If this file does not exist, the server will serve an empty board. When a story's status changes on the board, the server will write status transitions back to the YAML file and scaffold the story markdown specification inside `_bmad-output/implementation-artifacts/`.

---

## Developing
- **Backend changes**: Edit `project_board_server.py`. The HTTP server serves files dynamically on every page request (no hot-reloading tool needed, just refresh the browser page).
- **Frontend changes**:
  - HTML Layout: Edit `project_board_static/index.html`.
  - JS Logic: Edit `project_board_static/app.js`.
- **CSS styling**: Done via inline Tailwind CSS classes. If you need custom styles, customize the inline `tailwind.config` configuration script in `index.html`.
