#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

def main():
    if sys.version_info < (3, 6):
        print("Error: This script requires Python 3.6 or higher.", file=sys.stderr)
        sys.exit(1)
        
    if len(sys.argv) < 2:
        print("Usage: python3 install.py <target_project_path>")
        sys.exit(1)
        
    target_path = Path(sys.argv[1]).resolve()
    if not target_path.exists() or not target_path.is_dir():
        print(f"Error: Target path '{target_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)
        
    source_dir = Path(__file__).resolve().parent
    
    if not (source_dir / "project_board_server.py").exists() or not (source_dir / "project_board_static").is_dir():
        print("Error: Missing source files (project_board_server.py or project_board_static/).", file=sys.stderr)
        sys.exit(1)
        
    skill_dir = target_path / ".agents" / "skills" / "bmad-sprint-status-ui"
    
    print(f"Installing bmad-sprint-status-ui to {skill_dir}...")
    
    def safe_copy(src, dst):
        if dst.exists():
            backup = dst.with_name(dst.name + ".bak")
            shutil.copy2(dst, backup)
            print(f"Backed up {dst.name} to {backup.name}")
        shutil.copy2(src, dst)
        
    try:
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy server safely
        safe_copy(source_dir / "project_board_server.py", skill_dir / "project_board_server.py")
        
        # Copy static assets safely
        static_dest = skill_dir / "project_board_static"
        static_dest.mkdir(exist_ok=True)
        source_static = source_dir / "project_board_static"
        for item in source_static.iterdir():
            if item.is_file():
                safe_copy(item, static_dest / item.name)
        
        # Create SKILL.md safely
        source_skill_md = source_dir / "SKILL.md"
        dest_skill_md = skill_dir / "SKILL.md"
        if source_skill_md.exists():
            safe_copy(source_skill_md, dest_skill_md)
        elif not dest_skill_md.exists():
            with open(skill_dir / "SKILL.md", "w", encoding="utf-8") as f:
                f.write("""---
name: bmad-sprint-status-ui
description: Generate a rich visual Markdown dashboard or launch the interactive, web-based BMad local project board.
---

# BMad Sprint Status UI

Run the local server to view the project board:
```bash
python3 .agents/skills/bmad-sprint-status-ui/project_board_server.py
```

## Description
This skill provides a full UI dashboard to view and manage Epics and Stories using the BMad Method.

## Agent Instructions (Launch Intent)
When the user asks to "open project board", "start dashboard", or "view board":
1. Execute the server script (`.agents/skills/bmad-sprint-status-ui/project_board_server.py`) as a background task. The server automatically scans for an open port starting at `8010` and handles collisions gracefully.
2. Read the console output from the background task to identify which port the server actually bound to (e.g., "running on http://localhost:8010").
3. Respond to the user with a clickable markdown link to that specific URL (e.g. `[Open Dashboard](http://localhost:8010)`).
4. Do not attempt to use terminal commands to open the browser unless explicitly requested. Provide the URL and allow the user to click it.
""")
                
        print("Installation complete!")
    except Exception as e:
        print(f"Error during installation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
