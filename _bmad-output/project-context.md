---
project_name: 'bmad-method-project-board'
user_name: 'Martin'
date: '2026-06-22'
sections_completed: ['technology_stack']
existing_patterns_found: 4
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- **Backend Language**: Python 3 (standard library only, zero-dependency)
- **Frontend Stack**: Single Page Application (HTML5, Vanilla JavaScript)
- **Styling**: Tailwind CSS via CDN (v3.x, customized config in `<head>`), FontAwesome Icons via CDN
- **Data Persistence**: Local YAML (`sprint-status.yaml` parsed with custom regex-based parser) and active state text files (`last-active-story.txt`)
- **Agent Integration**: BMad Method (v6.8.0), BMad Core (v6.8.0), BMad Builder (v2.1.0), Whiteport Design Studio (v0.4.3)

## Critical Implementation Rules

- **Zero-Dependency Rule**: Do not introduce any external Python library dependencies (e.g., `PyYAML`, `requests`, `Flask`). Always stick to Python's standard library.
- **Tailwind CDN Styling**: When modifying the UI, use inline Tailwind CSS classes. Any custom theme settings must be configured inside the inline `tailwind.config` block.
- **Vanilla JavaScript**: Keep the frontend in plain, vanilla JavaScript inside `project_board_static/app.js`. Avoid introducing frameworks like React, Vue, or build-step tools.
- **YAML Parsing Safety**: The backend parses `sprint-status.yaml` using line-by-line custom text splitting. Make sure any status updates follow the exact formatting to avoid breaking the manual parser.
