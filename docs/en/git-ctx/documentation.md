## Git Context Script Documentation

Generates a structured Markdown summary of staged, unstaged, and untracked Git changes for a repository and optionally copies it to the clipboard.

### What it does

- Collects Git repository status using `git diff` and related commands
- Separates changes into staged, unstaged, and untracked files
- Converts the result into a readable Markdown report
- Writes the report to a local file inside the repository
- Optionally copies the output to the clipboard using `xclip`

This script is useful for quickly generating a commit-ready context summary, especially when preparing commit messages or reviewing changes.

### How to run it

```bash
python3 git_ctx.py /path/to/repo "Your change description"
```

### Inputs

- `project_path`: Path to the target Git repository
- `description`: Short text describing the changes

Optional dependencies:
- `git` (must be installed and available in PATH)
- `xclip` (optional, for clipboard support on Linux)

### Outputs

- Markdown file written to:
  ```
  <project_path>/.config/_git-changes-context.md
  ```

- Terminal output:
  - Success message with file location
  - Warning if clipboard tool is missing
  - Errors if path is invalid or not a Git repository

- Clipboard (optional):
  - Full Markdown summary copied via `xclip`

### Example

```bash
python3 git_ctx.py ~/projects/my-app "Refactored authentication flow and fixed login bug"
```