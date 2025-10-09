# nscript.ps1

* Script to quickly create a new PowerShell script from **clipboard content** and register a **PowerShell alias**.
* Goal is to automate the workflow of creating scripts + aliases in one step.

## Cli api

```sh
nscript -FileName <ScriptName.ps1> -AliasName <alias> [-Interactive]
```

### Parameters

* `-FileName` **(required)**: Name of the new PowerShell script file.
* `-AliasName` **(required)**: Alias name that will run the script.
* `-Interactive` *(switch)*: Prompts user to copy content to clipboard and press **Enter** before writing.

Running **`nscript`** with no parameters prints a **help message**.

### Shorter aliases

Provide short switches for speed:

* `-f` → `-FileName`
* `-a` → `-AliasName`
* `-i` → `-Interactive`

Example:

```sh
nscript -f magic.ps1 -a magic -i
```

## Workflow

1. `nscript -f MyScript.ps1 -a myscript`

   * Creates a **new file** in the default scripts folder.
   * Reads **clipboard content** and writes it into the file.
   * Appends a `Set-Alias` command to the PowerShell **$PROFILE** if not already present.
   * Sets the alias in the **current session** so it's ready to run immediately.

2. Optional flags:

   * `-Interactive`
     * Prompts user to **copy content** to the clipboard and press **Enter** before writing to the file.

3. When run without required parameters:

   * Prints usage instructions and examples.
   * Does **not** create any files or aliases.

## Files & Paths

* **Default script folder**
  ```
  C:\Atari-Monk\scripts\scripts
  ```
* All new scripts are saved in this folder unless `-TargetPath` is manually specified in future extensions.
* Aliases are stored in:
  ```
  $PROFILE
  ```
  ensuring persistence across sessions.
