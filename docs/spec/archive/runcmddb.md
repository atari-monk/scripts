# runcmddb

- PowerShell script to launch development environment for a project
- Kills existing Meilisearch processes and starts fresh instances of Meilisearch and Next.js development servers

## CLI API Definition

```ps1
runcmddb
```

## Script Behavior

1. **Terminates existing Meilisearch processes**
   - Identifies all running `meilisearch` processes
   - Forcefully stops each process with confirmation message

2. **Launches Meilisearch server**
   - Opens new PowerShell window with Meilisearch executable
   - Sets database path to `./data.ms`
   - Window remains open (`-NoExit` flag)

3. **Launches Next.js development server**
   - Opens separate PowerShell window with `pnpm dev` command
   - Window remains open for development usage

## Configuration Variables

- `$ProjectPath`: Root directory of the project (`C:/Atari-Monk/command-box`)
- `$MeilisearchExe`: Meilisearch executable filename (`meilisearch.exe`)

## Requirements

- **PowerShell** execution privileges
- **Meilisearch** executable available in project path
- **Node.js** and **pnpm** installed for Next.js development
- Project structure:
  ```
  C:/Atari-Monk/command-box/
  ├── meilisearch.exe
  ├── data.ms/ (directory, created by Meilisearch)
  └── package.json (for pnpm dev)
  ```

## Output

- Process termination messages
- Two separate console windows for each service
- Confirmation message in original PowerShell window

## Usage Notes

- Script is designed for Windows PowerShell environment
- Both launched windows remain open for monitoring logs
- Meilisearch data persists in `./data.ms` directory
- Next.js server runs on default development port (usually 3000)

## Misc Notes

- Once Meilisearch version changes and data.ms with indexes were removed
    - They were restored by edit save on each command