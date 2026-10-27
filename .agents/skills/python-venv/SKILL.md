---
name: python-venv
description: Create and use the project's Python virtual environment. Use before running, testing, linting or installing anything in Python — scripts, pip/uv installs, pytest, FastAPI/Django servers, notebooks, data work — in any project. Never use the global or system Python.
---

# Python virtual environment

Every Python command in a project runs inside its own virtual environment at `.venv` in the project root. This keeps dependencies isolated, reproducible and out of the user's system Python.

## 1. Find or create the environment

Check for an existing environment first and reuse it: `.venv/` (preferred), then `venv/`. Only create one if neither exists.

- **If the project uses uv** (`uv.lock` exists, or `uv` is installed and the user agrees):
  ```bash
  uv venv .venv
  ```
- **Otherwise, standard library venv:**
  ```bash
  python3 -m venv .venv        # macOS / Linux
  py -m venv .venv             # Windows (or: python -m venv .venv)
  ```

Use the Python version the project declares (`.python-version`, `pyproject.toml` `requires-python`, `runtime.txt`) when it is available; say so if it is not installed instead of silently using another version.

## 2. Use the environment's interpreter for every command

Call the venv interpreter directly. This works in every shell and in agent tools where `activate` does not persist between commands:

| OS | Interpreter |
|---|---|
| macOS / Linux | `.venv/bin/python` |
| Windows | `.venv\Scripts\python.exe` |

```bash
.venv/bin/python -m pip install -r requirements.txt     # or: -e . / -e ".[dev]"
.venv/bin/python -m pytest
.venv/bin/python -m uvicorn app.main:app --reload
```

With uv, `uv pip install …` and `uv run …` use `.venv` automatically.

Always invoke tools as modules (`python -m pip`, `python -m pytest`) so they resolve to the venv. If the user prefers an activated shell: `source .venv/bin/activate` (macOS/Linux), `.venv\Scripts\Activate.ps1` (PowerShell), `.venv\Scripts\activate.bat` (cmd).

## 3. Keep it reproducible and out of git

- Make sure `.venv/` (and `venv/`) is in `.gitignore`. Never commit the environment.
- Declare dependencies in `pyproject.toml` or `requirements*.txt` (or `uv.lock`), never only in the environment. Adding a dependency still needs the user's approval (`AGENTS.md`, "Ask first").
- Record the exact setup and test commands in `AGENTS.md` → "Project commands", using the venv interpreter.
- In CI, create a fresh environment (or use the runner's isolated Python) and install from the declared files.

## Never

- `pip install` into the global or system Python, or use `sudo pip`, `pip install --user` or `--break-system-packages`.
- Mix environments: if a command ran with the wrong interpreter, rerun it with `.venv`'s.
- Delete or recreate an existing environment without asking; repair it (`python -m pip install -r …`) instead.
