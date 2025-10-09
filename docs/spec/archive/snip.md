# snip.py

- Collect snippets from clipboard or files into a Markdown file and back to clip

## Cli api definition

```sh
snip # shows usage
snip -h # shows usage
snip add [file] # collect clipboard or optionaly a file
snip show # prints current collection
snip clear # clears collection
snip copy [--keep] # copy collection to clipboard, clears collection or not if --keep used
```

## File

Content is put in markdown blocks with language label
