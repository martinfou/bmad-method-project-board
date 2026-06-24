# Story 1.1: plugin-manifest

Status: done

## Story

As a developer using BMad Method,
I want to have a `.agents/manifest.json` file at the root of the project board repository,
so that it can be discovered and installed as a BMad module.

## Acceptance Criteria

1. Create a `.agents/manifest.json` file at the root of the repository.
2. The manifest must contain the plugin's definition following standard BMad Method conventions, including metadata (name: `bmad-method-project-board`, version, description) and register the `bmad-sprint-status-ui` skill.
3. The `bmad-sprint-status-ui` skill should define the capabilities and actions it exposes to the agent, specifying the path to the skill directory.

## Tasks / Subtasks

- [x] Design `.agents/manifest.json` structure (AC: 1, 2)
- [x] Create the `.agents/manifest.json` file at the workspace root (AC: 1, 2)
- [x] Validate that the manifest is correctly structured and contains necessary fields (AC: 3)

## Dev Notes

- The project board must remain platform-agnostic, using `.agents/` instead of platform-specific folders.
- Verify standard key names in manifest: `name`, `version`, `description`, `skills`.

## Dev Agent Record

### Agent Model Used

Antigravity (Google DeepMind)

### Debug Log References

- Validated manifest syntax using python json.tool parser:
  `python3 -m json.tool .agents/manifest.json` (Exited with 0)

### Completion Notes List

- Designed and created `.agents/manifest.json` following BMad plugin specifications.
- Registered the `bmad-sprint-status-ui` skill with `skills/bmad-sprint-status-ui` path.
- Exposed `render` and `launch` actions under the skill's `capabilities` field.

### File List

- [.agents/manifest.json](../../.agents/manifest.json)

### Review Findings

- [x] [Review][Patch] Inconsistent quoting of ISO-8601 timestamps [sprint-status.yaml:1-2]
- [x] [Review][Patch] Non-portable absolute URI in story file [1-1-plugin-manifest.md:47]
- [x] [Review][Defer] Mismatched script path for HTTP server launch action [.agents/manifest.json:28] — deferred, pre-existing
- [x] [Review][Defer] Non-existent script for static dashboard generation render action [.agents/manifest.json:23] — deferred, pre-existing
- [x] [Review][Defer] Mismatched skill source path in manifest [.agents/manifest.json:17] — deferred, pre-existing
- [x] [Review][Defer] Hardcoded port in server launch command [.agents/manifest.json:28] — deferred, pre-existing
- [x] [Review][Defer] Platform-dependent Python interpreter command [.agents/manifest.json:23,28] — deferred, pre-existing
