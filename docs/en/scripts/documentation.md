## `Scripts` Script

Scripts CLI dispatcher (bash wrapper for running JSON-defined commands)

### What it does

- Acts as a command dispatcher that reads available commands from a JSON configuration file
- Lets you list available scripts or execute a named script without hardcoding them in bash
- Delegates actual execution to either Python or PowerShell scripts based on metadata in the config

This solves the problem of managing multiple small utility scripts by centralizing their definitions in a single `scripts.json` file, making the system extensible without modifying the dispatcher.

### How to run it

```bash
./scripts.sh list [-v|--verbose]
./scripts.sh <command> [args...]
```

### Inputs

- JSON configuration file:
  - `$HOME/atari-monk/project/scripts/.config/scripts.json`

- Commands:
  - `list` → shows all available commands
  - `<command>` → executes a configured script

- Optional flags (for list mode):
  - `-v` or `--verbose` → show command descriptions

- Script arguments:
  - Any additional arguments are passed directly to the underlying Python or PowerShell script

### Outputs

- `list` mode:
  - Prints command names (or `name - description` in verbose mode)

- execution mode:
  - Runs the selected script and prints its output directly to stdout
  - Errors if:
    - command is not found
    - script language is unsupported
    - required script metadata is missing

### Example

```bash
# List available commands
./scripts.sh list

# List with descriptions
./scripts.sh list --verbose

# Run a configured command
./scripts.sh backup-db

# Run a command with arguments
./scripts.sh resize-images --input ./img --quality 80
```