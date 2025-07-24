# 'scripts'

A simple Python package with console entry points, installed as a development package locally.

---

## 📦 Install locally (editable mode)

First, navigate to the project root and run:

```bash
pip install -e .
```

This installs your package in **editable mode**, so changes to the code are picked up immediately.

---

## 🚀 Run the console scripts

After installing, you can run the CLI commands you defined:

```bash
# Runs script1's main()
myscript

# Runs script2's main() with an argument
otherscript YourName
```

Example output:

```bash
$ myscript
Running as a script:
Hello from script1!

$ otherscript Bob
Hello, Bob!
```

---

## ✅ Run tests

If you added tests, you can run them with:

```bash
pytest
```

---

## 📂 Project structure

```
your_project/
├── mypackage/
│   ├── __init__.py
│   ├── script1.py
│   └── script2.py
├── tests/
│   └── test_script1.py
├── pyproject.toml
└── README.md
```

---

## 📝 How it works

* The **package code** is in `mypackage/`.
* Entry points (`myscript`, `otherscript`) are defined in `pyproject.toml` under `[project.scripts]`.
* `pip install -e .` installs the package with console scripts.
* `pytest` runs your tests.

---

## 🔗 Example `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
description = "A simple example Python package with CLI entry points"
authors = [
  { name = "Your Name", email = "you@example.com" }
]
dependencies = []

[project.optional-dependencies]
dev = ["pytest"]

[project.scripts]
myscript = "mypackage.script1:main"
otherscript = "mypackage.script2:main"

[tool.setuptools.packages.find]
where = ["."]
```

---

## ✅ That’s it!

You now have a simple, reusable Python package with an easy CLI.
Happy coding! 🚀
