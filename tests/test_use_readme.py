"""Tests for packright.use_readme."""

from __future__ import annotations

from pathlib import Path

from packright.use_readme import add_readme


def test_add_readme_creates_file(minimal_project: Path) -> None:
    """Verify that add_readme creates README.md with expected content."""
    add_readme(str(minimal_project))

    readme = minimal_project / "README.md"
    assert readme.exists(), "README.md should be created"

    content = readme.read_text(encoding="utf-8")
    assert "# test-pkg" in content, (
        "README should contain the package name as title"
    )
    assert "pip install test-pkg" in content, (
        "README should contain install instructions"
    )
    assert "import test_pkg" in content, (
        "README should contain quickstart import"
    )
    assert "PyPI" in content, "README should contain PyPI badge placeholder"


def test_add_readme_includes_description(minimal_project: Path) -> None:
    """Verify that the description from pyproject.toml appears in README."""
    add_readme(str(minimal_project))

    readme = minimal_project / "README.md"
    content = readme.read_text(encoding="utf-8")
    assert "A test package." in content, "README should contain project description"


def test_add_readme_skips_if_exists(minimal_project: Path) -> None:
    """Verify that calling add_readme twice does not overwrite."""
    add_readme(str(minimal_project))

    readme = minimal_project / "README.md"
    original_content = readme.read_text(encoding="utf-8")

    # Call again — should skip gracefully
    add_readme(str(minimal_project))

    assert readme.read_text(encoding="utf-8") == original_content, (
        "add_readme should not overwrite existing README.md"
    )
