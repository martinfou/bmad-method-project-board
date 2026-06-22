# Source Tree Analysis

This document describes the directory structure, file hierarchy, and entry points of the BMAD Method Project Board repository.

---

## Annotated Directory Tree

```
bmad-method-project-board/
├── .agent/                             # Local Antigravity agent integration configurations (gitignored)
├── .agents/                            # Local Gemini agent integration configurations (gitignored)
├── _bmad/                              # Installer-managed BMAD modules (v6.8.0)
│   ├── _config/                        # Universal CLI helps and catalogs
│   ├── bmb/                            # BMad Builder module configs
│   ├── bmm/                            # BMad Core / Method module configs
│   ├── cis/                            # Creative Intelligence Suite configs
│   ├── core/                           # Universal core runner configs
│   ├── custom/                         # User & team customization overrides
│   ├── scripts/                        # Utility scripts (e.g. resolve customization)
│   ├── tea/                            # Test Architect module configs
│   └── wds/                            # Web Design Studio module configs
├── _bmad-output/                       # Core output folder for sprint status and specs
│   ├── implementation-artifacts/       # Sprint status files and story spec files
│   ├── planning-artifacts/             # PRD, Architecture, and Epics files
│   └── test-artifacts/                 # Test design, reviews, and automation reports
├── design-artifacts/                   # WDS user psychology and scenario artifacts
├── docs/                               # Project knowledge and index documentation
│   ├── api-contracts-root.md           # API contracts mapping endpoints
│   ├── data-models-root.md             # Persistence design and schemas
│   └── project-scan-report.json        # Workspace scanning state file (gitignored)
├── project_board_static/               # Static web frontend files
│   ├── app.js                          # SPA client logic (fetch calls, layout rendering)
│   └── index.html                      # Layout, HUD, and Tailwind customized GUI
├── .gitignore                          # Exclusions for personal TOMLs & agent folders
├── project_board_server.py             # Main entry point (Python HTTPServer)
└── README.md                           # Repository usage guide
```

---

## Critical Files & Entry Points

- **`project_board_server.py`**: The server bootstrapper. Parses `--project-root` and `--port` CLI arguments and runs `http.server.HTTPServer` at `localhost:8010`.
- **`project_board_static/index.html`**: The UI layout file. Loads Tailwind CSS, customizes theme variables, links FontAwesome icon styles, and renders the Kanban columns and Task Inspector panel.
- **`project_board_static/app.js`**: Orchestrates event handlers for drag-and-drop, reload triggers, and sends async `fetch` payloads to the backend API endpoints.
