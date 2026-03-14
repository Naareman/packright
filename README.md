# packright

Automate Python package development the right way — inspired by R's `usethis`.

## Installation

```bash
pip install packright
```

## Quickstart

```bash
# Create a new package with all conventions in place
packright scaffold my-analytics-lib
cd my-analytics-lib
uv sync
uv run pytest
```

This creates a complete package with:
- `src/` layout with `__init__.py`, `errors.py`, `_messages.py`, `core.py`
- `py.typed` marker for type checkers
- `pyproject.toml` with hatchling, ruff, pytest, mypy
- PEP 735 `[dependency-groups]` for dev deps
- `tests/` with conftest.py and starter tests
- `mkdocs.yml` with mkdocs-material + mkdocstrings
- `CHANGELOG.md`, `LICENSE`, `.gitignore`, `.python-version`

## Philosophy

packright follows the [python-package-development](https://github.com/Naareman/python-package-development) skill conventions — 5 principles from R's package ecosystem applied to Python:

1. **User communication is first-class** — `rich`, not `print()`
2. **Function names form a grammar** — `verb_noun()` patterns
3. **Lifecycle deserves ceremony** — formal deprecation process
4. **Documentation lives next to code** — Google docstrings + mkdocs
5. **There is a whole game** — scaffold first, refine later
