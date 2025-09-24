#!/usr/bin/env python
from __future__ import annotations

import argparse
import pyperclip
from pathlib import Path

def get_file_content(file_path: Path) -> str:
    """Read and return the content of a file."""
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"[Binary file content not displayed: {file_path}]"

def is_text_file(file_path: Path) -> bool:
    """Check if a file is likely to be a text file."""
    try:
        file_path.read_text(encoding="utf-8")
        return True
    except UnicodeDecodeError:
        return False

def gather_text_files(paths: list[Path]) -> list[Path]:
    """Collect all text files from given paths with proper typing."""
    files: list[Path] = []
    
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        
        if path.is_file() and is_text_file(path):
            files.append(path)
        elif path.is_dir():
            # This ensures proper type inference
            dir_files = [p for p in path.rglob("*") 
                        if p.is_file() and is_text_file(p)]
            files.extend(dir_files)
    
    return files

def generate_markdown(files: list[Path]) -> str:
    """Generate markdown content from files."""
    markdown_parts: list[str] = []
    
    for file_path in files:
        content = get_file_content(file_path)
        language = file_path.suffix.lstrip(".")
        markdown_parts.append(f"{file_path}\n```{language}\n{content}\n```\n\n")
    
    return "".join(markdown_parts)

def parse_arguments() -> list[Path]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert file contents to Markdown and copy to clipboard"
    )
    parser.add_argument(
        "paths", nargs="+", type=Path, help="File or directory paths to process"
    )
    return parser.parse_args().paths

def main() -> None:
    """Convert file contents to Markdown and copy to clipboard."""
    try:
        paths = parse_arguments()
        files = gather_text_files(paths)
        
        if not files:
            print("No text files found to process")
            return
        
        result = generate_markdown(files)
        pyperclip.copy(result)
        print("Markdown content copied to clipboard successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()