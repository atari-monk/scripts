## *Tiny bash wrapper* for ergonomics

Right now you have a working Python CLI (`prompt.py`). That already *is* the tool. You can run it directly like:

```sh
python3 ~/atari-monk/project/scripts/scripts/python/prompt.py feature dev-notes
```

---

### Why people add bash anyway

Because you want this UX:

```sh
prompt feature dev-notes
```

instead of:

```sh
python3 /long/path/to/script.py feature dev-notes
```

---

### Best practice (clean + minimal)

#### 1. Keep Python as the real CLI (you already have it)

#### 2. Add a tiny bash shim

Create:

```sh
~/atari-monk/project/scripts/scripts/bash/prompt
```

```bash
#!/usr/bin/env bash

BASE="$HOME/atari-monk/project"
SCRIPT="$BASE/scripts/scripts/python/prompt.py"

python3 "$SCRIPT" "$@"
```

Make it executable:

```sh
chmod +x ~/atari-monk/project/scripts/scripts/bash/prompt
```

---

#### 3. Add to PATH (in `.bashrc` or `.zshrc`)

```sh
code ~/.bashrc
```

```sh
export PATH="$HOME/atari-monk/project/scripts/scripts/bash:$PATH"
```

---

### Result

Now this works everywhere:

```sh
prompt feature dev-notes
prompt
```

and your Python script still handles:

* validation
* help output
* config loading
* execution

---