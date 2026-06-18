## `Scripts` Script

### Goal

Build a lightweight command dispatcher CLI named `scripts` that reads a JSON configuration file and dynamically executes named scripts written in either Python or PowerShell. The tool also supports listing available commands with optional verbosity.

The system acts as a centralized script runner driven entirely by a JSON config file.

---

### Changes Needed

- Add a CLI entrypoint script `scripts.sh` (or equivalent executable) that:
  - Accepts a command name as the first argument
  - Supports a built-in `list` command
  - Loads command definitions from a fixed JSON config file:
    - `$HOME/atari-monk/project/scripts/.config/scripts.json`

- Define a JSON configuration format:
  - Root object contains `commands`
  - Each command has:
    - `language`: `"py"` or `"pwsh"`
    - `script`: absolute or relative path to executable script file
    - `description`: human-readable description

  Example:
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

- Implement command parsing logic:
  - If no command is provided:
    - Print usage instructions
    - Exit with status 1
  - If command is `list`:
    - Support flags:
      - `-v` / `--verbose`
    - Output:
      - Non-verbose: command names only
      - Verbose: `name - description`

- Implement JSON reading (via Python subprocess, no external jq dependency):
  - Read config file
  - Extract `commands` map
  - Support lookup by command name
  - If command not found:
    - Return sentinel output `::NOT_FOUND::`

- Implement execution metadata extraction:
  - For valid command:
    - Output 3 lines from Python helper:
      1. language
      2. script path
      3. description
  - Parse output in bash using line extraction (`sed -n 'Np'`)

- Implement runtime dispatch:
  - Based on `language` field:
    - `"py"` → run script using `python3 <script> "$@"`
    - `"pwsh"` → run script using:
      ```bash
      pwsh -NoProfile -ExecutionPolicy Bypass -File <script> "$@"
      ```

- Add error handling:
  - If command is unknown or config returns invalid data:
    - Print `Unknown command: <cmd>`
    - Exit with status 1
  - If unsupported language:
    - Print `Unsupported language: <lang>`
    - Exit with status 1

- Pass-through argument behavior:
  - All arguments after the command name are forwarded to the target script unchanged.

---

### Acceptance Criteria

- [ ] The CLI accepts a command name and executes the corresponding script defined in a JSON config
- [ ] The CLI supports `list` and `list -v/--verbose`
- [ ] Commands are dynamically loaded from `$HOME/atari-monk/project/scripts/.config/scripts.json`
- [ ] Python is used internally for JSON parsing (no jq dependency)
- [ ] Scripts can be executed in both Python (`py`) and PowerShell (`pwsh`)
- [ ] Unknown commands return a clear error message and exit with status 1
- [ ] Unsupported languages are detected and reported cleanly
- [ ] All extra CLI arguments are forwarded to the executed script unchanged