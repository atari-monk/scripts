#!/usr/bin/env python3
from pathlib import Path
import argparse
from typing import Iterator, List
import sys


def find_files(directory: Path) -> Iterator[Path]:
    for path in directory.iterdir():
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from find_files(path)


def save_file_paths(directory: Path, file_paths: List[Path]) -> None:
    output_path = directory / "paths.md"
    with output_path.open("w", encoding="utf-8") as f:
        f.write("# List of Files\n\n")
        f.write("```\n")
        f.write("\n".join(str(path.resolve()) for path in file_paths))
        f.write("\n```\n")
    print(f"Saved {len(file_paths)} file paths to {output_path}")


def parse_arguments() -> Path:
    parser = argparse.ArgumentParser(description="List all files in a directory recursively and save to paths.md.")
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory path to search for files",
    )
    args = parser.parse_args()
    
    if not args.directory.exists():
        raise argparse.ArgumentError(None, f"Directory does not exist: {args.directory}")
    if not args.directory.is_dir():
        raise argparse.ArgumentError(None, f"Path is not a directory: {args.directory}")
        
    return args.directory


def main() -> None:
    try:
        target_dir = parse_arguments()
        files = list(find_files(target_dir))
        save_file_paths(target_dir, files)
    except argparse.ArgumentError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: Permission denied - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()