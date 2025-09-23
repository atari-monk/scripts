#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable, Set

try:
    import pyperclip
except ImportError:
    print("Error: pyperclip module is required. Please install it with: pip install pyperclip")
    sys.exit(1)

# File extension to language mapping
EXTENSION_MAP = {
    ".py": "python", ".js": "javascript", ".ts": "typescript", ".java": "java",
    ".kt": "kotlin", ".go": "go", ".rs": "rust", ".c": "c", ".cpp": "cpp",
    ".h": "c", ".hpp": "cpp", ".sh": "bash", ".html": "html", ".css": "css",
    ".scss": "scss", ".sql": "sql", ".md": "markdown", ".json": "json",
    ".yaml": "yaml", ".yml": "yaml", ".toml": "toml",
}

def get_language_from_extension(file_path: pathlib.Path) -> str:
    """Determine markdown language from file extension."""
    return EXTENSION_MAP.get(file_path.suffix.lower(), "text")

def should_ignore(path: pathlib.Path, ignore_dirs: Set[str], ignore_files: Set[str]) -> bool:
    """Check if path matches any ignore patterns."""
    if path.name in ignore_files:
        return True
    
    for part in path.parts:
        if part in ignore_dirs:
            return True
    
    return False

def should_process_file(file_path: pathlib.Path, max_size_mb: int = 10) -> bool:
    """Check if file should be processed based on size and other criteria."""
    try:
        return file_path.stat().st_size <= max_size_mb * 1024 * 1024
    except OSError:
        return False
    
def generate_markdown(
    root_dir: pathlib.Path,
    ignore_dirs: Iterable[str],
    ignore_files: Iterable[str],
) -> str:
    """Generate markdown content from directory contents."""
    ignore_dirs_set = set(ignore_dirs)
    ignore_files_set = set(ignore_files)
    
    markdown_parts: list[str] = []
    
    for file_path in root_dir.rglob("*"):
        if (file_path.is_file() and 
            not file_path.name.startswith(".") and 
            not should_ignore(file_path, ignore_dirs_set, ignore_files_set)) and should_process_file(file_path):
            
            language = get_language_from_extension(file_path)
            markdown_parts.append(f"\n{file_path}\n```{language}\n")
            
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    markdown_parts.append(f.read())
            except UnicodeDecodeError:
                # Skip binary files or files with encoding issues
                markdown_parts.append(f"# Binary or unreadable file: {file_path}\n")
            
            markdown_parts.append("\n```\n")
    
    return "".join(markdown_parts)

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    default_ignore_dirs = [".git", "__pycache__", "node_modules", "venv"]
    default_ignore_files = ["vite-env.d.ts", "tsconfig.json", "package.json"]
    
    parser = argparse.ArgumentParser(
        description="Generate a Markdown file containing code from all files in a directory and copy to clipboard."
    )
    parser.add_argument("directory", type=pathlib.Path, help="Directory to scan for code files")
    parser.add_argument("--ignore-dirs", nargs="+", default=default_ignore_dirs, 
                       help=f"Directories to ignore (default: {default_ignore_dirs})")
    parser.add_argument("--ignore-files", nargs="+", default=default_ignore_files,
                       help=f"Specific files to ignore (default: {default_ignore_files})")
    return parser.parse_args()

def main() -> None:
    """Entry point for the CLI application."""
    args = parse_arguments()

    if not args.directory.exists():
        sys.exit(f"Error: Directory '{args.directory}' does not exist")

    markdown_content = generate_markdown(
        root_dir=args.directory,
        ignore_dirs=args.ignore_dirs,
        ignore_files=args.ignore_files,
    )
    
    try:
        pyperclip.copy(markdown_content)
        print("Markdown content copied to clipboard successfully!")
    except pyperclip.PyperclipException as e:
        sys.exit(f"Error: Failed to copy to clipboard: {e}")

if __name__ == "__main__":
    main()