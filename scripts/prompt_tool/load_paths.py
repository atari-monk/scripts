#!/usr/bin/env python3
import pyperclip
from pathlib import Path
import argparse
import sys
from typing import List

def extract_paths_from_md(md_file: Path) -> List[str]:
    with md_file.open('r', encoding='utf-8') as f:
        content = f.read()
    
    start = content.find('```\n') + 4
    end = content.find('\n```', start)
    if start == -1 or end == -1:
        raise ValueError("Could not find paths in the markdown file")
    
    paths = content[start:end].split('\n')
    return [path.strip() for path in paths if path.strip()]

def create_content_blocks(paths: List[str]) -> str:
    md_content: List[str] = []
    for path in paths:
        file_path = Path(path)
        try:
            with file_path.open('r', encoding='utf-8') as f:
                content = f.read()
            
            ext = file_path.suffix[1:] if file_path.suffix else 'text'
            
            md_content.append(f"{path}\n```{ext}\n{content}\n```\n")
        except Exception as e:
            md_content.append(f"{path}\nError reading file: {e}\n")
    
    return '\n'.join(md_content)

def main() -> None:
    try:
        parser = argparse.ArgumentParser(description="Load paths.md and create content blocks for each file.")
        parser.add_argument(
            "md_file",
            type=Path,
            help="Path to the paths.md file",
            default=Path("paths.md"),
            nargs='?'
        )
        args = parser.parse_args()
        
        if not args.md_file.exists():
            raise FileNotFoundError(f"File does not exist: {args.md_file}")
        
        paths = extract_paths_from_md(args.md_file)
        if not paths:
            print("No paths found in the markdown file", file=sys.stderr)
            sys.exit(1)
            
        md_content = create_content_blocks(paths)
        pyperclip.copy(md_content)
        print(f"Copied content for {len(paths)} files to clipboard")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()