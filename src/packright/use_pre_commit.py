"""Add pre-commit configuration to an existing project.

Equivalent to usethis::use_tidy_style() in R.
"""

from __future__ import annotations

from pathlib import Path

from packright._messages import success, warn

_PRE_COMMIT_CONFIG = """\
# See https://pre-commit.com for more information
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: []
"""


def add_pre_commit(project_dir: str = ".") -> None:
    """Add a .pre-commit-config.yaml with ruff, mypy, and standard hooks.

    The configuration includes:
    - pre-commit-hooks (trailing whitespace, EOF fixer, YAML check, large files)
    - ruff (lint with --fix, and format)
    - mypy (type checking)

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    config_path = root / ".pre-commit-config.yaml"

    if config_path.exists():
        warn(".pre-commit-config.yaml already exists — skipping.")
        return

    config_path.write_text(_PRE_COMMIT_CONFIG, encoding="utf-8")
    success("Created .pre-commit-config.yaml")
    success("pre-commit setup complete")
