## scripts/python/templateify.py

```py
from __future__ import annotations

import re
from pathlib import Path
import sys


INCLUDE_PATTERN = re.compile(r"\[\[include:(.*?)\]\]")


def load_include(template_dir: Path, include_path: str) -> str:
    path = (template_dir / include_path.strip()).resolve()
    return path.read_text(encoding="utf-8")


def render_template(template_path: Path) -> str:
    content = template_path.read_text(encoding="utf-8")
    template_dir = template_path.parent

    def replace(match: re.Match[str]) -> str:
        return load_include(template_dir, match.group(1))

    return INCLUDE_PATTERN.sub(replace, content)


def output_path(template_path: Path) -> Path:
    return template_path.with_name(template_path.name.replace("_", ""))


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: template_assembler.py <template-file>", file=sys.stderr)
        return 1

    template_path = Path(sys.argv[1]).resolve()

    if not template_path.is_file():
        print(f"file not found: {template_path}", file=sys.stderr)
        return 1

    rendered = render_template(template_path)
    target = output_path(template_path)
    target.write_text(rendered, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```