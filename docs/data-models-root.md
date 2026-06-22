# Data Models & Persistence

This document describes the file-based persistence data structures utilized by the BMAD Method Project Board.

---

## 1. Sprint Status Configuration (`sprint-status.yaml`)
The board tracks all metadata and story workflow states inside a standard YAML file parsed dynamically by the backend:
- **Location**: `{project-root}/_bmad-output/implementation-artifacts/sprint-status.yaml`
- **Schema**:
  - Top level properties (metadata):
    - `name`: Name of the sprint or project.
    - `last_updated`: Timestamp of last state change in ISO format.
  - `development_status` block:
    - Lists keys and values representing story IDs and their corresponding workflow status (`backlog`, `ready-for-dev`, `in-progress`, `blocked`, `review`, `done`).

**Example File Structure:**
```yaml
name: "Trading Bridge Sprint 1"
last_updated: "2026-06-22T04:18:00Z"

development_status:
  epic-desktop-gui: in-progress
  dg-1-setup: ready-for-dev
  dg-2-implementation: backlog
```

---

## 2. Active Workspace State (`last-active-story.txt`)
The active pinned story is tracked as a single string written to a flat text file in the implementation output directory:
- **Location**: `{project-root}/_bmad-output/last-active-story.txt`
- **Content**: String containing the story key (e.g. `dg-1-setup`). An empty file implies no pinned task.

---

## 3. Story Specification Markdown Template
When transitioned to `ready-for-dev`, story files are scaffolded in markdown with frontmatter metadata:
- **Location**: `{project-root}/_bmad-output/implementation-artifacts/{story_key}.md`
- **Schema**:
  - **YAML Frontmatter**:
    - `baseline_commit`: The git commit hash at the time of development start.
  - **Sections**:
    - `# Story: <Title>`: Heading containing the title.
    - `Status: <status>`: String representing the status.
    - `## Story`: Markdown block describing the story role, feature request, and logic.
    - `## Acceptance Criteria`: Numbered list of criteria including checkbox markers:
      - `1. **AC1 — Description**:`
      - `   - [ ] verification detail`
    - `## Tasks / Subtasks`: Checklist of tasks for the developer:
      - `- [ ] Task details`

**Example Story Specification File:**
```markdown
---
baseline_commit: f571ee4568cc6f1b19ee67c58dbcad61cbb89579
---
# Story: Setup GUI Layout

Status: ready-for-dev

## Story
As a developer, I want to implement the layout configuration so that users see a responsive swimlane dashboard.

## Acceptance Criteria
1. **AC1 — Verification**:
   - [ ] Layout renders all columns correctly on standard viewport widths.

## Tasks / Subtasks
- [ ] Task 1: Core Implementation
- [ ] Task 2: Testing & Verification
```
