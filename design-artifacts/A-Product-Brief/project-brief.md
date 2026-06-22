# Project Brief: bmad-method-project-board

> Complete Strategic Foundation

**Created:** 2026-06-22
**Author:** Martin
**Brief Type:** Complete

---

## Vision

A local-first, zero-dependency, git-native project board bridging human developers and local AI agents to coordinate development sprints, manage stories, and track active tasks without leaving the local workspace.

---

## Positioning Statement

For developers collaborating with local AI agents who need a frictionless, revision-controlled Kanban board that is easily machine-readable and requires no external server or database setup.

**Breakdown:**

- **Target Customer:** Solo developers or small teams utilizing agentic workflows (e.g. Gemini, Antigravity) for project implementation.
- **Need/Opportunity:** Heavy cloud-based project management tools are detached from the local development loop and hard for local AI agents to interface with.
- **Category:** Local-first Agile Project Management Tool / Agent Console.
- **Key Benefit:** Keeps sprint statuses version-controlled directly inside the Git repository with markdown story files.
- **Differentiator:** Zero-dependency Python server with local flat-file configuration (YAML and txt) and auto-scaffolding of story specifications.

---

## Business Model

**Type:** Open Source, Personal Productivity Tool.

---

## Ideal Customer Profile (ICP)

Developer or engineer working with agentic coding assistants in local workspaces.

### Secondary Users

AI agents executing sprint plan tasks autonomously by reading/writing state files directly in the filesystem.

---

## Success Criteria

- 100% local operation without network dependencies.
- Instantaneous file updates and directory synchronizations.
- Clear, unambiguous state transitions for AI agent execution loops.
- Negligible system overhead during development sprints.

---

## Competitive Landscape

Traditional cloud project managers (Jira, Linear) are heavy, require browser-auth, and have no direct local file hooks. Raw text todo lists are lightweight but lack columns and visual structure.

### Our Unfair Advantage

Git-native structure where the project management state is checked into the same branch as the code itself, ensuring historical alignment between code commits and project tracking.

---

## Constraints

- Zero external Python library dependencies (must use standard library only).
- Zero database engines (must persist strictly in flat files like YAML/txt/MD).
- Standard browser compatibility for HTML/JS/CSS client.

---

## Platform & Device Strategy

**Primary Platform:** macOS / Linux

**Supported Devices:**
Desktop (Web browser)

**Device Priority:** Desktop Web

**Interaction Models:**
Web GUI (Drag & Drop, checklists) and Terminal CLI.

**Technical Requirements:**
- **Offline Functionality:** 100% offline local loop.
- **Native Features:** Local filesystem read/write.

**Platform Rationale:**
Running the server as a local background daemon ensures direct filesystem access to local project files and configuration boundaries.

**Future Platform Plans:**
Global CLI tool installer integration.

**Design Implications:**
High contrast, developer HUD aesthetic (dark mode, glassmorphism).

**Development Implications:**
Plain JS/HTML frontend, single Python backend script.

---

## Tone of Voice

**For UI Microcopy & System Messages**

### Tone Attributes

1. **Functional**: Clear, direct, no jargon or marketing copy.
2. **Precise**: Explicit status codes and console messaging.
3. **Professional**: Serious developer HUD tool.

### Examples

**Error Messages:**
- ✅ `[FSM] Blocked transition: backlog -> in-progress`
- ❌ `Oops! You can't drag that there!`

**Button Text:**
- ✅ `Reload`
- ❌ `Refresh the board`

**Empty States:**
- ✅ `Select a story card to inspect tasks`
- ❌ `No tasks here yet!`

**Success Messages:**
- ✅ `HEALTHY`
- ❌ `Everything is awesome!`

### Guidelines

**Do:**
- Use exact console formatting tags.
- State explicit status transitions.
- Keep label copy short.

**Don't:**
- Avoid friendly but vague error messages.
- Avoid conversational system modals.

---

*Note: Tone of Voice applies to UI microcopy (labels, buttons, errors, system messages). Strategic content (headlines, feature descriptions, value propositions) uses the Content Creation Workshop based on page-specific purpose and context.*

---

## Additional Context

None.

---

## Business Context

- **Primary Goal:** Provide a friction-free visual console for agentic developers.
- **Solution:** Flat-file, python-based local Kanban dashboard.
- **Target Users:** Humans and AI agents collaborating in a local workspace.

*Full strategic analysis (business goals, personas, driving forces) is developed in [Phase 2: Trigger Mapping](../B-Trigger-Map/).*

---

## Next Steps

This complete brief provides strategic foundation for all design work:

- [ ] **Phase 2: Trigger Mapping** - Map user psychology to business goals
- [ ] **Phase 3: PRD Platform** - Define technical foundation
- [ ] **Phase 4: UX Design** - Begin sketching and specifications
- [ ] **Phase 5: Design System** - If enabled, build components
- [ ] **Phase 6: PRD Finalization** - Compile for development handoff

---

_Generated by Whiteport Design Studio_
