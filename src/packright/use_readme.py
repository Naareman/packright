"""Add a README.md to an existing project.

Generates a README with badges, installation instructions, and quickstart.
"""

from __future__ import annotations

from pathlib import Path

from packright._config import get_package_name, get_pkg_name, read_project_config
from packright._messages import success, warn
from packright._templates import render_template


def add_readme(project_dir: str = ".") -> None:
    """Create a README.md from the scaffold_readme template.

    Reads the package name and description from pyproject.toml and renders
    a README with badges, install instructions, and a quickstart example.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    readme_path = root / "README.md"

    if readme_path.exists():
        warn("README.md already exists — skipping.")
        return

    name = get_package_name(project_dir)
    pkg_name = get_pkg_name(project_dir)

    config = read_project_config(project_dir)
    description = config.get("project", {}).get(
        "description", "A Python package."
    )

    content = render_template(
        "scaffold_readme.md.j2",
        {
            "name": name,
            "pkg_name": pkg_name,
            "description": description,
        },
    )

    readme_path.write_text(content, encoding="utf-8")
    success("Created README.md")
