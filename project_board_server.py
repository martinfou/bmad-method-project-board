#!/usr/bin/env python3
import os
import sys
import re
import json
import time
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

PORT = 8010
YAML_PATH = None
ARTIFACTS_DIR = None
PLANNING_DIR = None
PROJECT_ROOT = None
STATIC_DIR = Path(__file__).resolve().parent / "project_board_static"

ALLOWED_TRANSITIONS = {
    "backlog": ["ready-for-dev"],
    "ready-for-dev": ["in-progress", "backlog"],
    "in-progress": ["blocked", "review", "ready-for-dev"],
    "blocked": ["in-progress", "ready-for-dev"],
    "review": ["done", "in-progress"],
    "done": ["in-progress"]
}

def write_last_active_story(story_key):
    if YAML_PATH:
        target_path = YAML_PATH.parent.parent / "last-active-story.txt"
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = target_path.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(story_key)
            temp_path.replace(target_path)
        except Exception as e:
            sys.stderr.write(f"Error writing last active story trace: {e}\n")

def find_project_root(override_path=None):
    if override_path:
        p = Path(override_path).resolve()
        if not p.exists():
            sys.stderr.write(f"Error: Specified project root '{p}' does not exist.\n")
            sys.exit(1)
        if not p.is_dir():
            sys.stderr.write(f"Error: Specified project root '{p}' is not a directory.\n")
            sys.exit(1)
        return p

    # 1. Start check from directory of project_board_server.py
    script_dir = Path(__file__).resolve().parent
    try:
        cwd = Path(os.getcwd()).resolve()
    except Exception:
        cwd = script_dir
    
    # Helper to check if a directory has any of the markers with correct type checks
    def has_marker(p):
        try:
            if (p / ".agents").is_dir():
                return True
            if (p / "_bmad-output").is_dir():
                return True
            if (p / "project-context.md").is_file():
                return True
        except PermissionError:
            pass
        return False
        
    # Helper to walk up from a path
    def walk_up_find(start_path):
        curr = start_path
        while True:
            if has_marker(curr):
                return curr
            parent = curr.parent
            if parent == curr: # Reached filesystem root
                break
            curr = parent
        return None

    # Check from script dir first
    root = walk_up_find(script_dir)
    if root:
        return root
        
    # Check from CWD next
    if cwd != script_dir:
        root = walk_up_find(cwd)
        if root:
            return root
        
    # Fallback to CWD
    return cwd

def load_project_config(project_root):
    config_paths = [
        project_root / "_bmad" / "bmm" / "config.yaml",
        project_root / ".bmad" / "config.yaml"
    ]
    
    config = {}
    for path in config_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if ":" in line:
                            key, val = line.split(":", 1)
                            config[key.strip()] = val.strip().strip('"').strip("'")
                break
            except Exception as e:
                sys.stderr.write(f"Error reading config {path}: {e}\n")
    return config

def get_prd_content():
    global PLANNING_DIR, PROJECT_ROOT
    if not PROJECT_ROOT:
        return "PRD Not Configured", "Project root not resolved."
        
    # Standard check directories
    possible_paths = []
    if PLANNING_DIR:
        possible_paths.extend([
            PLANNING_DIR / "prd.md",
            PLANNING_DIR / "product-brief.md",
        ])
    possible_paths.append(PROJECT_ROOT / "design-artifacts" / "A-Product-Brief" / "project-brief.md")
    
    for path in possible_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return path.name, f.read()
            except Exception as e:
                sys.stderr.write(f"Error reading PRD path {path}: {e}\n")
                
    # Fallback to wildcard search in planning artifacts
    if PLANNING_DIR and PLANNING_DIR.exists():
        try:
            for p in sorted(PLANNING_DIR.glob("*prd*.md")):
                with open(p, "r", encoding="utf-8") as f:
                    return p.name, f.read()
            for p in sorted(PLANNING_DIR.glob("*brief*.md")):
                with open(p, "r", encoding="utf-8") as f:
                    return p.name, f.read()
        except PermissionError:
            pass
        except Exception as e:
            sys.stderr.write(f"Error searching PRD files: {e}\n")
            
    # Fallback to wildcard search in design-artifacts/A-Product-Brief
    brief_dir = PROJECT_ROOT / "design-artifacts" / "A-Product-Brief"
    if brief_dir.exists():
        try:
            for p in sorted(brief_dir.glob("*.md")):
                if "brief" in p.name.lower() or "prd" in p.name.lower():
                    with open(p, "r", encoding="utf-8") as f:
                        return p.name, f.read()
        except PermissionError:
            pass
        except Exception as e:
            sys.stderr.write(f"Error searching design brief files: {e}\n")
        
    return "PRD Not Found", "No PRD (`prd.md`) or Product Brief (`project-brief.md`) was found in the planning or design directories."

