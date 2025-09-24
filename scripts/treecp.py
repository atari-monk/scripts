#!/usr/bin/env python3
"""
Simple directory tree generator that copies to clipboard.
"""

import sys
from pathlib import Path
from typing import Set, List

try:
    import pyperclip
except ImportError:
    print("Error: pyperclip module is required. Please install it with: pip install pyperclip")
    sys.exit(1)

DEFAULT_IGNORE_FOLDERS: Set[str] = {'.git', '__pycache__', 'node_modules'}
DEFAULT_IGNORE_FILES: Set[str] = {'.DS_Store', 'Thumbs.db'}
DEFAULT_IGNORE_EXTENSIONS: Set[str] = {'.pyc', '.log'}


def validate_path(target_path: Path) -> None:
    if not target_path.exists():
        raise ValueError(f"Path '{target_path}' does not exist")
    if not target_path.is_dir():
        raise ValueError(f"'{target_path}' is not a directory")


def safe_clipboard_copy(content: str) -> None:
    try:
        pyperclip.copy(content)
    except pyperclip.PyperclipException as e:
        raise RuntimeError(f"Failed to copy to clipboard: {e}") from e


def should_include(item: Path, ignore_folders: Set[str], ignore_files: Set[str], ignore_extensions: Set[str]) -> bool:
    if item.is_dir():
        return item.name not in ignore_folders
    return item.name not in ignore_files and item.suffix not in ignore_extensions


def gather_directory_contents(path: Path, ignore_folders: Set[str], ignore_files: Set[str], ignore_extensions: Set[str]) -> List[Path]:
    items = [item for item in path.iterdir() 
             if should_include(item, ignore_folders, ignore_files, ignore_extensions)]
    return sorted(items, key=lambda p: (p.is_file(), p.name.lower()))


def build_tree(path: Path, prefix: str = '', ignore_folders: Set[str] = DEFAULT_IGNORE_FOLDERS,
               ignore_files: Set[str] = DEFAULT_IGNORE_FILES, ignore_extensions: Set[str] = DEFAULT_IGNORE_EXTENSIONS) -> str:
    contents = gather_directory_contents(path, ignore_folders, ignore_files, ignore_extensions)
    
    tree_lines: List[str] = []
    for index, item in enumerate(contents):
        connector = '└── ' if index == len(contents) - 1 else '├── '
        current_line = f"{prefix}{connector}{item.name}"
        
        if item.is_dir():
            current_line += "/"
            extension = '    ' if index == len(contents) - 1 else '│   '
            subtree = build_tree(item, prefix + extension, ignore_folders, ignore_files, ignore_extensions)
            tree_lines.append(f"{current_line}\n{subtree}")
        else:
            tree_lines.append(current_line)
    
    return '\n'.join(tree_lines)


def generate_directory_tree(root_path: Path) -> str:
    validate_path(root_path)
    return f"{root_path.name}/\n" + build_tree(root_path)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: treecp <folder_path>")
        sys.exit(1)

    root_path = Path(sys.argv[1])

    try:
        result = generate_directory_tree(root_path)
        safe_clipboard_copy(result)
        print("✅ Directory tree copied to clipboard!")
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()