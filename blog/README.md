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

# Blog CLI Tool - Part 3: List and Files Commands

This is the third part of the modular blog CLI tool implementation.

## Current Implementation

✅ **Completed:** Core Path Handling Module (`core/paths.ps1`)  
✅ **Completed:** Core Clipboard Module (`core/clipboard.ps1`)  
✅ **Completed:** Core Utilities Module (`core/utils.ps1`)  
✅ **Completed:** List Command Module (`commands/list.ps1`)  
✅ **Completed:** Files Command Module (`commands/files.ps1`)

### Features Implemented:

**List Command:**
- Recursive category listing with tree display
- Text filtering for category names
- Optional file listing within categories
- Hierarchical tree formatting with emojis
- Summary statistics

**Files Command:**
- File listing in specific categories
- File metadata (size, modification date)
- Text filtering for file names
- Formatted table display
- Quick action suggestions

### Functions Available:

**List Command:**
- `List-Categories` - Main listing function with all options
- `Format-CategoryTree` - Internal tree formatting
- `Show-ListHelp` - Command help display

**Files Command:**
- `List-Files` - Main file listing function
- `Format-FileList` - File metadata formatting
- `Display-FileTable` - Table display formatter
- `Show-FilesHelp` - Command help display

## Testing

Run the test scripts to verify functionality:

```powershell
# Test core modules
.\test-paths.ps1
.\test-core-utils.ps1

# Test command modules
.\test-commands.ps1
```

## Usage Examples

```powershell
# Browse categories
blog list dev-blog
blog list dev-blog --filter python
blog list dev-blog --show-files

# Browse files
blog files dev-blog programming
blog files dev-blog programming/python --filter tips
```

# Blog CLI Tool - Part 4: Post and Edit Commands

This is the fourth part of the modular blog CLI tool implementation.

## Current Implementation

✅ **Completed:** Core Path Handling Module (`core/paths.ps1`)  
✅ **Completed:** Core Clipboard Module (`core/clipboard.ps1`)  
✅ **Completed:** Core Utilities Module (`core/utils.ps1`)  
✅ **Completed:** List Command Module (`commands/list.ps1`)  
✅ **Completed:** Files Command Module (`commands/files.ps1`)  
✅ **Completed:** Post Command Module (`commands/post.ps1`)  
✅ **Completed:** Edit Command Module (`commands/edit.ps1`)

### Features Implemented:

**Post Command:**
- Clipboard content validation and reading
- YAML front matter generation with metadata
- Automatic category creation
- File conflict detection and overwrite protection
- Content formatting and statistics
- Force mode for overwriting existing files

**Edit Command:**
- System editor auto-detection (VS Code, Notepad++, etc.)
- Editor fallback chain with environment variable support
- File metadata display before/after editing
- Wait for editor completion
- File change statistics

### Functions Available:

**Post Command:**
- `Post-FromClipboard` - Main post creation function
- `New-PostContent` - Content formatting with YAML front matter
- `Test-PostCreation` - Pre-creation validation
- `Show-PostHelp` - Command help display

**Edit Command:**
- `Edit-File` - Main file editing function
- `Open-FileInEditor` - Editor launching with file handling
- `Get-SystemEditor` - Editor auto-detection
- `Show-EditHelp` - Command help display

## Testing

Run the test scripts to verify functionality:

```powershell
# Test core modules
.\test-paths.ps1
.\test-core-utils.ps1

# Test command modules
.\test-commands.ps1
.\test-post-edit.ps1
```

## Usage Examples

```powershell
# Create new posts
blog post dev-blog programming python-tips
blog post mind-dump ideas new-idea --force
blog post dev-blog javascript tips --auto-push

# Edit existing posts
blog edit dev-blog programming python-tips
blog edit mind-dump ideas my-idea --editor code
blog edit dev-blog javascript notes --no-index
```

## Workflow Example

```powershell
# 1. Copy content to clipboard
# 2. Create post from clipboard
blog post dev-blog programming new-article

# 3. Edit the post if needed
blog edit dev-blog programming new-article

# 4. Browse to verify
blog list dev-blog --show-files
```

# Blog CLI Tool - Part 5: Delete Command

This is the fifth part of the modular blog CLI tool implementation.

## Current Implementation

✅ **Completed:** Core Path Handling Module (`core/paths.psm1`)  
✅ **Completed:** Core Clipboard Module (`core/clipboard.psm1`)  
✅ **Completed:** Core Utilities Module (`core/utils.psm1`)  
✅ **Completed:** List Command Module (`commands/list.psm1`)  
✅ **Completed:** Files Command Module (`commands/files.psm1`)  
✅ **Completed:** Post Command Module (`commands/post.psm1`)  
✅ **Completed:** Edit Command Module (`commands/edit.psm1`)  
✅ **Completed:** Delete Command Module (`commands/delete.psm1`)

### Features Implemented:

**Delete Command:**
- Comprehensive file information display before deletion
- Safety confirmation prompts (can be bypassed with --force)
- File preview showing first few lines of content
- Automatic cleanup of empty categories after deletion
- Detailed metadata display (size, dates, line/word counts)
- Protection against accidental deletion

### Functions Available:

**Delete Command:**
- `Delete-File` - Main deletion function with all safety features
- `Get-FileInfoForDeletion` - File metadata retrieval
- `Show-DeletionSummary` - Detailed pre-deletion information display
- `Remove-EmptyCategory` - Automatic cleanup of empty folders
- `Show-DeleteHelp` - Command help display

## Testing

Run the test scripts to verify functionality:

```powershell
# Test core modules
.\test-paths.ps1
.\test-core-utils.ps1

# Test command modules
.\test-commands.ps1
.\test-post-edit.ps1
.\test-delete.ps1
```

## Usage Examples

```powershell
# Safe deletion with confirmation
blog delete dev-blog programming old-post

# Force deletion (no confirmation)
blog delete mind-dump ideas temp-idea --force

# Delete without cleaning up empty categories
blog delete dev-blog test sample --no-cleanup
```

## Safety Features

- **Confirmation prompts** for all deletions (unless --force)
- **File preview** shows content before deletion
- **Metadata display** with size, dates, and statistics
- **Empty category cleanup** maintains clean folder structure
- **Clear warnings** about irreversibility

