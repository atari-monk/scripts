import argparse
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


def should_ignore(path: Path, ignore_dirs: Set[str], ignore_files: Set[str]) -> bool:
    # Check if any parent directory is in ignore_dirs
    for parent in path.parents:
        if parent.name in ignore_dirs:
            return True
    
    # Check if the file itself should be ignored
    if path.name in ignore_files:
        return True
    
    return False


def discover_markdown_files(root_dir: Path, ignore_dirs: Set[str], ignore_files: Set[str]) -> Dict[str, List[Path]]:
    categories: Dict[str, List[Path]] = defaultdict(list)
    for item in root_dir.glob("**/*.md"):
        if (item.is_file() and 
            item != root_dir / "index.md" and 
            not should_ignore(item, ignore_dirs, ignore_files)):
            relative_path = item.relative_to(root_dir)
            category = str(relative_path.parent)
            categories[category].append(relative_path)
    return dict(categories)


def generate_index_content(categories: Dict[str, List[Path]]) -> str:
    content: List[str] = []
    for category, files in sorted(categories.items()):
        if category != ".":
            # Capitalize first letter of each word in category name
            display_category = ' '.join(word.capitalize() for word in category.split('/'))
            content.append(f"\n## {display_category}\n")
        else:
            content.append("\n## Root\n")
        
        for file_path in sorted(files):
            title = file_path.stem.replace("-", " ").title()
            link_path = file_path.with_suffix('')
            content.append(f"- [{title}]({link_path})\n")
    return "".join(content)


def write_index_file(root_dir: Path, content: str) -> None:
    index_path = root_dir / "index.md"
    index_path.write_text(content, encoding="utf-8")


def validate_directory(path: Path) -> Path:
    if not path.exists():
        raise ValueError(f"Directory does not exist: {path}")
    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate blog index from markdown files.")
    parser.add_argument(
        "blog_dir",
        type=Path,
        help="Root directory of the blog repository",
    )
    args = parser.parse_args()

    # Define directories and files to ignore
    IGNORE_DIRS = {"_layouts", "assets", ".git", "draft"}
    IGNORE_FILES = {"_config.yml", "README.md", "index.md"}

    try:
        validated_dir = validate_directory(args.blog_dir)
        markdown_files = discover_markdown_files(validated_dir, IGNORE_DIRS, IGNORE_FILES)
        index_content = generate_index_content(markdown_files)
        write_index_file(validated_dir, index_content)
        print(f"Successfully generated index at {validated_dir/'index.md'}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()