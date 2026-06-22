# Persona: AI Agent Executor (Gemini / Antigravity)

**Role**: Autonomous Code Implementation Agent
**Domain**: Auto-scaffolding, testing, and story development

---

## 1. Profile & Mindset
The agent is a local-running AI subagent process launched by the developer. It processes text instructions and file structures. It does not have human intuition, so it relies entirely on structured files, strict path patterns, and explicit exit codes.

---

## 2. Operational Driving Forces

### Positive (Clarity & Enablement)
- **Scaffolded story checklists**: Checkboxes formatted as `- [ ] Task Details` allow the agent to update and log progress in a structured manner.
- **Trace file markers**: `last-active-story.txt` gives the agent an instant anchor to determine what story it is assigned to.

### Negative (Friction & Obstacles)
- **Regex parsing failures**: Spacing shifts or custom YAML edits that break the backend parser prevent the agent from loading board coordinates.
- **Unstructured briefs**: Broad/vague task statements lead the agent to hallucinate implementation approaches, causing code review rejections.

---

## 3. Interaction Strategy
- Reads `sprint-status.yaml` to identify its current task.
- Reads and updates the story markdown file checklists inside `_bmad-output/implementation-artifacts/`.
- Logs active task markers in the local trace file.
