# API Contracts

This document specifies the REST API endpoints exposed by the BMAD Method Project Board server (`project_board_server.py`).

---

## Endpoints

### 1. `GET /api/board`
- **Description**: Returns all board data, including sprint metadata, epics roadmap, and stories checklist.
- **Request Headers**: None
- **Query Parameters**: None
- **Response Status**: `200 OK`
- **Response Body** (`application/json`):
  ```json
  {
    "metadata": {
      "project_name": "bmad-method-project-board",
      "communication_language": "English"
    },
    "epics": [
      {
        "key": "epic-desktop-gui",
        "name": "Epic Desktop GUI",
        "status": "in-progress",
        "stories_total": 5,
        "stories_done": 2
      }
    ],
    "stories": [
      {
        "key": "dg-1-setup",
        "epic": "epic-desktop-gui",
        "status": "in-progress",
        "title": "Setup GUI Layout",
        "tasks_total": 4,
        "tasks_done": 1,
        "file_exists": true,
        "stalled": false,
        "blockers": []
      }
    ]
  }
  ```

### 2. `GET /api/story`
- **Description**: Returns detailed tasks and markdown content for a specific story file.
- **Request Headers**: None
- **Query Parameters**:
  - `id` (string, required): The story key (e.g. `dg-1-setup`)
- **Response Status**: `200 OK`
- **Response Body** (`application/json`):
  ```json
  {
    "key": "dg-1-setup",
    "title": "Setup GUI Layout",
    "story_text": "As a developer...",
    "ac_text": "AC1...",
    "notes_text": "...",
    "tasks": [
      {
        "line_no": 24,
        "text": "Core Implementation",
        "done": false
      }
    ]
  }
  ```

### 3. `GET /api/epic`
- **Description**: Extracts the title and details of an epic from the planning documents.
- **Request Headers**: None
- **Query Parameters**:
  - `id` (string, required): The epic key (e.g. `epic-desktop-gui`)
- **Response Status**: `200 OK`
- **Response Body** (`application/json`):
  ```json
  {
    "key": "epic-desktop-gui",
    "title": "Epic Desktop GUI",
    "description": "Epic description markdown content..."
  }
  ```

### 4. `GET /api/story/active`
- **Description**: Retrieves the active story key currently pinned in the workspace.
- **Request Headers**: None
- **Query Parameters**: None
- **Response Status**: `200 OK`
- **Response Body** (`application/json`):
  ```json
  {
    "active_story_key": "dg-1-setup"
  }
  ```

### 5. `POST /api/story/status`
- **Description**: Transitions the state of a story and triggers scaffolding if set to `ready-for-dev`.
- **Request Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "key": "dg-1-setup",
    "status": "in-progress"
  }
  ```
- **Response Status**: `200 OK` or `400 Bad Request` (on illegal transitions)
- **Response Body**:
  ```json
  {
    "success": true
  }
  ```

### 6. `POST /api/story/active`
- **Description**: Pins or unpins a story key as the active workspace task.
- **Request Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "key": "dg-1-setup"
  }
  ```
- **Response Status**: `200 OK`
- **Response Body**:
  ```json
  {
    "success": true
  }
  ```

### 7. `POST /api/story/tasks`
- **Description**: Updates the check/uncheck status of task items directly in the story markdown file.
- **Request Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "key": "dg-1-setup",
    "tasks": [
      {
        "line_no": 24,
        "done": true
      }
    ]
  }
  ```
- **Response Status**: `200 OK`
- **Response Body**:
  ```json
  {
    "success": true
  }
  ```

### 8. `POST /api/story/create`
- **Description**: Scaffolds a new story markdown file with standardized metadata, ACs, and subtask checkpoints.
- **Request Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "key": "dg-1-setup",
    "overwrite": false
  }
  ```
- **Response Status**: `200 OK`
- **Response Body**:
  ```json
  {
    "success": true
  }
  ```
