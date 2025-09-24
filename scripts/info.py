#!/usr/bin/env python3
"""📘 Info Tool - Simple command reference display"""

import argparse
import json
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, TypedDict

class Command(TypedDict):
    alias: str
    description: str
    category: str

def main() -> None:
    parser = argparse.ArgumentParser(description="📘 Info Tool - Command reference")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show descriptions")
    default_path = Path(__file__).parent.parent / "data" / "info.json"
    parser.add_argument("--json-path", type=Path, default=default_path)
    args = parser.parse_args()
    
    # Load commands
    try:
        with args.json_path.open('r', encoding='utf-8') as f:
            commands: List[Command] = json.load(f).get("commands", [])
    except (FileNotFoundError, json.JSONDecodeError):
        commands = []
    
    if not commands:
        print("No commands available.")
        return
    
    # Group by category using defaultdict for cleaner code
    categories: Dict[str, List[Command]] = defaultdict(list)
    for cmd in commands:
        categories[cmd.get("category", "Uncategorized")].append(cmd)
    
    # Display commands
    for category, cmds in categories.items():
        print(f"\n{category}\n{'-' * len(category)}")
        for cmd in cmds:
            if args.verbose:
                print(f"  {cmd['alias']}: {cmd['description']}")
            else:
                print(f"  {cmd['alias']}")

if __name__ == "__main__":
    main()