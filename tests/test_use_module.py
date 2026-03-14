"""Tests for packright.use_module."""

from __future__ import annotations

from pathlib import Path

from packright.use_module import add_module, add_module_with_test, add_test


def test_add_module_creates_file(minimal_project: Path) -> None:
    """Verify that add_module creates src/<pkg>/name.py."""
    add_module(str(minimal_project), name="utils")

    module = minimal_project / "src" / "test_pkg" / "utils.py"
    assert module.exists(), "Module file should be created"

    content = module.read_text(encoding="utf-8")
    assert "from __future__ import annotations" in content
    assert "utils" in content


def test_add_module_warns_if_exists(minimal_project: Path) -> None:
    """Verify that add_module does not overwrite an existing module."""
    module = minimal_project / "src" / "test_pkg" / "utils.py"
    module.write_text("# existing\n", encoding="utf-8")

    add_module(str(minimal_project), name="utils")

    content = module.read_text(encoding="utf-8")
    assert content == "# existing\n", (
        "add_module should not overwrite an existing file"
    )


def test_add_test_creates_file(minimal_project: Path) -> None:
    """Verify that add_test creates tests/test_<name>.py."""
    add_test(str(minimal_project), name="utils")

    test_file = minimal_project / "tests" / "test_utils.py"
    assert test_file.exists(), "Test file should be created"

    content = test_file.read_text(encoding="utf-8")
    assert "from __future__ import annotations" in content
    assert "test_pkg" in content
    assert "def test_placeholder" in content


def test_add_test_warns_if_exists(minimal_project: Path) -> None:
    """Verify that add_test does not overwrite an existing test."""
    tests_dir = minimal_project / "tests"
    tests_dir.mkdir(exist_ok=True)
    test_file = tests_dir / "test_utils.py"
    test_file.write_text("# existing test\n", encoding="utf-8")

    add_test(str(minimal_project), name="utils")

    content = test_file.read_text(encoding="utf-8")
    assert content == "# existing test\n", (
        "add_test should not overwrite an existing file"
    )


def test_add_module_with_test_creates_both(minimal_project: Path) -> None:
    """Verify that add_module_with_test creates both files."""
    add_module_with_test(str(minimal_project), name="helpers")

    module = minimal_project / "src" / "test_pkg" / "helpers.py"
    test_file = minimal_project / "tests" / "test_helpers.py"

    assert module.exists(), "Module file should be created"
    assert test_file.exists(), "Test file should be created"
