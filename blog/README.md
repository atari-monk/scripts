# Blog CLI Tool - Part 1: Core Path Handling

This is the first part of the modular blog CLI tool implementation.

## Current Implementation

✅ **Completed:** Core Path Handling Module (`core/paths.ps1`)

### Features Implemented:

- Blog root configuration for `dev-blog` and `mind-dump`
- Category path resolution with security validation
- Category existence checking and creation
- Recursive subcategory discovery
- File listing in categories
- File path resolution with .md extension handling
- Comprehensive error handling

### Functions Available:

- `Get-BlogRoot` - Get root path for a blog
- `Resolve-CategoryPath` - Resolve full path for a category
- `Test-CategoryExists` - Check if category exists
- `Ensure-CategoryExists` - Create category if missing
- `Get-Subcategories` - List subcategories (recursive or flat)
- `Get-FilesInCategory` - List files in a category
- `Resolve-FilePath` - Resolve full path for a file
- `Test-FileExists` - Check if file exists

## Testing

Run the test script to verify the paths module:

```powershell
.\test-paths.ps1
