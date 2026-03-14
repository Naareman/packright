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

This creates a complete package with `src/` layout, `errors.py`, `_messages.py`, tests, docs, CI — all conventions in place, passing 22/22 checks.

## Commands

### Create

| Command | What it does |
|---|---|
| `packright scaffold <name>` | Create a complete package from scratch |
| `packright init` | Interactive project setup (prompts for name, author, license) |
| `packright use-module <name>` | Create a paired module + test file |

### Configure

| Command | What it does |
|---|---|
| `packright use-pytest` | Add pytest config + test structure |
| `packright use-mkdocs` | Add mkdocs-material documentation |
| `packright use-pre-commit` | Add pre-commit hooks (ruff, mypy) |
| `packright use-ruff` | Add ruff linter/formatter config |
| `packright use-mypy` | Add mypy strict config + py.typed |
| `packright use-coverage` | Add coverage.py config |
| `packright use-rich` | Add `_messages.py` for structured output |
| `packright use-errors` | Add `errors.py` exception hierarchy |

### Integrate

| Command | What it does |
|---|---|
| `packright use-github-actions` | Add CI, release, and docs workflows |
| `packright use-gitlab-ci` | Add GitLab CI pipeline |
| `packright use-git` | Init git + .gitignore + initial commit |
| `packright use-github` | Create GitHub repo via `gh` CLI |
| `packright use-docker` | Add Dockerfile + .dockerignore |

### Manage

| Command | What it does |
|---|---|
| `packright use-license` | Add LICENSE file (MIT) |
| `packright use-readme` | Generate README with badges |
| `packright use-changelog` | Add CHANGELOG.md |
| `packright use-contributing` | CONTRIBUTING + CODE_OF_CONDUCT + issue templates |
| `packright use-dep <name>` | Add a dependency |
| `packright use-dev-dep <name>` | Add a dev dependency |
| `packright bump-version <part>` | Bump version (major/minor/patch) |

### Inspect

| Command | What it does |
|---|---|
| `packright check` | Audit project against 22 conventions |
| `packright doctor` | Check development environment (uv, git, gh, ruff) |
| `packright browse-pypi` | Open PyPI page in browser |
| `packright browse-github` | Open GitHub repo in browser |
| `packright browse-docs` | Open docs site in browser |

## Examples

```bash
# Start from scratch
packright scaffold my-lib
cd my-lib

# Or add to an existing project piece by piece
packright use-pytest
packright use-ruff
packright use-pre-commit
packright use-github-actions

# Check what's missing
packright check

# Add a new feature module
packright use-module auth

# Bump version and release
packright bump-version minor
git tag v0.2.0
git push --tags  # CI publishes to PyPI
```

## Philosophy

packright follows the [python-package-development](https://github.com/Naareman/python-package-development) skill conventions — 5 principles from R's package ecosystem applied to Python:

1. **User communication is first-class** — `rich`, not `print()`
2. **Function names form a grammar** — `verb_noun()` patterns
3. **Lifecycle deserves ceremony** — formal deprecation process
4. **Documentation lives next to code** — Google docstrings + mkdocs
5. **There is a whole game** — scaffold first, refine later
