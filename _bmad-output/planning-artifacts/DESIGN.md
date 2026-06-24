---
status: final
updated: 2026-06-23
---

# DESIGN.md: Visual Design Specifications

This document outlines the visual identity, tokens, and style guidelines for the BMad Method Project Board.

## 1. Brand & Style
The Project Board uses a professional **Developer HUD (Heads-Up Display)** aesthetic. It is optimized for high readability, visual focus during coding, and direct visual feedback on sprint progress.

*   **Theme**: Cyberpunk-adjacent dark theme leveraging Neo-Mint and Teal accents on a deep Slate/Void background.
*   **Aesthetic Principle**: Glassmorphism (semi-transparent overlays with background blur) to create layering, depth, and spatial organization.

## 2. Colors

## Foundation Colors
*   **Workspace Background**: `#0b0e14` (Deep black-blue)
*   **Panes & Containers**: `#151b26` (Slate grey, typically overlayed with opacity)
*   **Border Accents**: `rgba(255, 255, 255, 0.05)` (Subtle white borders)

### Cyberpunk Neo-Mint & Teal Accents
*   **Cyber-Teal (Accent/Progress)**: `#00bbf9` (Primary brand accent, used for active selections, progress rings, and highlights)
*   **Neo-Mint (Highlights/Done)**: `#00f5d4` (Used for success indicators, logo accents, and complete states)
*   **Warm Orange (In Progress)**: `#fb8500` (Active work items)
*   **Electric Gold (Warning/Blocked)**: `#fee440` (Stalled or blocked states)
*   **Neon Pink/Rose (Active Pin/Danger)**: `#f15bb5` (Active story pin glow, thumbtacks, and critical actions)


## 3. Typography
*   **UI Controls & Headings**: `Inter` (Sans-serif)
    *   Weights: `300` (Light), `400` (Regular), `500` (Medium), `600` (Semi-Bold), `700` (Bold)
*   **Code & Metadata**: `JetBrains Mono` or `Fira Code` (Monospace)
    *   Used for file paths, commands, date tokens, and code boxes.

## 4. Layout & Spacing
*   **Structure**: Tri-pane flexible layout (`flex-row`) filling 100% viewport height.
    *   **Epic Pane**: Width `80` (fixed/collapsible), background `#0b0e14`.
    *   **Kanban Pane**: Flexible center area, background with Slate opacity.
    *   **Task Pane**: Width `96` (sliding drawer from right, overlaying workspace).
*   **Grid Spacing**: 4px grid (Tailwind spacing scales: `p-2` = 8px, `p-4` = 16px, `p-6` = 24px).

## 5. Shapes & Elevation
*   **Glass Containers**: `.glass` class applying:
    *   Background: `rgba(22, 27, 38, 0.6)`
    *   Backdrop Blur: `12px`
    *   Border: `1px solid rgba(255, 255, 255, 0.05)`
*   **Rounding**:
    *   Cards & Small Popups: `rounded-lg` (8px radius)
    *   Kanban Columns & Modal Containers: `rounded-xl` (12px radius)
    *   HUD Badges: `rounded-full` (capsule styling)

## 6. Components

### A. Sprint HUD Panel
*   Center-aligned navigation panel featuring:
    *   Running icon (`fa-running`) colored in Cyber-Teal.
    *   Sprint Name in white.
    *   Timeframe range in monospace slate-400.
    *   Dynamic capsule badges (Indigo/Teal for active days, Gold for ends today, Pink/Rose for overdue).

### B. Story Cards
*   **Default State**: Glass card with subtle border, grey title, metadata footers (tasks done/total).
*   **Active/Pinned State**: Border styled with `.pinned-glow` applying `box-shadow` of `rgba(241, 91, 181, 0.25)` (Neon Pink) and border color `rgba(241, 91, 181, 0.4)` (Neon Pink). Contains a Neon Pink thumbtack icon.
*   **Blocked State**: Highlighted card with an Electric Gold dashed border or warning state.

### C. PRD Modal Overlay
*   Overlay background: `bg-black/60` with background blur.
*   Modal body: Max-width 4xl, h-[85vh], scrolling container with prose typography, code syntax highlights (`text-cyan-400` or `text-teal-400` inside monospace code blocks).

