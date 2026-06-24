# Story 2.3: one-command-installer-skill

Status: ready-for-dev

## Story

As a developer using the bmad-method,
I want a simple installable skill or script that registers the dashboard skill into my workspace,
so that I can install the project board using a single command.

## Acceptance Criteria

1. Implement the install/onboarding script that can copy the server code, static assets, and the `bmad-sprint-status-ui` skill folder to the user's local workspace.
2. The installation payload must map resources into the target project's `.agents/skills/bmad-sprint-status-ui` directory.
3. Make sure the installer does not require any external package dependencies.

## Tasks / Subtasks

- [ ] Structure the plugin skill directory containing the script, static assets, and `SKILL.md` (AC: 1, 2)
- [ ] Create/configure the installer script (AC: 1)
- [ ] Verify that running the installer script copies the board skill into a new project cleanly (AC: 3)

## Dev Notes

- Re-running the installation command must safely update files without wiping out user changes or local sprint metadata.

## Dev Agent Record

### Agent Model Used

Gemini 1.5 Pro

### Debug Log References

### Completion Notes List

### File List
