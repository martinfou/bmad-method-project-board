---
stepsCompleted:
  - "requirements_extraction"
inputDocuments:
  - "docs/architecture.md"
  - "design-artifacts/A-Product-Brief/project-brief.md"
  - "User Request (Installation Flow Spec)"
---

# bmad-method-project-board - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for the **Easy Dashboard Installation & Setup** feature. The goal is to provide a frictionless, single-command installation experience for developers to bootstrap the project board UI in any fresh BMad Method project workspace.

## Requirements Inventory

### Functional Requirements

FR1: **One-Command Installation**: The developer must be able to install the project board using a single command from their terminal (e.g. `npx bmad-method install --custom-source github:martinfou/bmad-method-project-board`).
FR2: **Automated Skill Registration**: The installer must dynamically copy and register the `bmad-sprint-status-ui` skill into the target project's local `.agents/skills/` directory.
FR3: **Zero-State Stubbing**: If the target project has no existing BMad files, the installer must automatically stub out sample/template epics and stories (e.g., creating a sample `sprint-status.yaml` and planning directory) so the board boots with interactive example data instead of a blank or crashed screen.
FR4: **Dynamic Project-Root Resolution**: The server script must auto-detect the project root by walking up to find `.agents/` or `project-context.md` (Option 2), fallback to current working directory, or accept an override CLI flag.
FR5: **Interactive Launch Command**: The installed skill must register a simple chat intent (e.g. "open project board") so the developer's agent can run the server and open the browser window automatically, eliminating manual terminal commands.

### NonFunctional Requirements

NFR1: **Zero-Dependency Core**: The installation payload (server and API) must use only the Python standard library, requiring no pip or npm installations on the target machine.
NFR2: **Port Collision Avoidance**: The server must scan for available ports starting at `8010` to avoid address-in-use errors.
NFR3: **Idempotent Setup**: Re-running the installation command must safely update the skill and template files without wiping out the target project's existing sprint metadata or user stories.

### Additional Requirements

AR1: Provide a `.agents/manifest.json` manifest at the repository root to allow seamless discovery by the BMad plugin system.
AR2: Include a clean README showing the one-liner command and how to ask the agent to launch the board.

### UX Design Requirements

UX-DR1: **Onboarding Empty State**: The frontend dashboard must detect if there are no active stories or epics and display a beautiful, actionable empty state card with a step-by-step guide on how to create the first epic.

### FR Coverage Map

FR1: Epic 2 - One-Command Installation
FR2: Epic 2 - Automated Skill Registration
FR3: Epic 2 - Zero-State Stubbing
FR4: Epic 1 - Dynamic Root Resolution
FR5: Epic 2 - Agent-Driven Launch
NFR1: Epic 1 - Zero-Dependency Constraint
NFR2: Epic 1 - Fault Tolerance
NFR3: Epic 2 - Idempotent Setup
UX-DR1: Epic 2 - Onboarding Empty State
AR1: Epic 1 - Marketplace Manifest
AR2: Epic 1 - Server Output Log

### Epic List

### Epic 1: Project Board Bootstrapping & Resolution Core
Package the project board codebase as an installable BMad module. Implement dynamic directory auto-resolution and an API status endpoint (`/api/status` returning initialization and root detection details). 
*   **Developer Value**: Enables developers to immediately run the server manually against any directory (`python3 project_board_server.py --project-root .`) and verify root resolution.
*   **FRs covered:** FR4, NFR1, NFR2, AR1, AR2

### Epic 2: Interactive First-Run Onboarding & Agent Launch
Implement the one-command installer skill, the agent-driven launch intent (`"open project board"`), and a guided interactive UI onboarding state that feeds sample stubs to the board if the target repository is empty.
*   **Developer Value**: Enables a seamless one-liner installation and automatically guides the user through setting up their first epic without landing on a blank page.
*   **FRs covered:** FR1, FR2, FR3, FR5, NFR3, UX-DR1
