# Video Log (vid_log) - Specification

## Overview
Command-line utility for logging video entries to structured text files.

## Command Syntax
```bash
vid_log <title> <link> [note] [--pl|--en]
vid_log <date> <title> <link> [note] [--pl|--en]
```

## Features
- Flexible date input (current or specific)
- Multi-language support (EN/PL)
- Automatic text wrapping
- Structured log file format

## Parameters

### Arguments
- `date` - Optional YYYY-MM-DD format date
- `title` - Video title text
- `link` - Video URL
- `note` - Optional multi-line note text

### Flags
- `--en` - Use English log file (default)
- `--pl` - Use Polish log file

## Inputs
- Command-line arguments
- System date/time

## Outputs
- Appends entries to language-specific log files
- Confirmation message with title and date

## Dependencies

### Python Packages
- `pathlib` - File path handling
- `textwrap` - Text formatting
- `datetime` - Date processing

### System Requirements
- Python 3.6+
- Write access to log directory

## Error Handling
- Validates minimum argument count
- Provides usage instructions on error
- Fallback to default language

## Usage Notes
- Creates log files automatically
- Preserves paragraph structure in notes
- Supports UTF-8 characters
