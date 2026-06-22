## Proj Init Script Documentation

Initialize project structure (folders and files) from a JSON configuration.

### What it does

- Reads a JSON configuration file describing a project structure
- Creates a set of folders and files under a base directory
- Ensures existing folders/files are not recreated
- Prints status messages for each created or existing item

This script is useful for quickly scaffolding a project layout in a consistent and repeatable way.

### How to run it

```bash
powershell -File proj-init.ps1 -ConfigPath path/to/config.json
```

### Inputs

- A JSON configuration file passed via `-ConfigPath`
- JSON structure example:
  - `basePath`: root directory for the project
  - `folders`: array of folder paths relative to `basePath`
  - `files`: array of file paths relative to `basePath`

Example:

- `config.json`

### Outputs

- Creates folders under the specified `basePath`
- Creates files under the specified `basePath`
- Console output indicating:
  - Created folder/file paths
  - Existing folder/file notices
  - Completion message: `Init project complete`

### Example

```bash
powershell -File proj-init.ps1 -ConfigPath .\config.json
```