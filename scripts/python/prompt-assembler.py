from __future__ import annotations

import json
import sys
from pathlib import Path
from glob import glob
import subprocess


def resolve_path(root: Path, entry: str) -> Path:
    p = Path(entry)
    return p if p.is_absolute() else root / p


def read_group(root: Path, entries: list[str]) -> str:
    files: list[Path] = []

    for entry in entries:
        if not entry or not entry.strip():
            continue
        entry = entry.strip()

        pattern = str(resolve_path(root, entry))
        matches = glob(pattern, recursive=True)

        if matches:
            files.extend(Path(m) for m in matches)
        else:
            p = Path(pattern)
            if p.exists():
                files.append(p)

    unique_files = sorted(set(files))

    parts: list[str] = []

    for file_path in unique_files:
        if not file_path.is_file():
            continue

        parts.append(f"# File: {file_path}")
        parts.append(file_path.read_text(encoding="utf-8"))

    return "\n\n".join(parts)


def parse_includes(template: str) -> list[tuple[bool, str]]:
    result: list[tuple[bool, str]] = []
    buf: list[str] = []

    i = 0
    n = len(template)

    while i < n:
        if i + 1 < n and template[i] == "[" and template[i + 1] == "[":

            if buf:
                result.append((False, "".join(buf)))
                buf.clear()

            i += 2
            start = i

            while i + 1 < n:
                if template[i] == "]" and template[i + 1] == "]":
                    key = template[start:i].strip()
                    result.append((True, key))
                    i += 2
                    break
                i += 1
            else:
                raise ValueError("Unclosed include: missing ']]'")

        else:
            buf.append(template[i])
            i += 1

    if buf:
        result.append((False, "".join(buf)))

    return result


def assemble(template_path: Path, mapping_path: Path) -> str:
    template = template_path.read_text(encoding="utf-8")
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    root = Path(mapping.get("root", mapping_path.parent))

    parts: list[str] = []

    tokens = parse_includes(template)

    for is_include, value in tokens:
        if not is_include:
            parts.append(value)
        else:
            entries = mapping.get(value)

            if not entries or all(not e.strip() for e in entries):
                continue

            parts.append(read_group(root, entries))

    return "".join(parts)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: assemble_prompt.py TEMPLATE MAP", file=sys.stderr)
        return 1

    result = assemble(Path(sys.argv[1]), Path(sys.argv[2]))

    subprocess.run(
        "xclip -selection clipboard",
        input=result,
        text=True,
        shell=True,
        check=True,
    )

    print("Copied result to clipboard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())