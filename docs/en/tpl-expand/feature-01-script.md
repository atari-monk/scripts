## Template Expand Script

### Goal

Script to inject code in placeholders [[include:path]]

### Changes Needed

- Take a path to template file
- Load template file and inject code to it
- Save file in same path, same name as template but remove _ form name
- Dont use regex, write simple parser

### Acceptance Criteria

- [x] File generates proper md with injected code