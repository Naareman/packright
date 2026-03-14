"""Add pytest configuration and test scaffolding to an existing project.

Equivalent to usethis::use_testthat() in R.
"""

from __future__ import annotations

from pathlib import Path

from packright._config import get_package_name, get_pkg_name, read_project_config
from packright._messages import info, success, warn
from packright._templates import render_template


def add_pytest(project_dir: str = ".") -> None:
    """Add pytest configuration, test directory, and starter test files.

    Reads pyproject.toml to detect the package name, then:
    - Appends [tool.pytest.ini_options] to pyproject.toml (if missing)
    - Creates tests/ directory (if missing)
    - Creates tests/conftest.py (if missing)
    - Creates tests/test_core.py (if missing)

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    name = get_package_name(project_dir)
    pkg_name = get_pkg_name(project_dir)
    config = read_project_config(project_dir)

    # Check if pytest config already exists
    if "tool" in config and "pytest" in config["tool"]:
        warn("[tool.pytest.ini_options] already exists in pyproject.toml — skipping config.")
    else:
        _append_pytest_config(root, pkg_name)
        success("Added [tool.pytest.ini_options] to pyproject.toml")

    # Create tests/ directory
    tests_dir = root / "tests"
    if not tests_dir.exists():
        tests_dir.mkdir(parents=True)
        info(f"Created {tests_dir.relative_to(root)}/")

    # Create conftest.py
    context = {"name": name, "pkg_name": pkg_name}
    _write_if_missing(
        tests_dir / "conftest.py",
        render_template("conftest.py.j2", context),
        root,
    )

    # Create test_core.py
    _write_if_missing(
        tests_dir / "test_core.py",
        render_template("test_core.py.j2", context),
        root,
    )

    success("pytest setup complete")


def _append_pytest_config(root: Path, pkg_name: str) -> None:
    """Append [tool.pytest.ini_options] section to pyproject.toml.

    Args:
        root: Project root directory.
        pkg_name: Normalized importable package name.
    """
    toml_path = root / "pyproject.toml"
    existing = toml_path.read_text(encoding="utf-8")

    pytest_section = (
        "\n[tool.pytest.ini_options]\n"
        'testpaths = ["tests"]\n'
        f'addopts = "--cov={pkg_name} --cov-report=term-missing"\n'
    )

    toml_path.write_text(existing.rstrip("\n") + "\n" + pytest_section, encoding="utf-8")


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
