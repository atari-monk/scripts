## Git Context Script Requirements

### Command-Line Interface

* Accepts a required `project_path` argument pointing to a target directory.
* Accepts a required `description` argument describing the changes.
* Resolves the provided project path to an absolute path before processing.

### Repository Validation

* Displays an error and exits if the provided path does not exist.
* Displays an error and exits if the provided path is not a valid Git repository.
* Uses Git commands to determine repository validity.

### Git Change Detection (Staged Changes)

* Retrieves staged file changes from the Git repository.
* Categorizes staged changes into human-readable types: Added, Modified, Deleted, Renamed, and Copied.
* Falls back to a raw status value when a change type is not recognized.
* Produces no staged-change entries when no staged changes exist.

### Git Change Detection (Unstaged Changes)

* Retrieves unstaged file changes from the Git repository.
* Includes modifications and deletions in unstaged changes.
* Labels unknown or unrecognized change types using their raw status indicator.
* Produces no unstaged-change entries when no unstaged changes exist.

### Untracked File Detection

* Retrieves untracked files from the Git repository.
* Includes untracked files in the unstaged changes section labeled as “Untracked”.
* Displays no untracked entries when none are present.

### Markdown Summary Generation

* Generates a Markdown-formatted summary of Git changes.
* Includes the provided description in the output.
* Separates content into staged changes and unstaged changes sections.
* Formats each file entry as a bullet point with its change type and file path.
* Displays a placeholder message when no staged or unstaged changes exist.

### Output File Generation

* Writes the generated Markdown summary to `.config/_git-changes-context.md` within the target project directory.
* Creates the `.config` directory if it does not already exist.
* Prints the output file location after writing.

### Clipboard Integration

* Attempts to copy the generated Markdown summary to the system clipboard using `xclip`.
* Prints a success message when clipboard copying succeeds.
* Prints a warning message if clipboard functionality is unavailable.

### Error Handling

* Handles unexpected runtime errors gracefully.
* Prints error messages to standard error output.
* Exits with a non-zero status code on failure conditions.