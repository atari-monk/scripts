#!/usr/bin/env python3
import pyperclip
import os
import sys
from pathlib import Path
from typing import NoReturn

# Configuration
CLIPBOARD_FILE = Path("C:/Atari-Monk-Art/app-data/clipboard.md")
SEPARATOR = "\n\n---\n\n"  # Separator between entries

def ensure_directory_exists() -> None:
    """Create directory if it doesn't exist"""
    CLIPBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)

def push_from_clipboard() -> None:
    """Store clipboard content to file with timestamp"""
    ensure_directory_exists()
    try:
        content: str = pyperclip.paste()
        entry = f"{content}"
        
        mode = 'a' if CLIPBOARD_FILE.exists() else 'w'
        with open(CLIPBOARD_FILE, mode, encoding='utf-8') as f:
            if mode == 'a':
                f.write(SEPARATOR)
            f.write(entry)
        print(f"Clipboard content appended to {CLIPBOARD_FILE}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def push_from_file(file_path: str) -> None:
    """Store file content to clipboard file with language marker"""
    ensure_directory_exists()
    try:
        ext: str = os.path.splitext(file_path)[1][1:]  # Get extension without dot
        with open(file_path, 'r', encoding='utf-8') as src:
            content: str = src.read()
        
        entry = f"```{ext}\n{content}\n```"
        
        mode = 'a' if CLIPBOARD_FILE.exists() else 'w'
        with open(CLIPBOARD_FILE, mode, encoding='utf-8') as f:
            if mode == 'a':
                f.write(SEPARATOR)
            f.write(entry)
        print(f"File content appended with {ext} formatting to {CLIPBOARD_FILE}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def pop_to_clipboard() -> None:
    """Load content from file to clipboard and erase file"""
    try:
        if not CLIPBOARD_FILE.exists():
            print("Error: No clipboard content stored", file=sys.stderr)
            sys.exit(1)
            
        with open(CLIPBOARD_FILE, 'r', encoding='utf-8') as f:
            content: str = f.read()
        pyperclip.copy(content)
        os.remove(CLIPBOARD_FILE)
        print("Content restored to clipboard and file erased")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def reset_clipboard() -> None:
    """Erase the clipboard file"""
    try:
        if CLIPBOARD_FILE.exists():
            os.remove(CLIPBOARD_FILE)
            print("Clipboard file erased")
        else:
            print("No clipboard file exists", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def show_help() -> NoReturn:
    """Show usage information and exit"""
    print("Clipboard Manager Commands:")
    print(f"  {sys.argv[0]} push           - Store clipboard content")
    print(f"  {sys.argv[0]} push <file>    - Store file content with formatting")
    print(f"  {sys.argv[0]} pop            - Restore content to clipboard")
    print(f"  {sys.argv[0]} reset          - Erase clipboard file")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        show_help()

    command: str = sys.argv[1].lower()
    
    if command == "push":
        if len(sys.argv) > 2:
            push_from_file(sys.argv[2])
        else:
            push_from_clipboard()
    elif command == "pop":
        pop_to_clipboard()
    elif command == "reset":
        reset_clipboard()
    elif command in ("-h", "--help", "help"):
        show_help()
    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        show_help()