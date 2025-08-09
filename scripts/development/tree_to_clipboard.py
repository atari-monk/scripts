import sys
from pathlib import Path
import pyperclip

# ---------------- CONFIG ----------------

IGNORE_FOLDERS = {'.git', '__pycache__', 'node_modules'}
IGNORE_FILES = {'.DS_Store', 'Thumbs.db'}
IGNORE_EXTENSIONS = {'.pyc', '.log'}

# ----------------------------------------


def build_tree(path: Path, prefix: str = ''):
    tree = ''
    contents = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

    for index, item in enumerate(contents):
        connector = '└── ' if index == len(contents) - 1 else '├── '

        if item.is_dir():
            if item.name in IGNORE_FOLDERS:
                continue
            tree += f"{prefix}{connector}{item.name}/\n"
            extension = '    ' if index == len(contents) - 1 else '│   '
            tree += build_tree(item, prefix + extension)
        elif item.is_file():
            if item.name in IGNORE_FILES or item.suffix in IGNORE_EXTENSIONS:
                continue
            tree += f"{prefix}{connector}{item.name}\n"

    return tree


def main():
    if len(sys.argv) != 2:
        print(f"Usage: tree-clip <folder_path>")
        sys.exit(1)

    root_path = Path(sys.argv[1])

    if not root_path.exists() or not root_path.is_dir():
        print(f"Invalid path: {root_path}")
        sys.exit(1)

    result = f"{root_path.name}/\n" + build_tree(root_path)
    pyperclip.copy(result)
    print("✅ Directory tree copied to clipboard!")


if __name__ == '__main__':
    main()
