from pathlib import Path
from typing import Dict, List, Set, DefaultDict
from collections import defaultdict
import argparse


class DirectoryIndexer:

    def __init__(
        self,
        root_dir: Path,
        ignore_dirs: Set[str],
        ignore_files: Set[str],
        output_name: str = "index.md",
    ) -> None:
        self.root_dir = root_dir
        self.ignore_dirs = ignore_dirs
        self.ignore_files = ignore_files
        self.output_name = output_name
        self.content_dir = root_dir / "content"

    def should_ignore(self, path: Path) -> bool:
        if any(part in self.ignore_dirs for part in path.parts):
            return True
        if path.name in self.ignore_files:
            return True
        return False

    def format_name(self, name: str) -> str:
        name = name.replace("-", " ")
        return name.title()

    def discover_directory_structure(self) -> Dict[Path, List[Path]]:
        structure: DefaultDict[Path, List[Path]] = defaultdict(list)

        for item in self.content_dir.glob("**/*"):
            if self.should_ignore(item):
                continue
            structure[item.parent].append(item)

        return dict(structure)

    def generate_directory_index(self, directory: Path, contents: List[Path]) -> str:
        display_name = self.format_name(directory.name)
        lines: List[str] = [f"# {display_name}\n\n"]
        dirs: List[Path] = []
        files: List[Path] = []

        for item in contents:
            if item.is_dir():
                dirs.append(item)
            else:
                files.append(item)

        dirs.sort()
        files.sort()

        if dirs:
            lines.append("## Directories\n\n")
            for dir_path in dirs:
                rel_path = dir_path.relative_to(directory)
                display_dir_name = self.format_name(dir_path.name)
                lines.append(f"- [{display_dir_name}]({rel_path}/{self.output_name})\n")
            lines.append("\n")

        if files:
            lines.append("## Files\n\n")
            for file_path in files:
                display_file_name = self.format_name(file_path.stem)
                lines.append(f"- [{display_file_name}]({file_path.name})\n")

        return "".join(lines)

    def generate_all_indices(self) -> None:
        structure = self.discover_directory_structure()

        for directory, contents in structure.items():
            index_content = self.generate_directory_index(directory, contents)
            index_path = directory / self.output_name
            index_path.write_text(index_content, encoding="utf-8")

    def generate_root_index(self) -> None:
        dirs: List[Path] = []
        files: List[Path] = []
        
        for item in self.content_dir.iterdir():
            if self.should_ignore(item):
                continue
            if item.is_dir():
                dirs.append(item)
            elif item.is_file() and item.suffix == '.md' and item.name != self.output_name:
                files.append(item)

        if not dirs and not files:
            return

        dirs.sort()
        files.sort()
        
        lines: List[str] = ["# Index\n\n"]
        
        if dirs:
            lines.append("## Directories\n\n")
            for dir_path in dirs:
                rel_path = dir_path.relative_to(self.content_dir)
                display_dir_name = self.format_name(dir_path.name)
                lines.append(f"- [{display_dir_name}]({rel_path}/{self.output_name})\n")
            lines.append("\n")
        
        if files:
            lines.append("## Files\n\n")
            for file_path in files:
                display_file_name = self.format_name(file_path.stem)
                lines.append(f"- [{display_file_name}]({file_path.name})\n")

        index_path = self.content_dir / self.output_name
        index_path.write_text("".join(lines), encoding="utf-8")


def validate_directory(path: Path) -> Path:
    if not path.exists():
        raise ValueError(f"Directory does not exist: {path}")
    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate nested Markdown index files with consistent capitalization."
    )
    parser.add_argument(
        "root_dir",
        type=Path,
        help="Root directory containing 'content' folder",
    )
    parser.add_argument(
        "--ignore-dirs",
        nargs="*",
        default=["_layouts", "assets", ".git", "draft", "__pycache__", ".github"],
        help="Directories to ignore",
    )
    parser.add_argument(
        "--ignore-files",
        nargs="*",
        default=["_config.yml", "README.md", "index.md", ".gitignore"],
        help="Files to ignore",
    )
    parser.add_argument(
        "--output-name",
        default="index.md",
        help="Name of the index files to generate",
    )

    args = parser.parse_args()

    try:
        validated_dir = validate_directory(args.root_dir)
        indexer = DirectoryIndexer(
            root_dir=validated_dir,
            ignore_dirs=set(args.ignore_dirs),
            ignore_files=set(args.ignore_files),
            output_name=args.output_name,
        )

        indexer.generate_all_indices()
        indexer.generate_root_index()

        print(f"Successfully generated indices in {validated_dir}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()