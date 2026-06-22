# Feature Impact Analysis

This document prioritizes proposed board features by mapping them directly to the driving forces of our human and agent personas.

---

## Feature Impact Grid

| Feature | Targeted Persona | Driving Force Addressed | Priority | Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Flat-file state sync** | Human & Agent | Eliminates database setup / Ensures version control compatibility | Critical | **High**: Syncs state with code history. |
| **CLI command copy box** | Human (Martin) | Resolves handoff friction by removing manual command construction | High | **Medium**: Saves clicks/keystrokes. |
| **Checkbox checklist updates** | Human & Agent | Provides clear checklists of subtasks to track story completeness | High | **High**: Prevents agent execution drift. |
| **HUD active story badge** | Human (Martin) | Prevents obscurity by giving visual cues of the currently pinned task | Medium | **Medium**: Keeps developer oriented. |
| **Strict YAML parser validation** | Agent | Prevents agent crashes from formatting irregularities in YAML status | Critical | **High**: Guards server stability. |

---

## 1. High Impact Features

### Flat-File State Sync (`sprint-status.yaml`)
- **Rationale**: Storing status in YAML files makes the board portable and revision-tracked. 
- **Trigger Met**: satisfying the developer's need for local control and the agent's need to read state directly from files.

### CLI Command Copy Box
- **Rationale**: Clicking a story card exposes an input field showing the exact `dev this story [story-key]` command.
- **Trigger Met**: Resolves handoff friction by giving the developer a one-click copy path.

---

## 2. Risk Mitigation

### YAML Parser Robustness
- **Rationale**: Since the python backend parses YAML manually using line splitting and simple colon detection, the formatting is sensitive. We must enforce strict spacing trims and skip empty lines or inline comments to keep the parser robust without pulling in third-party libraries.
