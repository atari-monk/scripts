## Prompt Assembler Script Feature 02 - Cli Script

### Goal

Cli tool for running my prompt-assembler script.

### Changes Needed

#### Code

This pseudo code defines what i want:

```sh
base = "$HOME/atari-monk/project"
script = "$base/scripts/scripts/python/prompt-assembler.py"
prompts = "$base/prompts/prompts/"
promptsMap = "$base/prompts/prompts/prompts.json"
projects = "$base/projects.json"
# Select prompt file path by "$prompts/getPromptsMap(action)", action is key to file name with extension
prompt = selectPrompt()
# Select project root folder path by "$base/getProjectsMap(project)", project is key to folder name
project = selectProject()
# Run script with prompt and project
python3 $script $prompt $project 
# Command format
prompt action project
# Prompt prints help with list of acions and projects
prompt
```

#### Configs

projects.json:

```json
{
"dev-notes":"dev-notes",
"prompts":"prompts",
"scripts":"scripts",
"ts-library":"ts-library"
}
```

prompts.json:

```json
{
"requirements": "requirements.md",
"requirements_reverse": "requirements-reverse.md",
"feature": "feature.md",
"feature_reverse": "feature-reverse.md",
"implementation": "implementation.md",
"code": "code-files.md",
"documentation": "documentation.md",
"commit_message": "commit-message.md",
"explanation": "explanation.md",
"translation_en_pl": "translation-en-pl.md"
}
```

### Acceptance Criteria

- [ ] `prompt action project` works in terminal
- [ ] `prompt` prints help with list of actions and projects