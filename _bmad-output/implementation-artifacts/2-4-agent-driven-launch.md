# Story 2.4: agent-driven-launch

Status: ready-for-dev

## Story

As a developer chatting with an agent,
I want the agent to automatically launch the project board when I request to open it,
so that I don't have to manually start the server or find the URL.

## Acceptance Criteria

1. Implement the trigger/intent mapping inside the `bmad-sprint-status-ui` skill so that the agent responds to "open project board", "start dashboard", or similar intents.
2. The skill must describe how to run the background server process on an available port starting at `8010` (scanning ports to avoid collision).
3. The skill must instruct the agent to launch the browser or show the clickable URL to the user.

## Tasks / Subtasks

- [ ] Add trigger terms and action steps inside the `bmad-sprint-status-ui/SKILL.md` (AC: 1, 2)
- [ ] Implement port scanning and start scripts to cleanly run the server (AC: 2, 3)
- [ ] Validate launcher behavior by asking the agent to open the project board (AC: 1)

## Dev Notes

- Ensure the port scan handles address-in-use errors gracefully by incrementing the port value from 8010.

## Dev Agent Record

### Agent Model Used

Gemini 1.5 Pro

### Debug Log References

### Completion Notes List

### File List
