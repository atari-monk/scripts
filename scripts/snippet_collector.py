#!/usr/bin/env python3
"""
Snippet Collector

Small utility to collect snippets from clipboard or file into a single Markdown file in clip.
"""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Optional

import pyperclip

# Separator that appears between snippets in the single collection file
SEPARATOR = "\n\n---\n\n"

# Mapping of common extensions -> language hints for fenced code blocks
EXT_TO_LANG = {
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "json": "json",
    "yaml": "yaml",
    "yml": "yaml",
    "md": "",
    "txt": "",
    "sh": "bash",
    "bat": "batch",
    "ps1": "powershell",
    "java": "java",
    "c": "c",
    "cpp": "cpp",
    "h": "c",
    "html": "html",
    "css": "css",
    "rb": "ruby",
    "go": "go",
    # add more as desired
}


logger = logging.getLogger(__name__)


def default_collection_file() -> Path:
    """
    Determine the default snippets collection file.
    Uses the SNIPPET_COLLECTOR_PATH env var if set, otherwise a directory under the user's home.
    """
    base_env = os.getenv("SNIPPET_COLLECTOR_PATH")
    if base_env:
        base = Path(base_env)
    else:
        base = Path.home() / ".snippet_collector"
    return base / "snippets.md"


def _choose_fence_for_content(content: str) -> str:
    """Use triple backticks unless content contains them, then use quadruple."""
    return "````" if "```" in content else "```"


def _format_file_content(file_path: Path, content: str) -> str:
    """
    Format file content with a header and an optional fenced code block for markdown.
    Avoids collisions with existing backtick runs in the content.
    """
    extension = file_path.suffix.lstrip(".")
    header = f"**File:** {file_path.name}"
    if extension:
        header += f" (.{extension})"

    lang = EXT_TO_LANG.get(extension, extension)
    fence = _choose_fence_for_content(content)

    return f"{header}\n\n{fence}{lang}\n{content}\n{fence}"


def _append_content(file_path: Path, content: str) -> None:
    """
    Append content to the collection file, inserting SEPARATOR only if the file already
    has non-zero size (so we don't start a file with the separator).
    Ensures parent dir exists.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    mode = "a" if file_path.exists() and file_path.stat().st_size > 0 else "w"
    with file_path.open(mode, encoding="utf-8") as fh:
        if mode == "a":
            fh.write(SEPARATOR)
        fh.write(content)


def add_clipboard(file_path: Path) -> None:
    """Add current clipboard content to snippet collection file."""
    try:
        content = pyperclip.paste()
    except Exception as e:
        raise RuntimeError(
            "Failed to read system clipboard. Ensure a clipboard backend is available. "
            f"Underlying error: {e}"
        )
    _append_content(file_path, content)
    logger.info("Clipboard content added to %s", file_path)


def add_file(file_path: Path, source_path: str) -> None:
    """Add file content with syntax highlighting to snippet collection file."""
    src = Path(source_path)
    if not src.exists():
        raise FileNotFoundError(str(src))
    # reading with explicit encoding; handle decode errors to give a friendly message
    try:
        content = src.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise RuntimeError(f"Unable to decode file {src} as utf-8.")
    formatted = _format_file_content(src, content)
    _append_content(file_path, formatted)
    logger.info("File content from %s added to %s", src, file_path)


def copy_all(file_path: Path, remove_after: bool = True) -> None:
    """
    Copy all collected snippets to clipboard. Optionally remove the collection file after copying.
    If no snippets exist, this is a no-op (logs info).
    """
    if not file_path.exists():
        logger.info("No snippets collected to copy.")
        return
    content = file_path.read_text(encoding="utf-8")
    try:
        pyperclip.copy(content)
    except Exception as e:
        raise RuntimeError(
            "Failed to copy to system clipboard. Ensure a clipboard backend is available. "
            f"Underlying error: {e}"
        )
    logger.info("All collected snippets copied to clipboard.")
    if remove_after:
        try:
            file_path.unlink()
            logger.info("Collection file %s removed after copy.", file_path)
        except OSError as e:
            logger.warning("Could not remove collection file %s: %s", file_path, e)


def clear_collection(file_path: Path) -> None:
    """Clear the snippet collection file if it exists."""
    if not file_path.exists():
        logger.info("No snippet collection to clear.")
        return
    try:
        file_path.unlink()
        logger.info("Snippet collection cleared (%s).", file_path)
    except OSError as e:
        raise RuntimeError(f"Failed to clear snippet collection: {e}")


def show_collection(file_path: Path) -> None:
    """Print the current snippet collection to stdout (if present)."""
    if not file_path.exists():
        print("No snippets collected")
        return
    content = file_path.read_text(encoding="utf-8")
    print("\n" + "=" * 50)
    print("CURRENT SNIPPET COLLECTION:")
    print("=" * 50)
    print(content)
    print("=" * 50)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="snippet_collector", description="Collect snippets from clipboard or files into a Markdown file.")
    p.add_argument(
        "--path",
        "-p",
        type=Path,
        default=None,
        help="Path to directory where snippets.md will be stored (optional). "
             "Can also be set via SNIPPET_COLLECTOR_PATH env var. "
             "Default: ~/.snippet_collector/snippets.md",
    )

    sub = p.add_subparsers(dest="command", required=True, title="commands")

    add_parser = sub.add_parser("add", help="Add clipboard content (default) or a file if path provided.")
    add_parser.add_argument("file", nargs="?", help="Optional path to a file to add (if omitted, clipboard is used).")

    sub.add_parser("copy", help="Copy all collected snippets to clipboard and (by default) clear the collection.")\
        .add_argument("--keep", action="store_true", help="Do not delete the collection file after copying.")

    sub.add_parser("show", help="Display current collection without copying.")
    sub.add_parser("clear", help="Clear collection without copying.")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    """
    Main entry point. Returns exit code (0 success, non-zero error).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    # Simplify path resolution
    collection_file = args.path / "snippets.md" if args.path else default_collection_file()

    # basic logging setup: keep infos visible for user, debug can be enabled externally
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    else:
        # if already configured by caller, preserve that
        pass

    try:
        cmd = args.command
        if cmd == "add":
            if getattr(args, "file", None):
                add_file(collection_file, args.file)
            else:
                add_clipboard(collection_file)
        elif cmd == "copy":
            keep = getattr(args, "keep", False)
            copy_all(collection_file, remove_after=not keep)
        elif cmd == "show":
            show_collection(collection_file)
        elif cmd == "clear":
            clear_collection(collection_file)
        else:
            # argparse should handle unknown commands, but be defensive
            parser.print_help()
            return 2
        return 0

    except (FileNotFoundError, RuntimeError) as e:
        logger.error("%s", e)
        return 2
    except Exception as e:
        # Unexpected errors - let them propagate with full traceback
        logger.error("Unexpected error occurred: %s", e)
        raise


if __name__ == "__main__":
    raise SystemExit(main())