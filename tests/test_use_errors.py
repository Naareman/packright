"""Tests for packright.use_errors."""

from __future__ import annotations

from pathlib import Path


def test_add_errors_creates_errors_module(minimal_project: Path) -> None:
    """add_errors() creates errors.py in the package directory."""
    from packright.use_errors import add_errors

    add_errors(project_dir=str(minimal_project))

    errors_py = minimal_project / "src" / "test_pkg" / "errors.py"
    assert errors_py.exists()
    content = errors_py.read_text()
    assert "TestPkgError" in content
    assert "Exception" in content


def test_add_errors_uses_custom_base_name(minimal_project: Path) -> None:
    """add_errors() uses the provided base_name."""
    from packright.use_errors import add_errors

    add_errors(project_dir=str(minimal_project), base_name="MyCustomError")

    errors_py = minimal_project / "src" / "test_pkg" / "errors.py"
    content = errors_py.read_text()
    assert "MyCustomError" in content


def test_add_errors_skips_if_exists(minimal_project: Path) -> None:
    """add_errors() warns and skips if errors.py already exists."""
    from packright.use_errors import add_errors

    errors_py = minimal_project / "src" / "test_pkg" / "errors.py"
    errors_py.write_text("# existing", encoding="utf-8")

    add_errors(project_dir=str(minimal_project))

    assert errors_py.read_text() == "# existing"
