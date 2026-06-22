## Install script in bash

Fast and simple way to install py script in bash ?

Fastest simple way: **turn it into a command on your PATH**.

### Option 1 (best): symlink it into `/usr/local/bin`

Assume your script is called `scripts`:

```bash
chmod +x scripts.py
sudo ln -s "$PWD/scripts.py" /usr/local/bin/scripts
```

Now you can run:

```bash
scripts list
scripts mycommand arg1
```

---

### Option 2: install into `~/.local/bin` (no sudo, recommended)

```bash
mkdir -p ~/.local/bin
chmod +x scripts.py
ln -s "$PWD/scripts.py" ~/.local/bin/scripts
```

Make sure `~/.local/bin` is in your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

### Option 3: alias (quick but messy)

```bash
echo "alias scripts='python3 /full/path/to/scripts.py'" >> ~/.bashrc
source ~/.bashrc
```

---

### Recommendation

Use **Option 2**. It’s clean, portable, and doesn’t require root.

---

If you want, I can also show you how to:

* package it as a real CLI (`pip install scripts`)
* add auto-completion for bash/zsh
* or turn your JSON into a plugin system like `git` subcommands
