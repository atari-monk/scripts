## File: scripts/bash/scripts.sh

````sh
#!/usr/bin/env bash

set -euo pipefail

CONFIG="$HOME/atari-monk/project/scripts/.config/scripts.json"

CMD="${1:-}"
shift || true

if [[ -z "$CMD" ]]; then
  echo "Usage:"
  echo "  scripts list [-v|--verbose]"
  echo "  scripts <command> [args...]"
  exit 1
fi

# ----------------------------
# JSON reader (NO jq, python)
# ----------------------------
read_json() {
  python3 - "$CONFIG" "$CMD" <<'PY'
import json
import sys

config_path = sys.argv[1]
cmd = sys.argv[2]

with open(config_path, "r", encoding="utf-8") as f:
  data = json.load(f)

commands = data.get("commands", {})

if cmd == "__LIST__":
  verbose = sys.argv[3] == "1"
  for name, meta in commands.items():
    if verbose:
      desc = meta.get("description", "")
      print(f"{name} - {desc}")
    else:
      print(name)
  sys.exit(0)

cmd_data = commands.get(cmd)

if not cmd_data:
  print("::NOT_FOUND::")
  sys.exit(0)

print(cmd_data.get("language", ""))
print(cmd_data.get("script", ""))
print(cmd_data.get("description", ""))
PY
}

# ----------------------------
# LIST MODE
# ----------------------------
if [[ "$CMD" == "list" ]]; then

  LIST_VERBOSE=0

  for arg in "$@"; do
    case "$arg" in
      -v|--verbose)
        LIST_VERBOSE=1
        ;;
    esac
  done

  python3 - "$CONFIG" "$LIST_VERBOSE" <<'PY'
import json
import sys

config_path = sys.argv[1]
verbose = sys.argv[2] == "1"

with open(config_path, "r", encoding="utf-8") as f:
  data = json.load(f)

commands = data.get("commands", {})

for name, meta in commands.items():
  if verbose:
    desc = meta.get("description", "")
    print(f"{name} - {desc}")
  else:
    print(name)
PY

  exit 0
fi

# ----------------------------
# LOAD COMMAND
# ----------------------------
OUTPUT="$(python3 - "$CONFIG" "$CMD" <<'PY'
import json
import sys

config_path = sys.argv[1]
cmd = sys.argv[2]

with open(config_path, "r", encoding="utf-8") as f:
  data = json.load(f)

commands = data.get("commands", {})

if cmd == "__LIST__":
  for name in commands.keys():
    print(name)
  sys.exit(0)

cmd_data = commands.get(cmd)

if not cmd_data:
  print("::NOT_FOUND::")
  sys.exit(0)

print(cmd_data.get("language", ""))
print(cmd_data.get("script", ""))
print(cmd_data.get("description", ""))
PY
)"

LANG="$(echo "$OUTPUT" | sed -n '1p')"
SCRIPT="$(echo "$OUTPUT" | sed -n '2p')"
DESC="$(echo "$OUTPUT" | sed -n '3p')"

if [[ "$LANG" == "::NOT_FOUND::" || -z "$LANG" || -z "$SCRIPT" ]]; then
  echo "Unknown command: $CMD"
  exit 1
fi

run_pwsh() {
  pwsh -NoProfile -ExecutionPolicy Bypass -File "$SCRIPT" "$@"
}

run_py() {
  python3 "$SCRIPT" "$@"
}

case "$LANG" in
  pwsh)
    run_pwsh "$@"
    ;;
  py)
    run_py "$@"
    ;;
  *)
    echo "Unsupported language: $LANG"
    exit 1
    ;;
esac
````