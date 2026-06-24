# Story 1.5: prd-viewer

Status: ready-for-dev

## Story

As a developer using the project board,
I want a dedicated button in the interface to view the project's PRD (or Product Brief),
so that I can easily refer to requirements and goals while managing tasks.

## Acceptance Criteria

1. Create a `GET /api/prd` endpoint in `project_board_server.py`.
2. The endpoint must search for the PRD or Product Brief file relative to the resolved workspace root, checking paths such as `_bmad-output/planning-artifacts/prd.md` or `design-artifacts/A-Product-Brief/project-brief.md`.
3. If no file is found, return a friendly JSON error payload (e.g. `{"filename": "Not Found", "content": "..."}`) rather than a server error.
4. Add a "PRD" button to the top navbar next to the "Reload" button in `index.html`.
5. When clicked, load the PRD content via the API and display it in a beautiful, styled modal overlay with glassmorphism styling.
6. Enhance the markdown formatter in `app.js` to correctly parse headers (`#`, `##`, `###`) so the PRD renders with correct styling hierarchy.

## Tasks / Subtasks

- [ ] Implement backend `get_prd_content()` and the `/api/prd` route in `project_board_server.py` (AC: 1, 2, 3)
- [ ] Add navbar button and modal markup in `index.html` (AC: 4, 5)
- [ ] Implement modal popup logic and enhance markdown formatting in `app.js` (AC: 5, 6)
- [ ] Verify PRD displays correctly in modal with accurate headers and spacing (AC: 5)

## Dev Notes

- Ensure the modal is keyboard accessible (can close on 'Esc') and behaves cleanly on desktop.
- Markdown headers should have custom styles to contrast cleanly against the background.

## Dev Agent Record

### Agent Model Used

Gemini 1.5 Pro

### Debug Log References

### Completion Notes List

### File List
