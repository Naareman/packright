"""Tests for packright.use_pytest."""

from __future__ import annotations

from pathlib import Path

from packright.use_pytest import add_pytest


def test_add_pytest_creates_test_dir(minimal_project: Path) -> None:
    """Verify that add_pytest creates a tests/ directory."""
    add_pytest(str(minimal_project))

    tests_dir = minimal_project / "tests"
    assert tests_dir.is_dir(), "tests/ directory should be created"


def test_add_pytest_creates_conftest(minimal_project: Path) -> None:
    """Verify that add_pytest creates a tests/conftest.py file."""
    add_pytest(str(minimal_project))

    conftest = minimal_project / "tests" / "conftest.py"
    assert conftest.exists(), "tests/conftest.py should be created"
    content = conftest.read_text(encoding="utf-8")
    assert len(content) > 0, "conftest.py should not be empty"


def test_add_pytest_adds_config_to_pyproject(minimal_project: Path) -> None:
    """Verify that pytest config is added to pyproject.toml."""
    add_pytest(str(minimal_project))

    pyproject = minimal_project / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")
    assert "pytest" in content.lower(), (
        "pyproject.toml should reference pytest after add_pytest"
    )


def test_add_pytest_skips_if_already_configured(
    minimal_project: Path,
    capsys: object,
) -> None:
    """Verify that calling add_pytest twice warns and does not overwrite."""
    add_pytest(str(minimal_project))

    # Capture state after first call
    conftest = minimal_project / "tests" / "conftest.py"
    original_content = conftest.read_text(encoding="utf-8")

    # Call again — should skip gracefully
    add_pytest(str(minimal_project))

    # Content should be unchanged
    assert conftest.read_text(encoding="utf-8") == original_content, (
        "add_pytest should not overwrite existing conftest.py"
    )
