#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import sys
import subprocess
from typing import TypedDict, Dict, List, Optional, Literal


# ----------------------------
# Typed configuration schema
# ----------------------------

class CommandMeta(TypedDict, total=False):
    language: str
    script: str
    description: str


class Config(TypedDict):
    commands: Dict[str, CommandMeta]


Language = Literal["py", "pwsh"]


CONFIG_PATH: str = os.path.expanduser(
    "~/atari-monk/project/scripts/.config/scripts.json"
)


# ----------------------------
# Load config (strict)
# ----------------------------

def load_config() -> Config:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise TypeError("Config root must be a dict")

    commands = data.get("commands", {}) # type: ignore
    if not isinstance(commands, dict):
        raise TypeError("config.commands must be a dict")

    return {"commands": commands}


# ----------------------------
# Core helpers
# ----------------------------

def list_commands(config: Config, verbose: bool) -> None:
    for name, meta in config["commands"].items():
        if verbose:
            desc: str = meta.get("description", "")
            print(f"{name} - {desc}")
        else:
            print(name)


def get_command(config: Config, name: str) -> Optional[CommandMeta]:
    return config["commands"].get(name)


def run_pwsh(script: str, args: List[str]) -> None:
    subprocess.run(
        ["pwsh", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script, *args],
        check=True,
    )


def run_py(script: str, args: List[str]) -> None:
    subprocess.run(
        ["python3", script, *args],
        check=True,
    )


def parse_language(value: str) -> Optional[Language]:
    if value in ("py", "pwsh"):
        return value  # type: ignore[return-value]
    return None


# ----------------------------
# Main
# ----------------------------

def main(argv: List[str]) -> None:
    if len(argv) < 2:
        print("Usage:")
        print("  scripts list [-v|--verbose]")
        print("  scripts <command> [args...]")
        raise SystemExit(1)

    cmd: str = argv[1]
    args: List[str] = argv[2:]

    config: Config = load_config()

    
    # ----------------------------
    # LIST MODE
    # ----------------------------
    if cmd == "list":
        verbose: bool = any(a in ("-v", "--verbose") for a in args)
        list_commands(config, verbose)
        return

    # ----------------------------
    # COMMAND LOOKUP
    # ----------------------------
    meta: Optional[CommandMeta] = get_command(config, cmd)

    if meta is None:
        print(f"Unknown command: {cmd}")
        raise SystemExit(1)

    language_raw: str = meta.get("language", "")
    script: str = meta.get("script", "")
    _desc: str = meta.get("description", "")

    language: Optional[Language] = parse_language(language_raw)

    if language is None:
        print(f"Unsupported language: {language_raw}")
        raise SystemExit(1)

    if not script:
        print("Invalid command configuration: missing script")
        raise SystemExit(1)

    # ----------------------------
    # EXECUTION
    # ----------------------------
    if language == "pwsh":
        run_pwsh(script, args)
    elif language == "py":
        run_py(script, args)
    else:
        # Exhaustiveness check
        raise AssertionError("Unreachable")


if __name__ == "__main__":
    main(sys.argv)