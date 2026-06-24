# Story 2.1: onboarding-empty-state

Status: ready-for-dev

## Story

As a user first launching the project board in a fresh workspace,
I want the UI dashboard to display an actionable, beautiful empty state card,
so that I am guided on how to set up my first sprint/epic instead of seeing a blank screen.

## Acceptance Criteria

1. The frontend (`app.js` / `index.html`) must check if the retrieved Kanban board has no epics and no active stories.
2. When empty, replace the swimlanes and roadmap panels with a styled glassmorphic onboarding container.
3. The onboarding container must look professional, clean, and offer a step-by-step guide (e.g. step 1: run sprint planning; step 2: create epic; step 3: dev stories).
4. Do not show errors or crash the UI if no data is found.

## Tasks / Subtasks

- [ ] Add empty-state detection logic in `app.js` (AC: 1)
- [ ] Design and implement the empty-state UI component in `index.html` (AC: 2, 3)
- [ ] Verify UI behaves correctly when status endpoints return empty states (AC: 4)

## Dev Notes

- Make sure to match the existing dark mode/glassmorphism design theme.
- The step-by-step instructions should be clear and encourage starting immediately.

## Dev Agent Record

### Agent Model Used

Gemini 1.5 Pro

### Debug Log References

### Completion Notes List

### File List
