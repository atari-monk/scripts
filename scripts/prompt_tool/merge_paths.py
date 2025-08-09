#!/usr/bin/env python
from __future__ import annotations

import argparse
import pyperclip
from pathlib import Path
from typing import Iterator, List, Optional, Iterable


class FileProcessor:
    @staticmethod
    def get_file_content(file_path: Path) -> str:
        """Read and return the content of a file."""
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return f"[Binary file content not displayed: {file_path}]"

    @staticmethod
    def is_text_file(file_path: Path) -> bool:
        """Check if a file is likely to be a text file."""
        try:
            file_path.read_text(encoding="utf-8")
            return True
        except UnicodeDecodeError:
            return False


class MarkdownGenerator:
    @staticmethod
    def format_as_markdown(file_path: Path, content: str) -> str:
        """Format file content as a Markdown code block."""
        language = file_path.suffix.lstrip(".")
        return f"{file_path}\n```{language}\n{content}\n```\n\n"

    @classmethod
    def process_path(cls, path: Path) -> Iterator[str]:
        """Recursively process a path and yield Markdown formatted content."""
        if path.is_file() and FileProcessor.is_text_file(path):
            content = FileProcessor.get_file_content(path)
            yield cls.format_as_markdown(path, content)
        elif path.is_dir():
            for item in path.rglob("*"):
                if item.is_file() and FileProcessor.is_text_file(item):
                    content = FileProcessor.get_file_content(item)
                    yield cls.format_as_markdown(item, content)


class ClipboardManager:
    @staticmethod
    def copy_to_clipboard(content: str) -> None:
        """Copy content to system clipboard."""
        try:
            pyperclip.copy(content)
        except pyperclip.PyperclipException as e:
            raise RuntimeError("Failed to access clipboard") from e


def parse_arguments(args: Optional[List[str]] = None) -> List[Path]:
    """Parse command line arguments into Path objects."""
    parser = argparse.ArgumentParser(
        description="Convert file contents to Markdown and copy to clipboard"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="File or directory paths to process",
    )
    parsed = parser.parse_args(args)
    return parsed.paths


def validate_paths(paths: Iterable[Path]) -> None:
    """Validate that all paths exist."""
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")


def main() -> None:
    """Orchestrate the file processing and clipboard operations."""
    try:
        paths = parse_arguments()
        validate_paths(paths)
        
        markdown_content: List[str] = []
        for path in paths:
            markdown_content.extend(MarkdownGenerator.process_path(path))
        
        if not markdown_content:
            print("No text files found to process")
            return
            
        result = "".join(markdown_content)
        ClipboardManager.copy_to_clipboard(result)
        print("Markdown content copied to clipboard successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
