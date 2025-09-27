# Blog CLI Tool — Modular Layout

## 1️⃣ Folder Structure

```
blog-cli/
│
├── blog.ps1                  # CLI entry point (routes commands to modules)
├── core/
│   ├── paths.ps1             # Handles blog roots, category resolution, nested folders
│   ├── clipboard.ps1         # Clipboard operations (read/write)
│   ├── utils.ps1             # Logging, filtering, validation, error handling
│
├── commands/
│   ├── list.ps1              # Recursive category listing, optional filtering/files
│   ├── post.ps1              # Create new post from clipboard
│   ├── files.ps1             # List files in a category
│   ├── edit.ps1              # Open file in system editor
│   ├── delete.ps1            # Delete a file
│   ├── index.ps1             # Invoke indexing script
│   ├── push.ps1              # Invoke GitHub push script
│
├── integration/
│   ├── indexing.ps1          # Wrapper to invoke external indexing script
│   ├── github.ps1            # Wrapper to invoke REST push script
│
├── config.ps1                # Configurable settings: blog roots, default editor, flags
└── README.md                 # Markdown specification and usage instructions
```

> This layout keeps **core utilities** separate from **command logic**, and all **integration scripts** in their own folder.

---

## 2️⃣ Module Responsibilities

### Core

| Module          | Responsibility                                                     |
| --------------- | ------------------------------------------------------------------ |
| `paths.ps1`     | Resolve blog roots, handle nested categories, check/create folders |
| `clipboard.ps1` | Read/write clipboard content, validate non-empty                   |
| `utils.ps1`     | Logging, filtering, input validation, common error messages        |

### Commands

| Command      | Responsibility                                                                      |
| ------------ | ----------------------------------------------------------------------------------- |
| `list.ps1`   | Recursive category listing, optional filter, optional show files                    |
| `post.ps1`   | Save clipboard content as new `.md` post, auto-create folders, trigger integrations |
| `files.ps1`  | List files in a category, optional filter                                           |
| `edit.ps1`   | Open post in system editor                                                          |
| `delete.ps1` | Delete post (confirmation/force), optionally remove empty folders                   |
| `index.ps1`  | Invoke indexing script                                                              |
| `push.ps1`   | Invoke GitHub push script                                                           |

### Integration

| Module         | Responsibility                                              |
| -------------- | ----------------------------------------------------------- |
| `indexing.ps1` | Wrapper to call the existing indexing script, handle errors |
| `github.ps1`   | Wrapper to call REST push script, handle errors             |

---

## 3️⃣ Function Signatures (Example)

### Core Functions

```powershell
# core/paths.ps1
function Get-BlogRoot(`$blogName) { ... }
function Resolve-CategoryPath(`$blogName, `$categoryPath) { ... }

# core/clipboard.ps1
function Get-ClipboardText() { ... }
function Validate-ClipboardText(`$text) { ... }

# core/utils.ps1
function Write-Log(`$message) { ... }
function Filter-Items(`$items, `$filterText) { ... }
function Confirm-Action(`$message) { ... }
```

### Command Functions

```powershell
# commands/list.ps1
function List-Categories(`$blogName, `$filterText = "", `$showFiles = `$false) { ... }

# commands/post.ps1
function Post-FromClipboard(`$blogName, `$categoryPath, `$fileName) { ... }

# commands/files.ps1
function List-Files(`$blogName, `$categoryPath, `$filterText = "") { ... }

# commands/edit.ps1
function Edit-File(`$blogName, `$categoryPath, `$fileName) { ... }

# commands/delete.ps1
function Delete-File(`$blogName, `$categoryPath, `$fileName, `$force = `$false) { ... }

# commands/index.ps1
function Invoke-Index(`$blogName) { ... }

# commands/push.ps1
function Invoke-Push(`$blogName) { ... }
```

### Integration Functions

```powershell
# integration/indexing.ps1
function Run-IndexingScript(`$blogPath) { ... }

# integration/github.ps1
function Run-GitHubPushScript(`$blogPath) { ... }
```

---

## 4️⃣ CLI Entry Point

* `blog.ps1` parses the command and routes to the appropriate module function:

```powershell
param(`$Command, `$Args)

switch (`$Command) {
    "list"   { List-Categories @Args }
    "post"   { Post-FromClipboard @Args }
    "files"  { List-Files @Args }
    "edit"   { Edit-File @Args }
    "delete" { Delete-File @Args }
    "index"  { Invoke-Index @Args }
    "push"   { Invoke-Push @Args }
    default  { Show-Help }
}
```

* If no command is provided, prints **help message**.

---

## 5️⃣ Advantages of Modular Layout

* Easier to maintain and extend (add new commands, new integrations).
* Clear separation of concerns (core utilities, command logic, external integrations).
* Can support pipelines, semi-automation, and multiple blogs without rewriting code.
* Easy to test modules independently.

---

At this point, we have:

1. **Markdown spec** for behavior and workflow.
2. **Modular folder layout** and responsibilities.
3. **Function signatures** for all commands and core utilities.

---
