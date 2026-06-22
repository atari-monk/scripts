## Proj Init Script Requirements

### Script Invocation and Input

- Requires a mandatory `ConfigPath` parameter specifying the path to a configuration file.
- Accepts a configuration file path and uses it as the single input to drive all initialization behavior.

### Configuration Loading and Validation

- Reads a JSON configuration file from the provided path.
- Throws an error when the configuration file does not exist.
- Extracts a base path, a list of folder paths, and a list of file paths from the configuration.

### Path Resolution

- Resolves all folder and file paths relative to a configured base path.

### Directory Creation Behavior

- Creates each folder defined in the configuration if it does not already exist.
- Does not modify existing folders when they are already present.
- Prints a message indicating when a folder is created.
- Prints a message indicating when a folder already exists.

### File Creation Behavior

- Creates each file defined in the configuration if it does not already exist.
- Does not modify existing files when they are already present.
- Prints a message indicating when a file is created.
- Prints a message indicating when a file already exists.

### Execution Flow and Completion

- Initializes all folders before creating any files.
- Processes all configured folders and files exactly once per execution.
- Prints a completion message when project initialization finishes successfully.