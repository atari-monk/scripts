## Scripts Repository

### Structure

- Repository name - `scripts`
- `README` required
  - One-sentence description in English and Polish
- Repository for single-file, standalone scripts (ps1, js, py)
- Use [kebab-case](https://atari-monk.github.io/dev-notes/en/convention/naming.html) for all folders and files

- /scripts/ → all executable scripts
  - subfolders by language or purpose (optional):
    - /scripts/python/
    - /scripts/powershell/
    - /scripts/js/

- /docs/ → documentation (GitHub Pages source)

- Root → repository metadata and build/config files only (no executable scripts)
  (e.g. README, LICENSE, CI, package configs)

### Commits

- [Commit Message](https://atari-monk.github.io/dev-notes/en/convention/commit-message.html)
- [Feature-Centric Commits](https://atari-monk.github.io/dev-notes/en/convention/feature-commits.html)