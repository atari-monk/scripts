## Prompt Assembler Script Feature 01 - Script

### Goal

Build a CLI tool that assembles a final text prompt by:

* Parsing a template containing special include markers (`[[key]]`)
* Resolving each key against a JSON mapping file
* Expanding each key into one or more file contents (via paths or glob patterns)
* Concatenating everything into a single output string
* Copying the final result directly to the system clipboard (via `xclip`)

The system is designed for prompt composition workflows where reusable file groups (e.g., code snippets, docs, context packs) are dynamically injected into a template.

---

### Changes Needed

#### 1. Template Parsing Engine

Add logic to parse a raw template string and split it into ordered tokens of two types:

* **Literal text segments**
* **Include directives** in the form `[[key]]`

Rules:

* `[[key]]` marks an include block
* Whitespace inside keys is trimmed
* If `[[` appears without a matching `]]`, raise `ValueError("Unclosed include: missing ']]'")`
* Output must preserve original ordering of text and includes

Output structure:

```python
list[tuple[bool, str]]
# (is_include, value)
```

Where:

* `is_include = False` → raw text
* `is_include = True` → mapping key

---

#### 2. Mapping File Resolution

Introduce a JSON mapping file with structure:

```json
{
  "root": "/base/path",
  "some_key": [
    "path/or/pattern1",
    "path/or/pattern2"
  ]
}
```

Behavior:

* `root` defines base directory for relative paths (defaults to mapping file directory)
* Each key maps to a list of file entries:

  * absolute paths
  * relative paths (resolved against root)
  * glob patterns (supports `**` recursive matching)
* Empty or missing lists should be ignored during expansion

---

#### 3. File Group Resolution System

Implement a function to resolve each include key into a block of file contents.

For each mapping entry:

* Strip whitespace
* Resolve path relative to `root` if not absolute
* Expand glob patterns using `glob(..., recursive=True)`
* If no glob matches:

  * treat as direct file path if it exists

Then:

* Deduplicate all matched files
* Sort them (lexicographically by Path)
* Filter out non-files
* Read file contents as UTF-8

Output format per file:

```
# File: <file_path>
<file contents>
```

Join all file blocks using:

```
"\n\n"
```

---

#### 4. Template Assembly Engine

Core function:

```python
assemble(template_path: Path, mapping_path: Path) -> str
```

Workflow:

1. Load template file (UTF-8)
2. Load mapping JSON
3. Determine root path:

   * mapping["root"] if present
   * else mapping file directory
4. Parse template into tokens
5. For each token:

   * If literal → append directly
   * If include:

     * fetch mapping entries
     * skip if missing or empty
     * expand via file resolver
     * append expanded content
6. Return final concatenated string (no extra delimiter between tokens)

---

#### 5. CLI Interface

Add command-line entrypoint:

```bash
python assemble_prompt.py TEMPLATE MAP
```

Behavior:

* Validate argument count (must be exactly 2)
* Call `assemble()`
* Send result to clipboard using:

```bash
xclip -selection clipboard
```

via:

```python
subprocess.run(..., input=result, text=True, shell=True, check=True)
```

* Print confirmation:

```
Copied result to clipboard.
```

* Exit codes:

  * `0` success
  * `1` incorrect usage

---

#### 6. Error Handling

* Missing CLI args → print usage to stderr, exit 1
* Unclosed `[[...]]` → raise `ValueError`
* Missing files → silently ignored unless they resolve via glob or exist check
* Missing mapping key → treated as no-op (skip include)

---

### Acceptance Criteria

* [ ] Template strings containing `[[key]]` are correctly parsed into text + include tokens in order
* [ ] Mapping JSON correctly resolves include keys into file lists
* [ ] Glob patterns (`*`, `**`) are expanded recursively
* [ ] Files are deduplicated and sorted before reading
* [ ] Each file is prefixed with `# File: <path>` in output
* [ ] UTF-8 file contents are correctly concatenated with blank-line separation
* [ ] Missing or empty mapping entries are safely skipped
* [ ] Unclosed include markers raise a clear exception
* [ ] CLI correctly assembles output from template + mapping
* [ ] Final output is copied to clipboard via `xclip`
* [ ] Program exits with correct status codes and prints confirmation message