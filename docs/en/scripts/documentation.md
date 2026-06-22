## `Scripts` Script Documentation

Config-driven script runner for Python and PowerShell commands

### What it does

- Loads a JSON configuration file defining executable commands and their metadata
- Provides a simple CLI to list available commands or execute them by name
- Dispatches execution to either Python or PowerShell based on configuration
- Standardizes running local scripts behind a single unified interface

This script is useful when you want a single entry point (`scripts`) to manage multiple utility scripts without remembering their file paths or execution details.

### How to run it

```bash
python3 scripts.py list
python3 scripts.py list --verbose
python3 scripts.py <command> [args...]
```

### Inputs

- CLI arguments:
  - `list` — shows available commands
  - `<command>` — name of a configured command from the config file
  - optional flags:
    - `-v`, `--verbose` (for list mode)
  - optional positional arguments passed to the target script
- Configuration file:
  - `~/atari-monk/project/scripts/.config/scripts.json`

  Expected structure:
  ```json
  {
    "commands": {
      "example": {
        "language": "py",
        "script": "/path/to/script.py",
        "description": "Example script"
      }
    }
  }
  ```

### Outputs

- Prints a list of available commands (with optional descriptions in verbose mode)
- Executes the selected script and streams its output directly to the terminal
- Returns exit code 1 on:
  - missing or invalid command
  - unsupported language
  - malformed configuration
- Returns script-specific output and exit status for executed commands

### Example

```bash
python3 scripts.py list --verbose
python3 scripts.py backup_db
python3 scripts.py deploy staging
```