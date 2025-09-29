from pathlib import Path
from typing import List
import sys

DEFAULT_PATH = Path("C:/Atari-Monk/scripts/scripts").resolve()

def generate_line(file: Path) -> str:
    if not file.exists() or file.name == "__init__.py":
        return ""
    if file.suffix == ".py":
        return f'{file.stem} = "scripts.{file.stem}:main"'
    elif file.suffix == ".ps1":
        return f'Set-Alias -Name {file.stem} -Value "{file}"'
    return ""

def main() -> None:
    path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_PATH

    py_lines: List[str] = []
    ps1_lines: List[str] = []

    if path.is_dir():
        for file in path.iterdir():
            line = generate_line(file)
            if line:
                if file.suffix == ".py":
                    py_lines.append(line)
                elif file.suffix == ".ps1":
                    ps1_lines.append(line)
    else:
        line = generate_line(path)
        if line:
            if path.suffix == ".py":
                py_lines.append(line)
            elif path.suffix == ".ps1":
                ps1_lines.append(line)

    for line in py_lines + ps1_lines:
        print(line)

if __name__ == "__main__":
    main()
