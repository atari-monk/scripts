# projlog.py

- Tool for logging about projects

## Cli api definition

```sh
projlog # shows usage
projlog -h # shows usage
projlog -p 1 # prints 1 last record
projlog -s scripts "note" # adds record for proj 'scripts' with optional note
projlog -n "note" # adds note to last record
projlog -e "note" # closes record by adding time, duration and optional note
```

## File

Path for storage file:  
"C:/Atari-Monk/logs/proj-log-2025.txt"  

Examples of records.  

Record after -s:

```txt
2025-09-24 18:36  scripts
Refine somescript.py
```

Record after -s, -n, -e

```txt
2025-09-24 15:00-16:30 1h30m scripts
Refine somescript.py
Renamed to path2md.py
scripts\path2md.py quality assured
```

## Edge Cases/Fixes

These are probably already fixed but make sure

### 0m

- When 0m there is a gap "  " beetween time and proj name, we should state 0m

```txt
2025-09-24 21:43-21:43  test
test
test

2025-09-24 21:43-21:44 1m test
test
test
```

### Note on -s and -e

- When we invoke -s or -e note must be optional !
- In help it should be [-e END [NOTE ...]] !
- Cant invoke 'projlog -e' ! 