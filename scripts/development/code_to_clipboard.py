#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable, Optional, Set, TextIO
from io import StringIO

try:
    import pyperclip
except ImportError:
    print("Error: pyperclip module is required. Please install it with: pip install pyperclip")
    sys.exit(1)


class CodeFileProcessor:
    """Handles processing of individual code files into markdown blocks."""

    @staticmethod
    def get_language_from_extension(file_path: pathlib.Path) -> str:
        """Determine markdown language from file extension."""
        extension_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".kt": "kotlin",
            ".go": "go",
            ".rs": "rust",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
            ".sh": "bash",
            ".html": "html",
            ".css": "css",
            ".scss": "scss",
            ".sql": "sql",
            ".md": "markdown",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".toml": "toml",
        }
        return extension_map.get(file_path.suffix.lower(), "text")

    @classmethod
    def file_to_markdown(cls, file_path: pathlib.Path, output: TextIO) -> None:
        """Convert a single file to markdown code block and write to output."""
        language = cls.get_language_from_extension(file_path)
        output.write(f"\n{file_path}\n```{language}\n")
        with file_path.open("r", encoding="utf-8") as f:
            output.write(f.read())
        output.write("\n```\n")


class DirectoryScanner:
    """Handles directory scanning with ignore patterns."""

    def __init__(self, ignore_dirs: set[str], ignore_files: set[str]) -> None:
        self.ignore_dirs = ignore_dirs
        self.ignore_files = ignore_files

    def should_ignore(self, path: pathlib.Path) -> bool:
        """Check if path matches any ignore patterns."""
        if path.name in self.ignore_files:
            return True
        return any(part in self.ignore_dirs for part in path.parts)


class MarkdownGenerator:
    """Orchestrates the markdown generation process."""

    def __init__(
        self,
        root_dir: pathlib.Path,
        ignore_dirs: Optional[Iterable[str]] = None,
        ignore_files: Optional[Iterable[str]] = None,
    ) -> None:
        self.root_dir = root_dir
        self.ignore_dirs: Set[str] = set(ignore_dirs) if ignore_dirs else set()
        self.ignore_files: Set[str] = set(ignore_files) if ignore_files else set()

    def generate(self) -> str:
        """Generate markdown content from directory contents."""
        scanner = DirectoryScanner(
            ignore_dirs=self.ignore_dirs,
            ignore_files=self.ignore_files
        )
        with StringIO() as buffer:
            for file_path in self._walk_directory():
                if not scanner.should_ignore(file_path):
                    CodeFileProcessor.file_to_markdown(file_path, buffer)
            return buffer.getvalue()

    def _walk_directory(self) -> Iterable[pathlib.Path]:
        """Walk through directory and yield all file paths."""
        return (
            path
            for path in self.root_dir.rglob("*")
            if path.is_file() and not path.name.startswith(".")
        )


def parse_arguments() -> argparse.Namespace:
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a Markdown file containing code from all files in a directory and copy to clipboard."
    )
    parser.add_argument(
        "directory",
        type=pathlib.Path,
        help="Directory to scan for code files",
    )
    parser.add_argument(
        "--ignore-dirs",
        nargs="+",
        default=[".git", "__pycache__", "node_modules", "venv"],
        help="Directories to ignore",
    )
    parser.add_argument(
        "--ignore-files",
        nargs="+",
        default=["vite-env.d.ts", "tsconfig.json", "package.json"],
        help="Specific files to ignore",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point for the CLI application."""
    args = parse_arguments()

    if not args.directory.exists():
        sys.exit(f"Error: Directory '{args.directory}' does not exist")

    generator = MarkdownGenerator(
        root_dir=args.directory,
        ignore_dirs=args.ignore_dirs,
        ignore_files=args.ignore_files,
    )
    markdown_content = generator.generate()
    
    try:
        pyperclip.copy(markdown_content)
        print("Markdown content copied to clipboard successfully!")
    except pyperclip.PyperclipException as e:
        sys.exit(f"Error: Failed to copy to clipboard: {e}")


if __name__ == "__main__":
    main()