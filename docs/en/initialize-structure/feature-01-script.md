## Initialize Structure Script Feature 01 - Script

### Goal

Implement a command-line utility that initializes a project directory structure based on a JSON configuration file. The tool should create a set of folders and files under a specified base path, ensuring idempotent behavior (existing files/folders are not overwritten), and provide console feedback for each operation.

### Changes Needed

- Add a CLI entrypoint that accepts a single mandatory parameter: `ConfigPath` (path to a JSON configuration file).
- Add configuration loading logic that:
  - Validates the existence of the config file.
  - Parses JSON into an internal configuration model with:
    - `basePath` (string)
    - `folders` (string array of relative paths)
    - `files` (string array of relative paths)
- Add path resolution utility:
  - Join `basePath` with each relative folder/file path into a full filesystem path.
- Add folder initialization logic:
  - Create directories if they do not exist.
  - Skip creation if already present.
  - Log status messages to console.
- Add file initialization logic:
  - Create files if they do not exist.
  - Skip creation if already present.
  - Log status messages to console.
- Add orchestration layer (`main` function equivalent) that:
  - Loads configuration
  - Initializes folders
  - Initializes files
  - Prints completion message
- Ensure all operations are safe to re-run (idempotent behavior).

### Implementation Blueprint

#### 1. Configuration Schema
Expected JSON structure:
```json
{
  "basePath": "string",
  "folders": ["relative/path/one", "relative/path/two"],
  "files": ["relative/file1.txt", "relative/file2.txt"]
}
```

#### 2. Core Components

**Config Loader**
- Input: `ConfigPath`
- Steps:
  - Check file existence
  - Read entire file content
  - Parse JSON
  - Map to internal structure:
    - basePath
    - folders[]
    - files[]
- Error handling:
  - Throw error if file does not exist

**Path Resolver**
- Input: `basePath`, `relativePath`
- Output: absolute/combined filesystem path
- Behavior:
  - Use standard path join semantics (OS-safe)

**Folder Creator**
- Input: full folder path
- Behavior:
  - If path does not exist as directory → create it
  - If exists → do nothing
  - Print:
    - "Created folder: X"
    - or "Folder already exists: X"

**File Creator**
- Input: full file path
- Behavior:
  - If file does not exist → create empty file
  - If exists → do nothing
  - Print:
    - "Created file: X"
    - or "File already exists: X"

#### 3. Initialization Flow

1. Parse CLI argument `ConfigPath`
2. Load configuration
3. For each folder in config:
   - Resolve full path
   - Create folder if needed
4. For each file in config:
   - Resolve full path
   - Create file if needed
5. Print completion message:
   - "Init project complete"

#### 4. Execution Behavior

- Must be runnable as a standalone script.
- Must support repeated execution without side effects beyond missing structure creation.
- Must not overwrite existing files or directories.

### Acceptance Criteria

- [ ] Script accepts a required `ConfigPath` argument and fails if not provided.
- [ ] Script validates existence of configuration file before execution.
- [ ] JSON configuration is correctly parsed into `basePath`, `folders`, and `files`.
- [ ] All folder paths are created relative to `basePath`.
- [ ] All file paths are created relative to `basePath`.
- [ ] Existing folders are not recreated or modified.
- [ ] Existing files are not overwritten.
- [ ] Console output is produced for every create/skip action.
- [ ] Script prints "Init project complete" after successful execution.
- [ ] Entire process is idempotent across multiple runs.