# entry.py Specification

* Default path is `C:/Atari-Monk/scripts/scripts`.
* Accepts an optional path argument: a **file or a directory**.
* Processes `.py` and `.ps1` files.
* Ignores `__init__.py`.
* Produces output in two formats:

For Python files:

```txt
script_name = "scripts.script_name:main"
```

For PowerShell files:

```txt
Set-Alias -Name script_name -Value "full_path_to_script.ps1"
```

* Preserves **folder order**.
* Prints **all `.py` lines first**, then `.ps1` lines, including nested directories.
* Contains a `main()` function so the script can be run as a **console script** or **standalone**.
* No interactive flag (`-i`) — simply run with a file or directory path or use the default.
* Fully self-documenting code; no comments.

---
