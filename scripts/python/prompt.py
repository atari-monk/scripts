from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import cast

from prompt_build import run_cli


BASE_DIR = Path(os.environ.get("HOME", "")) / "atari-monk" / "project"
PROMPTS_DIR = BASE_DIR / "prompts" / "prompts"
PROMPTS_PATH = PROMPTS_DIR / "prompts.json"
PROJECTS_PATH = BASE_DIR / "projects.json"


class Config:
    def __init__(self, prompts: dict[str, str], projects: dict[str, str]) -> None:
        self.prompts = prompts
        self.projects = projects


def load_json(path: Path) -> object:
    if not path.exists():
        raise FileNotFoundError(str(path))
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_prompts() -> dict[str, str]:
    raw = load_json(PROMPTS_PATH)
    if not isinstance(raw, dict):
        raise ValueError("prompts.json must be an object")
    return cast(dict[str, str], raw)


def load_projects() -> dict[str, str]:
    raw = load_json(PROJECTS_PATH)
    if not isinstance(raw, dict):
        raise ValueError("projects.json must be an object")
    return cast(dict[str, str], raw)


def load_config() -> Config:
    return Config(
        prompts=load_prompts(),
        projects=load_projects(),
    )


def print_help(config: Config) -> None:
    actions = "\n".join(sorted(config.prompts.keys()))
    projects = "\n".join(sorted(config.projects.keys()))

    sys.stdout.write(
        "Usage:\n"
        "  prompt <action> <project>\n\n"
        "Actions:\n"
        f"{actions}\n\n"
        "Projects:\n"
        f"{projects}\n"
    )


def main() -> int:
    config = load_config()

    if len(sys.argv) != 3:
        print_help(config)
        return 0

    action = sys.argv[1]
    project = sys.argv[2]

    if action not in config.prompts:
        print_help(config)
        return 1

    if project not in config.projects:
        print_help(config)
        return 1

    prompt_path = PROMPTS_DIR / config.prompts[action]
    prompt_map_path = BASE_DIR / config.projects[project] / ".config" / "prompt-map.json"

    return run_cli(prompt_path, prompt_map_path)


if __name__ == "__main__":
    raise SystemExit(main())