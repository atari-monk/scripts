## Linkify Script

linkify.py — converts comma-separated text expressions into Markdown anchor-style link items.

### What it does

- Takes command-line input, treating it as a comma-separated list of expressions
- Validates that each expression contains only alphabetic words (no numbers or symbols)
- Converts each expression into a Markdown list item with an internal anchor link
- Generates a URL-friendly slug from each expression
- Prints the resulting Markdown to stdout

This script is useful for quickly generating a table-of-contents-style list from plain text phrases, where each item links to an internal section anchor.

### How to run it

```bash
python linkify.py "First Item, Second Item, Third Item"
```

### Inputs

- Command-line arguments (joined into a single string)
- Expressions separated by commas

  - Example input string:
    - `"Getting Started, Installation Guide, Usage Notes"`

### Outputs

- Printed Markdown list (one item per line)
- Each line has the format:
  - `- [Expression](#expression-slug)`
- Output is written to standard output (console)

### Example

```bash
python linkify.py "Hello World, Data Pipeline, API Reference"
```