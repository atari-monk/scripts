## Prompt Assembler Script Documentation

Template assembler that expands include tokens into file contents and copies the result to clipboard.

### What it does

- Reads a template file containing special include markers in the form `[[key]]`
- Loads a JSON mapping file that defines which files belong to each key
- Resolves file paths (including glob patterns) relative to a configurable root directory
- Replaces each `[[key]]` in the template with the concatenated contents of matching files
- Copies the final assembled output to the system clipboard using `xclip`

This script is typically used to build prompt or document bundles from multiple source files in a reproducible way.

### How to run it

```bash
python assemble_prompt.py TEMPLATE MAP
```

> Requires `xclip` to be installed and available in the system PATH.

### Inputs

- `TEMPLATE`
  - Path to a text template file
  - Contains plain text and include markers like `[[section_name]]`

- `MAP`
  - Path to a JSON mapping file
  - Structure example:
    ```json
    {
      "root": "./base_dir",
      "section_name": [
        "file1.txt",
        "dir/*.md"
      ]
    }
    ```

  - Fields:
    - `root` (optional): base directory for resolving relative paths
    - keys: match include markers in the template
    - values: list of file paths or glob patterns

### Outputs

- Final assembled text is:
  - Printed to the system clipboard (via `xclip -selection clipboard`)
  - Not written to disk unless redirected externally
- Terminal output:
  - `Copied result to clipboard.` on success

### Example

```bash
python assemble_prompt.py prompt_template.txt mapping.json
```