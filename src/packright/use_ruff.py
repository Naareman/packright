"""Add ruff linter configuration to pyproject.toml.

Appends a [tool.ruff] section with sensible defaults.
"""

from __future__ import annotations

from pathlib import Path

from packright._config import read_project_config
from packright._messages import success, warn


def add_ruff(project_dir: str = ".") -> None:
    """Append ruff configuration to pyproject.toml.

    Adds [tool.ruff] with line-length = 88 and a curated set of lint rules.
    Skips if [tool.ruff] already exists.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    toml_path = root / "pyproject.toml"

    config = read_project_config(project_dir)

    if "tool" in config and "ruff" in config.get("tool", {}):
        warn("[tool.ruff] already exists in pyproject.toml — skipping.")
        return

    ruff_block = (
        "\n"
        "[tool.ruff]\n"
        "line-length = 88\n"
        "\n"
        "[tool.ruff.lint]\n"
        'select = ["E", "F", "I", "UP"]\n'
    )

    existing = toml_path.read_text(encoding="utf-8")
    toml_path.write_text(existing + ruff_block, encoding="utf-8")
    success("Added [tool.ruff] configuration to pyproject.toml")
