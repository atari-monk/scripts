# `Scripts` Script, Feature 01 - Script

## Goal

Build a lightweight command dispatcher CLI named `scripts` implemented in Python. It reads a JSON configuration file and dynamically executes named scripts written in either Python or PowerShell. It also supports listing available commands.

The system acts as a centralized script runner driven entirely by a JSON config file.

---

## Command Interface

The CLI is executed as:

```bash
scripts <command> [args...]
```

### Built-in commands

* `list`
* `list -v` / `list --verbose`

---

## Configuration

The CLI loads commands from a fixed JSON file:

```
$HOME/atari-monk/project/scripts/.config/scripts.json
```

### Format

```json
{
  "commands": {
    "hello": {
      "language": "py",
      "script": "/path/to/hello.py",
      "description": "Prints hello world"
    }
  }
}
```

### Command schema

Each command must define:

* `language`: `"py"` or `"pwsh"`
* `script`: path to executable script
* `description`: human-readable description

---

## Behavior

### 1. No arguments

If no command is provided:

* Print usage instructions
* Exit with status `1`

---

### 2. List command

#### `scripts list`

Prints all available command names.

#### `scripts list -v | --verbose`

Prints:

```
name - description
```

---

### 3. Command execution

If a command is provided:

* Load config
* Resolve command by name

#### If command is not found

* Print:

  ```
  Unknown command: <cmd>
  ```
* Exit with status `1`

---

### 4. Command validation

If command exists but is invalid:

* Missing `script` → error + exit `1`
* Unsupported `language` → error:

  ```
  Unsupported language: <lang>
  ```

  Exit `1`

---

### 5. Execution dispatch

#### Python scripts

```bash
python3 <script> <args...>
```

#### PowerShell scripts

```bash
pwsh -NoProfile -ExecutionPolicy Bypass -File <script> <args...>
```

All arguments after the command name are forwarded unchanged.

---

## Error Handling

The CLI must:

* Fail fast on invalid configuration
* Provide clear error messages
* Exit with status `1` on all errors

---

## Removed Legacy Requirements (No longer applicable)

The following original spec requirements are intentionally removed:

* Bash-based `scripts.sh` entrypoint
* Python subprocess-based JSON parsing
* 3-line metadata extraction protocol
* `sed`-based parsing logic
* `::NOT_FOUND::` sentinel output

---

## Acceptance Criteria

* [x] CLI accepts a command name and executes mapped script from JSON config
* [x] Supports `list` and `list -v/--verbose`
* [x] Loads commands from `$HOME/atari-monk/project/scripts/.config/scripts.json`
* [x] Uses Python-native JSON parsing
* [x] Executes Python and PowerShell scripts correctly
* [x] Unknown commands produce clear error and exit 1
* [x] Unsupported languages are detected and reported
* [x] Extra CLI arguments are forwarded unchanged
* [x] No Bash dependency required for execution flow