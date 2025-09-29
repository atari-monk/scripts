# Blog CLI Tool Specification

## 1. Overview / Purpose

**Goal:** Provide a **high-level, semi-automated CLI tool** to manage multiple blogs efficiently, directly from the console.

**Key Features:**

* Create posts from clipboard text.
* Browse categories and files recursively.
* Edit and delete posts.
* Integrate existing indexing and GitHub deployment scripts.
* Enable high-level, console-driven workflow without manual clicking.

**Workflow Example:**
Clipboard → `post` → `index` → `push` → blog updated on GitHub Pages.

---

## 2. Architecture / Modular Layout

### Entry Point

* **CLI script** (`blog.ps1` or `blog.py`) invoked from the console.
* Parses commands and flags and routes to the corresponding module/function.

### Modules

1. **Core Module**

   * Handle paths, categories, nested folder resolution.
   * Clipboard operations.
   * Shared utilities (logging, error handling, filtering).

2. **Commands Module**

   * `list`: recursive category listing, optional filtering, optional file listing.
   * `post`: create a post from clipboard in specified category.
   * `files`: list files in a category.
   * `edit`: open a file in system editor.
   * `delete`: remove a file (with confirmation).
   * `index`: invoke existing indexing script.
   * `push`: invoke REST script to deploy to GitHub.

3. **Integration Module**

   * External scripts for indexing and GitHub push.
   * Handles errors from external scripts gracefully.

4. **Configuration**

   * Blog roots (paths).
   * Default editor.
   * Optional flags for automatic indexing and GitHub push.

---

## 3. Commands Specification

### 3.1 `list`

```sh
blog list <blog-name> [--filter text] [--show-files]
```

* Lists all categories recursively.
* `--filter`: optional substring filter for category names.
* `--show-files`: optionally list `.md` files in categories.
* Example:

```
programming/
programming/python/
ideas/
```

### 3.2 `post`

```sh
blog post <blog-name> <category-path> <file-name>
```

* Creates a new post from clipboard.
* Automatically creates missing category folders.
* Triggers indexing and/or GitHub push if configured.
* Validates clipboard content and file existence.

### 3.3 `files`

```sh
blog files <blog-name> <category-path> [--filter text]
```

* Lists markdown files in a specific category.
* Optional filter.

### 3.4 `edit`

```sh
blog edit <blog-name> <category-path> <file-name>
```

* Opens the file in system editor (`$EDITOR`, `code`, `notepad`, configurable).
* Edits modify the file in place.
* Optionally triggers indexing after save.

### 3.5 `delete`

```sh
blog delete <blog-name> <category-path> <file-name> [--force]
```

* Deletes a post with confirmation.
* `--force` skips confirmation.
* Optionally remove empty folders after deletion.

### 3.6 `index`

```sh
blog index <blog-name>
```

* Invokes the existing indexing script for the specified blog.

### 3.7 `push`

```sh
blog push <blog-name>
```

* Invokes REST script to push blog to GitHub Pages.

---

## 4. Data / Paths

* Blog roots:

  * `C:\Atari-Monk\dev-blog\content`
  * `C:\Atari-Monk\mind-dump\content`
* Supports **nested folder structure** freely.
* Categories are folders; posts are `.md` files inside categories.

---

## 5. Integration

* **Indexing:** call existing script automatically after `post`, optionally after `edit` or `delete`.
* **GitHub push:** call REST script automatically after `post` or via explicit `push` command.
* Both scripts configurable; errors handled gracefully.

---

## 6. Error Handling

* Missing clipboard content → error message, abort post.
* Invalid blog name, category, or file → descriptive error.
* File conflicts → warn or abort.
* External script failures → logged, does not crash CLI.

---

## 7. High-Level Workflow Examples

1. **Add new post and update blog**

```sh
blog post dev-blog programming/python new-tips
# optional automatic index + push
```

2. **Browse and edit a post**

```sh
blog list dev-blog --filter python
blog files dev-blog programming/python
blog edit dev-blog programming/python new-tips
```

3. **Delete a post**

```sh
blog delete dev-blog programming/python old-post
```

4. **Manual index and push**

```sh
blog index dev-blog
blog push dev-blog
```

---

## 8. Extensibility

* Add new commands by creating modules/functions in the Commands Module.
* Configure multiple blogs easily via Blog Roots in configuration.
* Editor and integration scripts can be changed without modifying core logic.
* Designed to scale: recursive category handling, filtering, automation.

---

✅ This document can now serve as the **driving specification** for the implementation of the modular blog CLI tool.

---
