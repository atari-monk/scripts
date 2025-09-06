import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, DefaultDict
from collections import defaultdict


def should_ignore(path: Path, ignore_dirs: Set[str], ignore_files: Set[str]) -> bool:
    for parent in path.parents:
        if parent.name in ignore_dirs:
            return True
    if path.name in ignore_files:
        return True
    return False


def discover_markdown_files(root_dir: Path, ignore_dirs: Set[str], ignore_files: Set[str]) -> Dict[Tuple[str, ...], List[Path]]:
    categories: DefaultDict[Tuple[str, ...], List[Path]] = defaultdict(list)
    content_dir = root_dir / "content"
    
    for item in content_dir.glob("**/*.md"):
        if item.is_file() and not should_ignore(item, ignore_dirs, ignore_files):
            relative_path = item.relative_to(content_dir)
            path_parts = relative_path.parts[:-1]  # Exclude the filename itself
            categories[path_parts].append(relative_path)
    
    return dict(categories)


def generate_nested_list(categories: Dict[Tuple[str, ...], List[Path]]) -> str:
    content: List[str] = []
    sorted_categories = sorted(categories.items(), key=lambda x: x[0])
    
    current_indent = 0
    current_path: Tuple[str, ...] = ()
    
    for path_parts, files in sorted_categories:
        common_depth = 0
        for a, b in zip(current_path, path_parts):
            if a == b:
                common_depth += 1
            else:
                break
        
        while len(current_path) > common_depth:
            current_path = current_path[:-1]
            current_indent -= 1
        
        for depth in range(common_depth, len(path_parts)):
            part = path_parts[depth]
            display_name = part.replace("-", " ").title()
            content.append("    " * current_indent + f"- {display_name}\n")
            current_path = path_parts[:depth+1]
            current_indent += 1
        
        for file_path in sorted(files):
            title = file_path.stem.replace("-", " ").title()
            link_path = Path("content") / file_path.with_suffix('')
            content.append("    " * current_indent + f"- [{title}]({link_path})\n")
    
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

    IGNORE_DIRS: Set[str] = {"_layouts", "assets", ".git", "draft"}
    IGNORE_FILES: Set[str] = {"_config.yml", "README.md", "index.md"}

    try:
        validated_dir = validate_directory(args.blog_dir)
        markdown_files = discover_markdown_files(validated_dir, IGNORE_DIRS, IGNORE_FILES)
        index_content = generate_nested_list(markdown_files)
        write_index_file(validated_dir, index_content)
        print(f"Successfully generated index at {validated_dir/'index.md'}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()