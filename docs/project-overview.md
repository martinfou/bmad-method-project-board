# Project Overview

The **BMAD Method Project Board** is a lightweight Kanban board designed to run locally in developer workspaces. It helps teams manage sprint statuses and epic specifications in an agile, AI-driven development environment.

---

## High-Level Capabilities

- **State Syncing**: Connects with Gemini and Antigravity AI agents to track active tasks.
- **Custom Backends**: No database is required; state is persisted directly in text files to remain lightweight and version-controlled.
- **Dynamic Scaffolding**: Automatically scaffolds initial markdown templates for code components and stories.
- **HUD Interface**: Embeds an active story tracker and a completion progress indicator.

---

## Core Technical Profile

- **Type**: Monolith Web Application
- **Language**: Python 3.10+ and Vanilla JavaScript
- **Styling**: Tailwind CSS
- **Database**: Plain YAML and text files
- **Ecosystem**: BMAD Method

---

## Detailed Documentation Directory

For deep-dives into specific aspects of the codebase, consult the following files in the `docs/` directory:
- **[Architecture Guide](./architecture.md)**: System design patterns and structure.
- **[API Catalog](./api-contracts-root.md)**: REST API contracts and parameters.
- **[Data Models](./data-models-root.md)**: Storage schemas and formats.
- **[Source Tree](./source-tree-analysis.md)**: Full annotated file hierarchy.
- **[Development Guide](./development-guide.md)**: Prerequisites, setup, and CLI commands.
