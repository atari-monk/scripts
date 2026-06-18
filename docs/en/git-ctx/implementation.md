## File: scripts/python/git_ctx.py

```python
#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

def run_git_command(repo_path: Path, args: List[str]) -> Tuple[int, str, str]:
    proc = subprocess.Popen(
        ["git"] + args,
        cwd=str(repo_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = proc.communicate()
    return proc.returncode, stdout.strip(), stderr.strip()

def is_git_repository(path: Path) -> bool:
    code, _, _ = run_git_command(path, ["rev-parse", "--git-dir"])
    return code == 0

def get_staged_changes(repo_path: Path) -> Dict[str, str]:
    code, output, _ = run_git_command(repo_path, ["diff", "--cached", "--name-status"])
    if code != 0 or not output:
        return {}
    
    changes: Dict[str, str] = {}
    for line in output.split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            status: str = parts[0]
            filepath: str = parts[1]
            status_map: Dict[str, str] = {
                "A": "Added",
                "M": "Modified",
                "D": "Deleted",
                "R": "Renamed",
                "C": "Copied"
            }
            change_type: str = status_map.get(status[0], status)
            changes[filepath] = change_type
    return changes

def get_unstaged_changes(repo_path: Path) -> Dict[str, str]:
    code, output, _ = run_git_command(repo_path, ["diff", "--name-status"])
    if code != 0 or not output:
        return {}
    
    changes: Dict[str, str] = {}
    for line in output.split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            status: str = parts[0]
            filepath: str = parts[1]
            status_map: Dict[str, str] = {
                "M": "Modified",
                "D": "Deleted",
            }
            change_type: str = status_map.get(status[0], status)
            changes[filepath] = change_type
    return changes

def get_untracked_files(repo_path: Path) -> List[str]:
    code, output, _ = run_git_command(repo_path, ["ls-files", "--others", "--exclude-standard"])
    if code != 0 or not output:
        return []
    return output.split("\n")

def generate_markdown(description: str, staged: Dict[str, str], unstaged: Dict[str, str], untracked: List[str]) -> str:
    lines: List[str] = ["# Git Changes Context", "", f"**Description:** {description}", "", "## Staged Changes", ""]
    
    if staged:
        for filepath, change_type in staged.items():
            lines.append(f"- **{change_type}**: `{filepath}`")
    else:
        lines.append("*No staged changes*")
    
    lines.extend(["", "## Unstaged Changes", ""])
    
    all_unstaged: Dict[str, str] = {**unstaged}
    for filepath in untracked:
        all_unstaged[filepath] = "Untracked"
    
    if all_unstaged:
        for filepath, change_type in all_unstaged.items():
            lines.append(f"- **{change_type}**: `{filepath}`")
    else:
        lines.append("*No unstaged changes*")
    
    lines.append("")
    return "\n".join(lines)

def write_to_file(project_path: Path, content: str) -> None:
    config_dir: Path = project_path / ".config"
    config_dir.mkdir(exist_ok=True)
    
    output_file: Path = config_dir / "_git-changes-context.md"
    output_file.write_text(content)
    print(f"Summary written to: {output_file}")

def copy_to_clipboard(content: str) -> bool:
    try:
        proc = subprocess.Popen(
            ["xclip", "-selection", "clipboard"],
            stdin=subprocess.PIPE,
            text=True
        )
        proc.communicate(input=content)
        return proc.returncode == 0
    except FileNotFoundError:
        return False

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Git change summary for commit context"
    )
    parser.add_argument(
        "project_path",
        help="Path to the target Git repository"
    )
    parser.add_argument(
        "description",
        help="Description of the changes"
    )
    
    args = parser.parse_args()
    
    project_path: Path = Path(args.project_path).resolve()
    
    if not project_path.exists():
        print(f"Error: Path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)
    
    if not is_git_repository(project_path):
        print(f"Error: Not a Git repository: {project_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        staged_changes: Dict[str, str] = get_staged_changes(project_path)
        unstaged_changes: Dict[str, str] = get_unstaged_changes(project_path)
        untracked_files: List[str] = get_untracked_files(project_path)
        
        summary: str = generate_markdown(
            args.description,
            staged_changes,
            unstaged_changes,
            untracked_files
        )
        
        write_to_file(project_path, summary)
        
        if copy_to_clipboard(summary):
            print("Summary copied to clipboard")
        else:
            print("Warning: xclip not found. Install with: sudo apt install xclip", file=sys.stderr)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```