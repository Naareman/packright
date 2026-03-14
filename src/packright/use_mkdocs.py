"""Add MkDocs documentation scaffolding to an existing project.

Equivalent to usethis::use_pkgdown() in R.
"""

from __future__ import annotations

from pathlib import Path

from packright._config import get_package_name, get_pkg_name
from packright._messages import info, success, warn
from packright._templates import render_template


def add_mkdocs(project_dir: str = ".") -> None:
    """Add MkDocs configuration and starter documentation files.

    Creates mkdocs.yml at the project root, plus docs/index.md and
    docs/api.md using the project's templates.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    name = get_package_name(project_dir)
    pkg_name = get_pkg_name(project_dir)
    context = {"name": name, "pkg_name": pkg_name}

    # Create mkdocs.yml at project root
    mkdocs_path = root / "mkdocs.yml"
    if mkdocs_path.exists():
        warn("mkdocs.yml already exists — skipping.")
        return

    mkdocs_path.write_text(
        render_template("mkdocs.yml.j2", context),
        encoding="utf-8",
    )
    success("Created mkdocs.yml")

    # Create docs/ directory
    docs_dir = root / "docs"
    if not docs_dir.exists():
        docs_dir.mkdir(parents=True)
        info(f"Created {docs_dir.relative_to(root)}/")

    # Create docs/index.md
    _write_if_missing(
        docs_dir / "index.md",
        render_template("docs_index.md.j2", context),
        root,
    )

    # Create docs/api.md
    _write_if_missing(
        docs_dir / "api.md",
        render_template("docs_api.md.j2", context),
        root,
    )

    success("MkDocs setup complete")


def _write_if_missing(path: Path, content: str, root: Path) -> None:
    """Write a file only if it does not already exist.

    Args:
        path: Target file path.
        content: File content to write.
        root: Project root for relative path display.
    """
    if path.exists():
        warn(f"{path.relative_to(root)} already exists — skipping.")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    success(f"Created {path.relative_to(root)}")
