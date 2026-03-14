"""Package scaffolding — the "whole game."

This is the Python equivalent of R's usethis::create_package().
Creates a complete, working package structure in one call.
"""

from __future__ import annotations

from pathlib import Path

from packright._messages import info, success
from packright._templates import render_template
from packright.errors import FileExistsError, ScaffoldError


def create_package(name: str, parent: str = ".") -> Path:
    """Create a new Python package following all conventions.

    Args:
        name: Package name (e.g., "my-analytics-lib"). Will be normalized
            to a valid Python package name (hyphens become underscores).
        parent: Parent directory to create the package in. Defaults to ".".

    Returns:
        Path to the created package directory.

    Raises:
        FileExistsError: If the target directory already exists.
        ScaffoldError: If the package cannot be created.
    """
    pkg_name = _normalize_name(name)
    pkg_dir = Path(parent).resolve() / name

    if pkg_dir.exists():
        raise FileExistsError(
            f"Directory '{pkg_dir}' already exists.",
            path=str(pkg_dir),
        )

    info(f"Package name: [bold]{name}[/bold] (import as [bold]{pkg_name}[/bold])")

    try:
        _create_structure(pkg_dir, name, pkg_name)
    except OSError as e:
        raise ScaffoldError(
            f"Failed to create package: {e}",
            path=str(pkg_dir),
        ) from e

    return pkg_dir


def _normalize_name(name: str) -> str:
    """Convert a package name to a valid Python identifier.

    Args:
        name: Package name (e.g., "my-analytics-lib").

    Returns:
        Normalized name (e.g., "my_analytics_lib").
    """
    return name.replace("-", "_").replace(" ", "_").lower()


def _create_structure(pkg_dir: Path, name: str, pkg_name: str) -> None:
    """Create the full directory tree and all files."""
    context = {"name": name, "pkg_name": pkg_name}

    # Directories
    src_dir = pkg_dir / "src" / pkg_name
    tests_dir = pkg_dir / "tests"
    docs_dir = pkg_dir / "docs"

    src_dir.mkdir(parents=True)
    tests_dir.mkdir(parents=True)
    docs_dir.mkdir(parents=True)

    # Config files
    _write(pkg_dir / "pyproject.toml", render_template("pyproject.toml.j2", context))
    _write(pkg_dir / "README.md", render_template("README.md.j2", context))
    _write(pkg_dir / "CHANGELOG.md", render_template("CHANGELOG.md.j2", context))
    _write(pkg_dir / "LICENSE", render_template("LICENSE.j2", context))
    _write(pkg_dir / ".gitignore", render_template("gitignore.j2", context))
    _write(pkg_dir / ".python-version", "3.12\n")
    _write(pkg_dir / "mkdocs.yml", render_template("mkdocs.yml.j2", context))

    # Source files
    _write(src_dir / "__init__.py", render_template("__init__.py.j2", context))
    _write(src_dir / "py.typed", "")
    _write(src_dir / "errors.py", render_template("errors.py.j2", context))
    _write(src_dir / "_messages.py", render_template("_messages.py.j2", context))
    _write(src_dir / "core.py", render_template("core.py.j2", context))

    # Test files
    _write(tests_dir / "conftest.py", render_template("conftest.py.j2", context))
    _write(tests_dir / "test_core.py", render_template("test_core.py.j2", context))

    # Doc files
    _write(docs_dir / "index.md", render_template("docs_index.md.j2", context))
    _write(docs_dir / "api.md", render_template("docs_api.md.j2", context))

    success(f"Created {_count_files(pkg_dir)} files")


def _write(path: Path, content: str) -> None:
    """Write content to a file, creating parent dirs if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    info(f"  Created {path.relative_to(path.parent.parent.parent) if len(path.parts) > 3 else path.name}")


def _count_files(directory: Path) -> int:
    """Count all files in a directory tree."""
    return sum(1 for _ in directory.rglob("*") if _.is_file())
