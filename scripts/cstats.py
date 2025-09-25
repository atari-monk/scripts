#!/usr/bin/env python3
import ast
import argparse
from typing import Dict, Any

def analyze_file(file_path: str) -> Dict[str, Any]:
    """Analyze a Python file and return statistics."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Count only lines with actual code (ignore blanks and comments)
    loc = sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))

    # Parse AST
    tree = ast.parse("".join(lines))

    num_functions = 0
    num_classes = 0
    function_lengths: list[int] = []
    dependencies: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            num_functions += 1
            start = node.lineno
            end = getattr(node, 'end_lineno', start)
            function_lengths.append(end - start + 1)
        elif isinstance(node, ast.ClassDef):
            num_classes += 1
        elif isinstance(node, ast.Import):
            for n in node.names:
                dependencies.add(n.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                dependencies.add(node.module.split('.')[0])

    avg_func_len = sum(function_lengths) / len(function_lengths) if function_lengths else 0
    max_func_len = max(function_lengths) if function_lengths else 0
    num_dependencies = len(dependencies)

    return {
        "loc": loc,
        "num_functions": num_functions,
        "num_classes": num_classes,
        "avg_function_length": round(avg_func_len, 2),
        "max_function_length": max_func_len,
        "dependencies_count": num_dependencies,
        "dependencies": sorted(list(dependencies))
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Python file metrics")
    parser.add_argument("file", help="Path to the Python file to analyze")
    args = parser.parse_args()

    stats = analyze_file(args.file)
    for k, v in stats.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
