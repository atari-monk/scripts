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
            path_parts = relative_path.parts[:-1]
            categories[path_parts].append(relative_path)
    
    return dict(categories)


def generate_category_hierarchy(categories: Dict[Tuple[str, ...], List[Path]]) -> List[Tuple[int, str, List[Path]]]:
    hierarchy: List[Tuple[int, str, List[Path]]] = []
    
    for path_parts in sorted(categories.keys()):
        files = categories[path_parts]
        
        if not path_parts:
            hierarchy.append((0, "Root", files))
            continue
        
        for depth, part in enumerate(path_parts, start=1):
            existing = next((x for x in hierarchy if x[1] == part and x[0] == depth-1), None)
            if not existing:
                hierarchy.append((depth-1, part, files if depth == len(path_parts) else []))
    
    return hierarchy


def generate_index_content(categories: Dict[Tuple[str, ...], List[Path]]) -> str:
    content: List[str] = []
    hierarchy = generate_category_hierarchy(categories)
    
    current_depth = -1
    for depth, category, files in hierarchy:
        heading_level = min(depth + 2, 6)
        
        if depth < current_depth:
            content.append("\n")
        
        display_name = category.replace("-", " ").title()
        content.append(f"{'#' * heading_level} {display_name}\n\n")
        
        if files:
            for file_path in sorted(files):
                title = file_path.stem.replace("-", " ").title()
                link_path = Path("content") / file_path.with_suffix('')
                content.append(f"- [{title}]({link_path})\n")
        
        current_depth = depth
    
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
        index_content = generate_index_content(markdown_files)
        write_index_file(validated_dir, index_content)
        print(f"Successfully generated index at {validated_dir/'index.md'}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()