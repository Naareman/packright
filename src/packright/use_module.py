"""Scaffold new Python modules and their matching test files.

Equivalent to usethis::use_r() / usethis::use_test() in R.
"""

from __future__ import annotations

from pathlib import Path

from packright._config import get_pkg_name
from packright._messages import success, warn
from packright.errors import PackrightError

_MODULE_TEMPLATE = '''\
"""TODO: Add module docstring for {name}."""

from __future__ import annotations
'''

_TEST_TEMPLATE = '''\
"""Tests for {pkg_name}.{name}."""

from __future__ import annotations

from {pkg_name}.{name} import *  # noqa: F403


def test_placeholder() -> None:
    """Placeholder test — replace with real assertions."""
    assert True
'''


def _validate_module_name(name: str) -> None:
    """Validate that name is a safe, valid Python identifier.

    Args:
        name: Module name to validate.

    Raises:
        PackrightError: If name contains path separators or is not a valid identifier.
    """
    forbidden = ("/", "\\", "..")
    for char in forbidden:
        if char in name:
            raise PackrightError(
                f"Invalid module name '{name}': must not contain '{char}'."
            )
    if not name.isidentifier():
        raise PackrightError(
            f"Invalid module name '{name}': must be a valid Python identifier."
        )


def add_module(project_dir: str = ".", name: str = "") -> None:
    """Create a new Python module under ``src/<pkg_name>/<name>.py``.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
        name: Module name (without ``.py`` extension).
    """
    if not name:
        warn("No module name provided.")
        return

    _validate_module_name(name)

    root = Path(project_dir).resolve()
    pkg_name = get_pkg_name(project_dir)
    module_path = root / "src" / pkg_name / f"{name}.py"

    if module_path.exists():
        warn(f"src/{pkg_name}/{name}.py already exists — skipping.")
        return

    module_path.parent.mkdir(parents=True, exist_ok=True)
    module_path.write_text(
        _MODULE_TEMPLATE.format(name=name),
        encoding="utf-8",
    )
    success(f"Created src/{pkg_name}/{name}.py")


def add_test(project_dir: str = ".", name: str = "") -> None:
    """Create a test file at ``tests/test_<name>.py``.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
        name: Module name (without ``test_`` prefix or ``.py`` extension).
    """
    if not name:
        warn("No test name provided.")
        return

    _validate_module_name(name)

    root = Path(project_dir).resolve()
    pkg_name = get_pkg_name(project_dir)
    test_path = root / "tests" / f"test_{name}.py"

    if test_path.exists():
        warn(f"tests/test_{name}.py already exists — skipping.")
        return

    test_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.write_text(
        _TEST_TEMPLATE.format(pkg_name=pkg_name, name=name),
        encoding="utf-8",
    )
    success(f"Created tests/test_{name}.py")


def add_module_with_test(project_dir: str = ".", name: str = "") -> None:
    """Create both a module and its matching test file.

    Calls :func:`add_module` and :func:`add_test` in sequence.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
        name: Module name.
    """
    add_module(project_dir, name)
    add_test(project_dir, name)
