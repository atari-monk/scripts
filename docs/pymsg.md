# pymsg

- Script to extract and format messages from JSON clipboard data
- Parses JSON from clipboard, extracts messages with file locations, and copies formatted results back to clipboard

## CLI API Definition

```sh
pymsg                    # extracts messages from JSON in clipboard
```

## Input Requirements

- Clipboard must contain valid JSON data
- JSON should be an array of objects with message information
- Expected object structure:
  ```json
  [
    {
      "message": "Error message text",
      "resource": "/path/to/file.py",
      "startLineNumber": 10,
      "startColumn": 5
    }
  ]
  ```

## Output Format

- Each message is formatted as: `filename:line:column: message`
- Results are copied back to clipboard as newline-separated strings
- Example output:
  ```
  script.py:10:5: Syntax error
  utils.py:25:1: Undefined variable
  main.py:3:15: Import error
  ```

## Error Handling

- Exits with error code 1 for:
  - Empty clipboard
  - Invalid JSON format
  - Other processing errors
- Provides descriptive error messages

## Dependencies

- `pyperclip` - Clipboard operations
- `json` - JSON parsing
- `sys` - System operations and exit codes
- `os` - File path operations
- `typing` - Type hints