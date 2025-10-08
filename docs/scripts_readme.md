# scripts_readme.py

- Script to generate README documentation from JSON command data
- Creates organized markdown documentation with command reference tables

## Actual Usage

```sh
scripts_readme                    # Generate README with default paths
scripts_readme -i input.json      # Use custom input JSON file
scripts_readme -o output.md       # Use custom output markdown file
scripts_readme -i input.json -o output.md  # Custom both files
```

## Default Paths
- **Input**: `C:/Atari-Monk/scripts/data/info.json`
- **Output**: `C:/Atari-Monk/scripts/README.md`

## What it actually does:

1. **Loads JSON data** from specified input file
2. **Groups commands by category** from the JSON structure
3. **Generates markdown** with:
   - Title and timestamp
   - Table of contents with category links
   - Command tables organized by category
4. **Saves to output file** as formatted README

## JSON Format Expected:
```json
{
    "commands": [
        {
            "alias": "command_name",
            "description": "Command description",
            "category": "CategoryName"
        }
    ]
}
```

## Features:
- Automatic command categorization
- Alphabetical sorting of categories and commands
- Clean markdown table formatting
- Error handling for missing files and invalid JSON
- Type-safe Python implementation
