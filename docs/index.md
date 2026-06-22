# Project Documentation Index

This index serves as the entry point and primary reference map for AI agents and developers working on the BMAD Method Project Board.

---

### Project Overview

- **Repository Type**: Monolith
- **Primary Language**: Python 3 and Vanilla JavaScript
- **Architecture**: Single Page Application (SPA) Client + Python HTTP Server

---

### Quick Reference

- **Tech Stack**: Python 3 standard library, HTML5/CSS3/Vanilla JS, Tailwind CSS CDN, FontAwesome Icons CDN
- **Entry Point**: `project_board_server.py`
- **Main Config File**: `_bmad/config.toml`

---

### Generated Documentation

- [Project Overview](./project-overview.md)
- [Architecture Guide](./architecture.md)
- [Source Tree Analysis](./source-tree-analysis.md)
- [Development Guide](./development-guide.md)
- [API Contracts](./api-contracts-root.md)
- [Data Models](./data-models-root.md)
- [Component Inventory](./component-inventory-root.md) _(To be generated)_

---

### Existing Documentation

- [README.md](../README.md) - General user guide, commands, and installation instructions.

---

### Getting Started

To launch the server locally:
```bash
python3 project_board_server.py --project-root . --port 8010
```

Once running, navigate your browser to `http://localhost:8010`.
To invoke AI tasks and developer sprint planning features, ensure you have initialized BMad Method via `npx bmad-method install`.