def normalize_to_tokens(text):
    if not text:
        return []
    cleaned = re.sub(r'[^a-z0-9]', ' ', text.lower())
    return [t for t in cleaned.split() if t]

def get_epic_details(epic_key):
    if not PLANNING_DIR or not PLANNING_DIR.exists():
        return epic_key, "Planning directory not found."
        
    title = epic_key.replace("epic-", "Epic ").title()
    description = ""
    
    # 1. Normalize key
    key_tokens = [t for t in normalize_to_tokens(epic_key) if t != 'epic']
    if not key_tokens:
        return title, "Invalid epic key."
        
    is_numeric = all(t.isdigit() for t in key_tokens)
    
    best_score = -1
    best_match_file = None
    best_match_heading = None
    best_match_content_start = -1
    
    # Track files where this epic is found for duplicate warnings
    matched_files = []
    
    # Sort files alphabetically to ensure deterministic order
    files = sorted(list(PLANNING_DIR.glob("*.md")))
    
    for p_file in files:
        try:
            with open(p_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Extract H1 text if any
            h1_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
            h1_text = h1_match.group(1).strip() if h1_match else ""
            
            # Find all H2/H3 headings
            headings = list(re.finditer(r"^(##|###)\s+(.*)$", content, re.MULTILINE))
            for h_match in headings:
                heading_text = h_match.group(2).strip()
                
                # Calculate match score
                score = 0
                heading_tokens = normalize_to_tokens(heading_text)
                file_tokens = normalize_to_tokens(p_file.name)
                h1_tokens = normalize_to_tokens(h1_text)
                
                if is_numeric:
                    number = key_tokens[0]
                    has_epic = any(t in heading_tokens for t in ['epic', 'epics'])
                    # We want exact number token match
                    has_number = number in heading_tokens
                    if has_number and has_epic:
                        score = 100
                    elif has_number:
                        score = 50
                else:
                    # Text-based matching
                    matched_count = 0
                    for token in key_tokens:
                        if token in heading_tokens:
                            score += 30
                            matched_count += 1
                        elif token in h1_tokens:
                            score += 15
                            matched_count += 1
                        elif token in file_tokens:
                            score += 10
                            matched_count += 1
                        else:
                            # Substring fallback
                            for ht in heading_tokens:
                                if token in ht or ht in token:
                                    score += 15
                                    matched_count += 1
                                    break
                            else:
                                for ft in file_tokens:
                                    if token in ft or ft in token:
                                        score += 5
                                        matched_count += 1
                                        break
                    if any(t in heading_tokens for t in ['epic', 'epics']):
                        score += 20
                    if matched_count == 0:
                        score = 0
                        
                if score > 0:
                    if score > best_score:
                        best_score = score
                        best_match_file = p_file
                        best_match_heading = heading_text
                        best_match_content_start = h_match.end()
                        matched_files = [p_file]
                    elif score == best_score:
                        matched_files.append(p_file)
                        
        except Exception as e:
            sys.stderr.write(f"Error reading {p_file}: {e}\n")
            
    # Resolve and get description from the best match
    if best_match_file and best_score > 0:
        # Check for duplicates in other files (with the same score)
        unique_matched_files = []
        for f in matched_files:
            if f not in unique_matched_files:
                unique_matched_files.append(f)
                
        if len(unique_matched_files) > 1:
            # First one alphabetically wins, which is best_match_file (since files are sorted)
            # Log warning about duplicates
            sys.stderr.write(f"[WARN] Duplicate Epic {epic_key} found in files: {[f.name for f in unique_matched_files]}. Falling back to {best_match_file.name}.\n")
            
        try:
            with open(best_match_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            title = best_match_heading
            # Find next heading to slice description
            next_heading = re.search(r"^(##|###)\s+", content[best_match_content_start:], re.MULTILINE)
            if next_heading:
                description = content[best_match_content_start:best_match_content_start + next_heading.start()].strip()
            else:
                description = content[best_match_content_start:].strip()
                
        except Exception as e:
            sys.stderr.write(f"Error reading matched file {best_match_file}: {e}\n")
            
    return title, description or "Details not found in planning files."

def parse_sprint_status():
    if not YAML_PATH.exists():
        return {}, {}
        
    metadata = {}
    development_status = {}
    in_dev_status = False
    
    with open(YAML_PATH, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            
            if stripped.startswith("development_status:"):
                in_dev_status = True
                continue
            
            if ":" not in stripped:
                continue
                
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            
            if not in_dev_status:
                metadata[key] = val
            else:
                development_status[key] = val
                
    return metadata, development_status

def update_yaml_status(story_key, new_status):
    if not YAML_PATH.exists():
        return False
        
    metadata, dev_status = parse_sprint_status()
    old_status = dev_status.get(story_key)
    if not old_status:
        return False
        
    # Validate transition
    if new_status not in ALLOWED_TRANSITIONS.get(old_status, []):
        sys.stderr.write(f"[FSM] Blocked transition: {old_status} -> {new_status} for {story_key}\n")
        return False
        
    with open(YAML_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    updated = False
    for i, line in enumerate(lines):
        match = re.match(r"^(\s*)" + re.escape(story_key) + r"\s*:\s*(.*)$", line)
        if match:
            indent = match.group(1)
            lines[i] = f"{indent}{story_key}: {new_status}\n"
            updated = True
            break
            
    if updated:
        # Also update last_updated in metadata
        for i, line in enumerate(lines):
            if line.startswith("last_updated:"):
                now_str = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                lines[i] = f"last_updated: \"{now_str}\"\n"
                break
                
        with open(YAML_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return True
    return False

def get_epic_for_story(story_key):
    if story_key.startswith("dg-"):
        return "epic-desktop-gui"
    if story_key.startswith("dci-"):
        return "epic-desktop-crossplatform-ci"
    if story_key.startswith("dbj-"):
        return "epic-desktop-bundle-java"
    
    match = re.match(r"^(\d+)-", story_key)
    if match:
        return f"epic-{match.group(1)}"
    return None

def scan_story_file(story_key, status):
    filepath = ARTIFACTS_DIR / f"{story_key}.md"
    title = story_key.replace("-", " ").title()
    tasks_total = 0
    tasks_done = 0
    stalled = False
    blockers = []
    file_exists = False
    
    if filepath.exists():
        file_exists = True
        mtime = os.path.getmtime(filepath)
        if status in ("in-progress", "review") and (time.time() - mtime > 48 * 3600):
            stalled = True
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Extract title (first h1)
            title_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                
            # Count checkboxes
            for line in content.splitlines():
                match = re.match(r"^(\s*)-\s*\[([ xX])\]\s*(.*)$", line)
                if match:
                    tasks_total += 1
                    if match.group(2).lower() == "x":
                        tasks_done += 1
                    else:
                        line_lower = line.lower()
                        if any(w in line_lower for w in ("block", "depend", "stuck")):
                            if "unblock" not in line_lower:
                                blockers.append(line.strip())
        except Exception:
            pass
            
    return file_exists, title, tasks_total, tasks_done, stalled, blockers

def get_story_tasks(story_key):
    filepath = ARTIFACTS_DIR / f"{story_key}.md"
    tasks = []
    title = story_key
    story_text = ""
    ac_text = ""
    notes_text = ""
    
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            title_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                
            sections = re.split(r"^##\s+", content, flags=re.MULTILINE)
            for sec in sections:
                lines = sec.splitlines()
                if not lines:
                    continue
                header = lines[0].strip().lower()
                body = "\n".join(lines[1:]).strip()
                
                if header.startswith("story"):
                    story_text = body
                elif header.startswith("acceptance criteria"):
                    ac_text = body
                elif header.startswith("dev notes") or header.startswith("notes"):
                    notes_text = body
                    
            lines = content.splitlines()
            for i, line in enumerate(lines):
                match = re.match(r"^(\s*)-\s*\[([ xX])\]\s*(.*)$", line)
                if match:
                    tasks.append({
                        "line_no": i,
                        "text": match.group(3).strip(),
                        "done": match.group(2).lower() == "x"
                    })
        except Exception as e:
            sys.stderr.write(f"Error reading story tasks: {e}\n")
            
    return title, tasks, story_text, ac_text, notes_text

def update_story_tasks(story_key, task_updates):
    filepath = ARTIFACTS_DIR / f"{story_key}.md"
    if not filepath.exists():
        return False
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for update in task_updates:
            line_no = int(update["line_no"])
            done = bool(update["done"])
            if 0 <= line_no < len(lines):
                line = lines[line_no]
                match = re.match(r"^(\s*)-\s*\[([ xX])\](.*)$", line)
                if match:
                    indent = match.group(1)
                    rem = match.group(3)
                    check = "x" if done else " "
                    lines[line_no] = f"{indent}- [{check}]{rem}\n"
                    
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return True
    except Exception as e:
        sys.stderr.write(f"Error updating story tasks: {e}\n")
        return False

def scaffold_story_file(story_key, overwrite=False):
    filepath = ARTIFACTS_DIR / f"{story_key}.md"
    if filepath.exists() and not overwrite:
        return True
        
    # Search for story description in planning epics files
    description = ""
    acceptance_criteria = []
    
    # Try finding inside any epic markdown file
    try:
        for p_file in PLANNING_DIR.glob("*.md"):
            with open(p_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Look for story heading e.g., "Story 16.13:" or "16-13"
            parts = story_key.split("-")
            if len(parts) >= 2:
                # Match e.g. "3.1" or "3-1" with word boundaries to avoid matching "13-01"
                pattern = r"(?i)(###?\s+.*\b" + re.escape(parts[0]) + r"[.-]" + re.escape(parts[1]) + r"\b.*?)(?=\n###?\s+|\Z)"
            else:
                pattern = r"(?i)(###?\s+.*\b" + re.escape(story_key) + r"\b.*?)(?=\n###?\s+|\Z)"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                section = match.group(1)
                description = section.strip()
                # Parse out list items as ACs
                for line in section.splitlines():
                    if line.strip().startswith("- ") or line.strip().startswith("* "):
                        acceptance_criteria.append(line.strip()[2:])
                break
    except Exception:
        pass
        
    if not description:
        description = f"As a developer, I want to implement the tasks associated with {story_key}."
        acceptance_criteria = ["Implement core functionality.", "Add unit tests.", "Verify implementation."]
        
    # Scaffold Template
    story_title = story_key.replace("-", " ").title()
    template = []
    template.append("---")
    template.append("baseline_commit: unknown")
    template.append("---")
    template.append(f"# Story: {story_title}\n")
    template.append("Status: ready-for-dev\n")
    template.append("## Story\n")
    template.append(description + "\n")
    template.append("## Acceptance Criteria\n")
    for i, ac in enumerate(acceptance_criteria):
        template.append(f"{i+1}. **AC{i+1} — Verification**:")
        template.append(f"   - [ ] {ac}")
    template.append("\n## Tasks / Subtasks\n")
    template.append("- [ ] Task 1: Core Implementation")
    template.append("- [ ] Task 2: Testing & Verification")
    
    try:
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(template) + "\n")
        return True
    except Exception as e:
        sys.stderr.write(f"Error scaffolding story file: {e}\n")
        return False

class ProjectBoardRequestHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
        
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path
        query = urllib.parse.parse_qs(url_parsed.query)
        
        # API Endpoints
        if path == "/api/board":
            try:
                metadata, dev_status = parse_sprint_status()
            except Exception as e:
                sys.stderr.write(f"Error parsing sprint status: {e}\n")
                metadata, dev_status = {}, {}
            
            epics = {}
            stories = []
            
            for key, val in dev_status.items():
                if key.startswith("epic-") and not key.endswith("-retrospective"):
                    epics[key] = {
                        "key": key,
                        "name": key.replace("epic-", "Epic "),
                        "status": val,
                        "stories_total": 0,
                        "stories_done": 0
                    }
            
            for key, val in dev_status.items():
                if not key.startswith("epic-") and not key.endswith("-retrospective"):
                    epic_key = get_epic_for_story(key)
                    file_exists, title, tasks_tot, tasks_dn, stalled, blockers = scan_story_file(key, val)
                    
                    stories.append({
                        "key": key,
                        "epic": epic_key,
                        "status": val,
                        "title": title,
                        "tasks_total": tasks_tot,
                        "tasks_done": tasks_dn,
                        "file_exists": file_exists,
                        "stalled": stalled,
                        "blockers": blockers
                    })
                    
                    if epic_key in epics:
                        epics[epic_key]["stories_total"] += 1
                        if val == "done":
                            epics[epic_key]["stories_done"] += 1
                            
            board_data = {
                "metadata": metadata,
                "epics": list(epics.values()),
                "stories": stories
            }
            self.send_json(board_data)
            return
            
        elif path == "/api/story":
            story_id = query.get("id", [None])[0]
            if not story_id:
                self.send_json({"error": "Missing story id"}, 400)
                return
                
            title, tasks, story_text, ac_text, notes_text = get_story_tasks(story_id)
            self.send_json({
                "key": story_id,
                "title": title,
                "story_text": story_text,
                "ac_text": ac_text,
                "notes_text": notes_text,
                "tasks": tasks
            })
            return
            
        elif path == "/api/epic":
            epic_id = query.get("id", [None])[0]
            if not epic_id:
                self.send_json({"error": "Missing epic id"}, 400)
                return
                
            title, description = get_epic_details(epic_id)
            self.send_json({
                "key": epic_id,
                "title": title,
                "description": description
            })
            return
            
        elif path == "/api/story/active":
            active_key = ""
            if YAML_PATH:
                target_path = YAML_PATH.parent.parent / "last-active-story.txt"
                if target_path.exists():
                    try:
                        with open(target_path, "r", encoding="utf-8") as f:
                            active_key = f.read().strip()
                    except Exception:
                        pass
            self.send_json({"active_story_key": active_key})
            return

        elif path == "/api/prd":
            filename, content = get_prd_content()
            self.send_json({
                "filename": filename,
                "content": content
            })
            return
            
        # Serve Static Files
        if path == "/" or path == "":
            file_to_serve = STATIC_DIR / "index.html"
            content_type = "text/html"
        else:
            filename = os.path.basename(path)
            file_to_serve = STATIC_DIR / filename
            if filename.endswith(".js"):
                content_type = "application/javascript"
            elif filename.endswith(".css"):
                content_type = "text/css"
            else:
                content_type = "text/plain"
                
        if file_to_serve.exists() and file_to_serve.is_file():
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            with open(file_to_serve, "rb") as sf:
                self.wfile.write(sf.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")

    def do_POST(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path
        
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode("utf-8"))
        except Exception:
            self.send_json({"error": "Invalid JSON payload"}, 400)
            return
            
        if path == "/api/story/status":
            story_key = data.get("key")
            new_status = data.get("status")
            
            if not story_key or not new_status:
                self.send_json({"error": "Missing key or status"}, 400)
                return
                
            success = update_yaml_status(story_key, new_status)
            if success:
                # Write active story trace when transitioning to in-progress
                if new_status == "in-progress":
                    write_last_active_story(story_key)
                # Just-in-Time Story Spec Generation
                if new_status == "ready-for-dev":
                    scaffold_story_file(story_key)
                self.send_json({"success": True})
            else:
                self.send_json({"error": f"Story {story_key} not found or invalid transition"}, 400)
                
        elif path == "/api/story/active":
            story_key = data.get("key")
            if story_key is None:
                self.send_json({"error": "Missing key"}, 400)
                return
            # Empty string implies unpinning
            write_last_active_story(story_key)
            self.send_json({"success": True})
            
        elif path == "/api/story/tasks":
            story_key = data.get("key")
            task_updates = data.get("tasks", [])
            
            if not story_key or not task_updates:
                self.send_json({"error": "Missing key or tasks"}, 400)
                return
                
            success = update_story_tasks(story_key, task_updates)
            if success:
                self.send_json({"success": True})
            else:
                self.send_json({"error": "Failed to update story tasks"}, 500)
                
        elif path == "/api/story/create":
            story_key = data.get("key")
            overwrite = data.get("overwrite", False)
            if not story_key:
                self.send_json({"error": "Missing key"}, 400)
                return
                
            success = scaffold_story_file(story_key, overwrite=overwrite)
            if success:
                self.send_json({"success": True})
            else:
                self.send_json({"error": "Failed to scaffold story"}, 500)
        else:
            self.send_response(404)
            self.end_headers()

def seed_templates():
    if not YAML_PATH.exists():
        try:
            ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
            import datetime
            now = datetime.datetime.now()
            end_date = now + datetime.timedelta(days=14)
            with open(YAML_PATH, "w", encoding="utf-8") as f:
                f.write(f"""project: "My BMAD Project"
project_key: "BMAD"
sprint_name: "Sprint 1: Foundation"
sprint_goal: "Set up the core architecture and basic authentication"
start_date: "{now.strftime('%Y-%m-%d')}"
end_date: "{end_date.strftime('%Y-%m-%d')}"
last_updated: "{now.strftime('%Y-%m-%dT%H:%M:%SZ')}"

development_status:
  epic-1: in-progress
  epic-2: backlog
  
  1-1: done
  1-2: in-progress
  1-3: ready-for-dev
  
  2-1: backlog
""")
            print("Seeded sprint-status.yaml template.")
        except Exception as e:
            sys.stderr.write(f"Error seeding sprint-status.yaml: {e}\n")
            
    epics_path = PLANNING_DIR / "epics.md"
    if not epics_path.exists():
        try:
            PLANNING_DIR.mkdir(parents=True, exist_ok=True)
            with open(epics_path, "w", encoding="utf-8") as f:
                f.write("""# Project Epics

## Epic 1: Scaffold Initial Architecture
Set up the core boilerplate, file structure, and CI pipelines for the project.

## Epic 2: Core User Authentication
Implement login, registration, and password recovery.
""")
            print("Seeded epics.md template.")
        except Exception as e:
            sys.stderr.write(f"Error seeding epics.md: {e}\n")

def main():
    global YAML_PATH, ARTIFACTS_DIR, PLANNING_DIR, PROJECT_ROOT
    import argparse
    
    parser = argparse.ArgumentParser(description="BMAD Method Project Board Server")
    parser.add_argument("--project-root", default=None, help="Path to project workspace root")
    parser.add_argument("--port", type=int, default=PORT, help="Port to run server on")
    args = parser.parse_args()
    
    if not (0 <= args.port <= 65535):
        parser.error("Port must be between 0 and 65535")
        
    project_root = find_project_root(args.project_root)
        
    PROJECT_ROOT = project_root
    
    config = load_project_config(project_root)
    impl_dir = config.get("implementation_artifacts_dir") or config.get("story_location") or "_bmad-output/implementation-artifacts"
    plan_dir = config.get("planning_artifacts_dir") or "_bmad-output/planning-artifacts"
    
    ARTIFACTS_DIR = project_root / impl_dir
    PLANNING_DIR = project_root / plan_dir
    YAML_PATH = ARTIFACTS_DIR / "sprint-status.yaml"
    
    seed_templates()
    
    port = args.port
    server = None
    while port < 65535:
        try:
            server = HTTPServer(("localhost", port), ProjectBoardRequestHandler)
            break
        except OSError as e:
            # Catch "Address already in use" (98 on Linux, 48 on macOS) or Permission Error (13)
            if e.errno in (98, 48, 13):
                port += 1
            else:
                raise
                
    if not server:
        sys.stderr.write("Could not bind to any port.\n")
        sys.exit(1)
        
    print(f"BMAD Method Project Board server running on http://localhost:{port} (Workspace: {project_root})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping BMAD Method Project Board server.")
        server.server_close()

if __name__ == "__main__":
    main()
