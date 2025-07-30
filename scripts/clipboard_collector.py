#!/usr/bin/env python3
"""Clipboard content collector tool."""

import sys
from typing import List, Optional
import pyperclip
import keyboard


class ClipboardCollector:
    """Collects multiple clipboard entries until Esc is pressed."""

    def __init__(self) -> None:
        """Initialize the collector with empty entries."""
        self.entries: List[str] = []

    def collect_entries(self) -> None:
        """Collect clipboard entries until Esc is pressed."""
        print(">>Enter to get clipboard content, Esc to end")
        while True:
            if keyboard.is_pressed("esc"):
                break
            if keyboard.is_pressed("enter"):
                content = self._get_clipboard_content()
                if content and content not in self.entries:
                    self.entries.append(content)
                    print(f"Captured: {content[:50]}...")

    def _get_clipboard_content(self) -> Optional[str]:
        """Safely get clipboard content with error handling."""
        try:
            return pyperclip.paste().strip()
        except pyperclip.PyperclipException as e:
            print(f"Error accessing clipboard: {e}", file=sys.stderr)
            return None

    def format_entries(self) -> str:
        """Format collected entries as a single string."""
        return "\n\n".join(self.entries) if self.entries else ""


def main() -> None:
    """Orchestrate the clipboard collection process."""
    collector = ClipboardCollector()
    collector.collect_entries()
    formatted_content = collector.format_entries()
    
    if formatted_content:
        try:
            pyperclip.copy(formatted_content)
            print("\nContents copied back to clipboard:")
            print(formatted_content)
        except pyperclip.PyperclipException as e:
            print(f"Error writing to clipboard: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("No content collected.", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)