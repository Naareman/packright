"""Tests for packright.use_coverage."""

from __future__ import annotations

from pathlib import Path

from packright.use_coverage import add_coverage


def test_add_coverage_creates_config(minimal_project: Path) -> None:
    """Verify that add_coverage appends coverage config to pyproject.toml."""
    add_coverage(str(minimal_project))

    toml_path = minimal_project / "pyproject.toml"
    content = toml_path.read_text(encoding="utf-8")
    assert "[tool.coverage.run]" in content, (
        "pyproject.toml should contain [tool.coverage.run]"
    )
    assert "[tool.coverage.report]" in content, (
        "pyproject.toml should contain [tool.coverage.report]"
    )
    assert '"test_pkg"' in content, (
        "coverage source should use the normalized package name"
    )


def test_add_coverage_sets_fail_under(minimal_project: Path) -> None:
    """Verify that coverage report includes a fail_under threshold."""
    add_coverage(str(minimal_project))

    toml_path = minimal_project / "pyproject.toml"
    content = toml_path.read_text(encoding="utf-8")
    assert "fail_under" in content, "coverage config should set fail_under"


def test_add_coverage_skips_if_exists(minimal_project: Path) -> None:
    """Verify that calling add_coverage twice does not duplicate the config."""
    add_coverage(str(minimal_project))

    toml_path = minimal_project / "pyproject.toml"
    original_content = toml_path.read_text(encoding="utf-8")

    # Call again — should skip gracefully
    add_coverage(str(minimal_project))

    assert toml_path.read_text(encoding="utf-8") == original_content, (
        "add_coverage should not duplicate [tool.coverage] in pyproject.toml"
    )
