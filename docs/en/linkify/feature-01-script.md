## Linkify Script

### Goal

Converts "Expression1,Expression2,..." to 

```markdown
- [Expression1](#word1-word2-...)\n...
```

### Changes Needed

- Script takes "Expression1,Expression2,..." or "Expression1, Expression2, ..." as arg
- Validate Expression as words with space separator
- Each expression is converted to 

```markdown
- [Expression1](#word1-word2-...)\n...
```

 where words are lowercase words in expression (separated by space)
- Each expression is separate line

### Acceptance Criteria

- [x] Expressions are corectly converted to md links