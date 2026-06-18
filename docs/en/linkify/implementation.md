## File: scripts/python/linkify.py

```py
from typing import List
import sys


def parse_input(args: List[str]) -> str:
    return " ".join(args).strip()


def split_expressions(raw: str) -> List[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def validate_expression(expression: str) -> None:
    words: List[str] = expression.split()
    if not words:
        sys.exit(1)
    for word in words:
        if not word.isalpha():
            sys.exit(1)


def make_slug(expression: str) -> str:
    return "-".join(word.lower() for word in expression.split())


def format_markdown(expression: str) -> str:
    return f"- [{expression.strip()}](#{make_slug(expression)})"


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(1)

    raw: str = parse_input(sys.argv[1:])
    expressions: List[str] = split_expressions(raw)

    output: List[str] = []
    for expr in expressions:
        validate_expression(expr)
        output.append(format_markdown(expr))

    print("\n".join(output))


if __name__ == "__main__":
    main()
```