## Commit Info Script Feature 01 - Script

### Goal

Build a CLI utility that inspects a local Git repository and generates a human-readable Markdown summary of the working directory state (staged changes, unstaged changes, and untracked files). The tool writes the summary to a project-local file and optionally copies it to the system clipboard.

---

### Changes Needed

- Add a CLI entrypoint (`main`) that accepts:
  - `project_path` (path to a Git repository)
  - `description` (free-text explanation of changes)

- Add Git execution abstraction:
  - Implement a helper to run Git commands via `subprocess.Popen`
  - Must support:
    - capturing stdout/stderr
    - returning exit code
    - executing commands in a specified repository directory

- Add repository validation:
  - Verify the path exists on disk
  - Verify it is a Git repository using `git rev-parse --git-dir`

- Implement change collection features:
  - **Staged changes**
    - Use `git diff --cached --name-status`
    - Parse output lines formatted as:
      - `<status>\t<filepath>`
    - Map statuses:
      - `A → Added`
      - `M → Modified`
      - `D → Deleted`
      - `R → Renamed`
      - `C → Copied`
  - **Unstaged changes**
    - Use `git diff --name-status`
    - Map statuses:
      - `M → Modified`
      - `D → Deleted`
  - **Untracked files**
    - Use `git ls-files --others --exclude-standard`
    - Split output into a list of file paths

- Implement Markdown generator:
  - Output structure:
    - Title: `# Git Changes Context`
    - Description section
    - Staged changes section (bullet list or “No staged changes”)
    - Unstaged changes section
      - Merge unstaged modified/deleted files with untracked files labeled as `Untracked`
  - Format each item as:
    - `**<ChangeType>**: \`filepath\``

- Implement file output:
  - Create directory: `<project_path>/.config/`
  - Write output file:
    - `<project_path>/.config/_git-changes-context.md`
  - Overwrite existing file if present
  - Print confirmation with file path

- Implement clipboard support:
  - Attempt to copy final Markdown using `xclip -selection clipboard`
  - If successful: print success message
  - If `xclip` is missing: print warning to stderr (non-fatal)

- Add robust error handling:
  - Exit with non-zero status on:
    - invalid path
    - non-git repository
    - unexpected runtime errors
  - Print errors to stderr

---

### Acceptance Criteria

- [ ] Running the CLI with a valid Git repository path generates a Markdown summary of repository changes
- [ ] Staged, unstaged, and untracked files are correctly categorized and displayed
- [ ] Output file is created at `.config/_git-changes-context.md` inside the target repository
- [ ] The summary includes the user-provided description
- [ ] The tool correctly maps Git status codes into human-readable labels
- [ ] The tool gracefully handles empty change sets
- [ ] The tool attempts to copy output to clipboard using `xclip`
- [ ] Missing `xclip` does not crash the program
- [ ] Invalid paths or non-git directories cause a clean exit with error messages