---
status: final
updated: 2026-06-23
---

# EXPERIENCE.md: Interaction & UX Specifications

This document outlines the information architecture, behaviors, user states, and key interactive flows for the BMad Method Project Board.

## 1. Foundation
*   **Platform**: Desktop Web Client.
*   **Operating Context**: Run as a local server background process with direct local filesystem read/write permissions. Fits into developer workflows alongside editors and terminals.
*   **Visual System Reference**: Stylings and tokens are defined in [DESIGN.md](file:///Volumes/T7/src/bmad-method-project-board/_bmad-output/planning-artifacts/DESIGN.md).

## 2. Information Architecture

```
[HUD / Top Navbar] -> Pinned Story ID, Health State, Completion Progress Ring, Reload, PRD Modal Open
[Workspace Area (Tri-Pane)]
  ├── [Left Pane: Epic Roadmap] -> List of Epics & Overall completion percentage per Epic
  ├── [Center Pane: Kanban Board] -> Six Swimlanes (Backlog, Ready for Dev, In Progress, Blocked, Review, Done)
  └── [Right Pane: Task Inspector] -> Story Description, Checklist Checklist, Transition Control buttons
```

## 3. Voice and Tone
*   **UI Microcopy**: Functional, clear, and professional developer terminal style.
*   **Console Logging**: Precise transitions and states are logged in absolute formats (e.g. `[FSM] Transition: backlog -> ready-for-dev`).
*   **State Information**: Explicit labels (e.g. "Select a story card to inspect tasks", "No active story pinned").

## 4. State Patterns

### Pinned / Active Story
*   **Purpose**: Tracks which story is currently active in the workspace, syncing with terminal agents.
*   **Persistence**: Pinned story key is written to `last-active-story.txt` in the root workspace.
*   **Exclusivity**: Only one story can be pinned at any time. Pinning a new story immediately unpins the previous one.
*   **Behavior**: When a story is promoted to "In Progress", it is automatically pinned. Clicking the pin icon on any card manually toggles the pin state.

### Drag & Drop Transitions
*   Dragging a card between columns triggers a state change validation in the backend Finite State Machine (FSM).
*   **Allowed Transitions**:
    *   `backlog` $\rightarrow$ `ready-for-dev`
    *   `ready-for-dev` $\rightarrow$ `in-progress` or `backlog`
    *   `in-progress` $\rightarrow$ `blocked`, `review`, or `ready-for-dev`
    *   `blocked` $\rightarrow$ `in-progress` or `ready-for-dev`
    *   `review` $\rightarrow$ `done` or `in-progress` (request changes)
    *   `done` $\rightarrow$ `in-progress`
*   **Invalid Actions**: If a user drags a card to an invalid column (e.g. dragging directly from `backlog` to `done`), the drag is cancelled, the card returns to its column, and a warning is logged: `[FSM] Blocked transition: backlog -> done`.

### Just-in-Time Story Scaffolding
*   When a story transitions to `ready-for-dev` (whether via drag-and-drop or navbar transition button), the server checks if the story file (e.g., `_bmad-output/implementation-artifacts/1-1-plugin-manifest.md`) exists.
*   If not found, it scaffolds a template file pre-populated with description and default tasks.

## 5. Interaction Primitives

### Click story card:
*   Opens the **Task Inspector** sliding pane from the right.
*   Highlights the selected card.

### Toggle task checkboxes:
*   Clicking a subtask checkbox in the inspector immediately sends a `POST /api/story/tasks` request to the backend.
*   The backend updates the task checkbox state (`[ ]` to `[x]`) in the story's markdown file, recalculates the task count, and refreshes the HUD progress ring.

### View PRD Modal:
*   Clicking "PRD" in the navbar opens the Modal overlay.
*   Content is fetched from `GET /api/prd`.
*   Users can close the modal by clicking the "X" button or pressing the `Esc` key.

## 6. Key Flows

### Flow A: Developer Begins Sprint
1. Developer opens dashboard in browser.
2. The HUD loads sprint goal, timeframe, and remaining days.
3. The board shows stories organized by column. If the workspace is empty, it renders the Empty State onboarding card.

### Flow B: Starting Development
1. Developer clicks a card in `Ready for Dev` lane.
2. In the Task Inspector, developer clicks "Start Development" (or drags the card to the "In Progress" column).
3. The story moves to "In Progress", is automatically pinned, and `last-active-story.txt` is updated.
4. The navbar badge updates to show the active pinned story ID.

### Flow C: Reviewing PRD Specs
1. Developer is writing code and needs to check the core design brief.
2. Developer clicks "PRD" in the top navbar.
3. The glassmorphic modal overlays the screen, displaying the parsed markdown content of the Product Brief.
4. Developer reviews the parameters, then presses `Esc` to close the modal and resume work.
