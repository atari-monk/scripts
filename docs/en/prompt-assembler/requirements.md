## Prompt Assembler Script Requirements

Extracted from code.

### Command-Line Interface Behavior

- The program must be executed with exactly two command-line arguments: a template file path and a mapping JSON file path.
- If the required arguments are not provided, the program must print a usage message to standard error and exit with a non-zero status code.
- When executed correctly, the program must process the template and mapping files and produce a single assembled output.
- After successful processing, the program must print a confirmation message indicating that the result was copied to the clipboard.
- The program must exit with status code 0 upon successful completion.

### Template Include Parsing Behavior

- The program must treat occurrences of `[[key]]` in the template as include directives.
- Any text outside `[[...]]` delimiters must be preserved exactly as literal output content.
- The program must split the template into alternating literal segments and include tokens based on `[[` and `]]` markers.
- Whitespace inside include keys must be trimmed before processing.
- If an opening `[[` is found without a matching closing `]]`, the program must raise an error and stop execution.
- Malformed or unclosed include directives must prevent successful assembly.

### Mapping Resolution Behavior

- Each include key in the template must be resolved using a JSON mapping file.
- If a key is not present in the mapping or maps to an empty/whitespace-only list, the include must be skipped and produce no output.
- The mapping file may define a `root` directory used as the base path for resolving file references.
- If no `root` is provided, the mapping root must default to the directory containing the mapping file.

### File Resolution and Group Expansion Behavior

- Each mapping entry must represent a file path or glob pattern.
- Relative file paths must be resolved relative to the configured root directory.
- Absolute file paths must be used as provided without modification.
- Glob patterns must be expanded recursively to match filesystem files.
- If a glob pattern produces matches, all matched files must be included.
- If no glob matches are found, the program must treat the entry as a literal path and include it only if it exists.
- Only existing regular files must be included in the output; directories must be ignored.
- Duplicate file paths must be removed so each file is included at most once.
- The final set of files must be sorted before inclusion to ensure deterministic output.

### File Content Formatting Behavior

- Each included file must be preceded by a header line in the format `# File: <file path>`.
- The full UTF-8 content of each file must be included after its header.
- Each file block must be separated from other blocks using two newline characters.
- The final expanded include content must preserve the original file text without modification.

### Assembly Output Behavior

- The final output must be constructed by concatenating literal template segments and expanded include content in order.
- Include blocks must be replaced entirely by their resolved file content.
- Literal text segments from the template must remain unchanged in the final output.
- The final assembled string must be a single continuous text result.

### Clipboard Output Behavior

- After assembling the final output, the program must copy the result to the system clipboard using `xclip` with the `-selection clipboard` option.
- The assembled text must be passed to the clipboard command via standard input.
- The clipboard operation must be executed as a shell command and must succeed for the program to complete successfully.
- If the clipboard operation fails, the program must terminate with a non-zero exit code.

### Error Handling Behavior

- Missing closing include delimiters must raise a runtime error and stop execution.
- Failure of the clipboard command must cause the program to fail.
- Invalid command-line usage must result in an error message and non-zero exit code.