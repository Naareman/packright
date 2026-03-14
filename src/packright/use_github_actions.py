"""Add GitHub Actions CI/CD workflows to an existing project.

Creates workflows for testing, releasing, and documentation deployment.
"""

from __future__ import annotations

from pathlib import Path

from packright._messages import info, success, warn

_CI_YML = """\
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --group dev

      - name: Lint
        run: uv run ruff check .

      - name: Type check
        run: uv run mypy src/

      - name: Test
        run: uv run pytest
"""

_RELEASE_YML = """\
name: Release

on:
  push:
    tags:
      - "v*"

permissions:
  id-token: write

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4

      - name: Build
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
"""

_DOCS_YML = """\
name: Docs

on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --group dev

      - name: Deploy docs
        run: uv run mkdocs gh-deploy --force
"""


def add_github_actions(project_dir: str = ".") -> None:
    """Add GitHub Actions workflows for CI, release, and docs deployment.

    Creates three workflow files under .github/workflows/:
    - ci.yml: Run tests on push/PR with Python 3.10-3.12 matrix using uv
    - release.yml: Publish to PyPI on v* tags using trusted publishing
    - docs.yml: Deploy MkDocs to GitHub Pages on push to main

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    workflows_dir = root / ".github" / "workflows"

    if not workflows_dir.exists():
        workflows_dir.mkdir(parents=True)
        info(f"Created {workflows_dir.relative_to(root)}/")

    workflows = {
        "ci.yml": _CI_YML,
        "release.yml": _RELEASE_YML,
        "docs.yml": _DOCS_YML,
    }

    created = 0
    for filename, content in workflows.items():
        path = workflows_dir / filename
        if path.exists():
            warn(f"{path.relative_to(root)} already exists — skipping.")
            continue
        path.write_text(content, encoding="utf-8")
        success(f"Created {path.relative_to(root)}")
        created += 1

    if created > 0:
        success("GitHub Actions setup complete")
    else:
        info("All workflow files already exist — nothing to do.")
