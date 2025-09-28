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
```

# Blog CLI Tool - Part 2: Core Utilities

This is the second part of the modular blog CLI tool implementation.

## Current Implementation

✅ **Completed:** Core Path Handling Module (`core/paths.ps1`)  
✅ **Completed:** Core Clipboard Module (`core/clipboard.ps1`)  
✅ **Completed:** Core Utilities Module (`core/utils.ps1`)

### Features Implemented:

**Clipboard Module:**
- Multi-method clipboard reading (Windows PowerShell, .NET, clip.exe, cross-platform)
- Clipboard writing with fallback methods
- Clipboard content validation with meaningful checks
- Error handling for clipboard access issues

**Utilities Module:**
- Configurable logging with levels and colors
- Item filtering with substring matching
- User confirmation prompts
- File size formatting
- Timestamp generation
- Filename validation and sanitization
- Progress spinner for long operations

### Functions Available:

**Clipboard:**
- `Get-ClipboardText` - Read text from clipboard
- `Set-ClipboardText` - Write text to clipboard  
- `Test-ClipboardText` - Check if clipboard has valid text
- `Validate-ClipboardText` - Validate clipboard content for posting

**Utilities:**
- `Set-LogLevel` - Configure logging verbosity
- `Write-Log` - Consistent logging with colors
- `Filter-Items` - Filter collections by substring
- `Confirm-Action` - Interactive confirmation prompts
- `Format-FileSize` - Human-readable file sizes
- `Get-Timestamp` - Flexible timestamp generation
- `Test-ValidFileName` - Validate filename characters
- `Sanitize-FileName` - Make filenames filesystem-safe
- `Show-Spinner` - Progress indicator for long operations

## Testing

Run the test scripts to verify functionality:

```powershell
# Test paths module (from Part 1)
.\test-paths.ps1

# Test clipboard and utilities modules
.\test-core-utils.ps1
```