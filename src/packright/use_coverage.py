"""Add coverage configuration to pyproject.toml.

Appends [tool.coverage.run] and [tool.coverage.report] sections.
"""

from __future__ import annotations

from pathlib import Path

from packright._config import get_pkg_name, read_project_config
from packright._messages import info, success, warn


def add_coverage(project_dir: str = ".") -> None:
    """Append coverage configuration to pyproject.toml.

    Adds [tool.coverage.run] with source set to the package name and
    [tool.coverage.report] with standard thresholds. Skips if coverage
    config already exists.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    toml_path = root / "pyproject.toml"

    config = read_project_config(project_dir)

    tool = config.get("tool", {})
    if "coverage" in tool:
        warn("[tool.coverage] already exists in pyproject.toml — skipping.")
        return

    pkg_name = get_pkg_name(project_dir)

    coverage_block = (
        "\n"
        "[tool.coverage.run]\n"
        f'source = ["{pkg_name}"]\n'
        "\n"
        "[tool.coverage.report]\n"
        "show_missing = true\n"
        "fail_under = 80\n"
    )

    existing = toml_path.read_text(encoding="utf-8")
    toml_path.write_text(existing + coverage_block, encoding="utf-8")
    success("Added [tool.coverage] configuration to pyproject.toml")
    info('Tip: add "pytest-cov" to your [dependency-groups] dev list.')
