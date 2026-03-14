"""Tests for packright.use_mypy."""

from __future__ import annotations

from pathlib import Path

from packright.use_mypy import add_mypy


def test_add_mypy_appends_config(minimal_project: Path) -> None:
    """Verify that add_mypy adds [tool.mypy] to pyproject.toml."""
    add_mypy(str(minimal_project))

    content = (minimal_project / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.mypy]" in content
    assert "strict = true" in content
    assert 'python_version = "3.10"' in content


def test_add_mypy_creates_py_typed(minimal_project: Path) -> None:
    """Verify that add_mypy creates py.typed if not present."""
    # Remove the existing py.typed that minimal_project creates
    py_typed = minimal_project / "src" / "test_pkg" / "py.typed"
    py_typed.unlink()
    assert not py_typed.exists()

    add_mypy(str(minimal_project))

    assert py_typed.exists(), "py.typed should be created"


def test_add_mypy_skips_if_exists(minimal_project: Path) -> None:
    """Verify that add_mypy skips if [tool.mypy] already in pyproject.toml."""
    # Add [tool.mypy] manually
    pyproject = minimal_project / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")
    content += "\n[tool.mypy]\nstrict = false\n"
    pyproject.write_text(content, encoding="utf-8")

    original = pyproject.read_text(encoding="utf-8")

    add_mypy(str(minimal_project))

    assert pyproject.read_text(encoding="utf-8") == original, (
        "add_mypy should not modify pyproject.toml when [tool.mypy] exists"
    )


def test_add_mypy_keeps_existing_py_typed(minimal_project: Path) -> None:
    """Verify that add_mypy does not overwrite an existing py.typed."""
    py_typed = minimal_project / "src" / "test_pkg" / "py.typed"
    # py.typed already exists from minimal_project fixture

    add_mypy(str(minimal_project))

    assert py_typed.exists(), "py.typed should still exist"
