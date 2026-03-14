"""Tests for packright.use_ruff."""

from __future__ import annotations

from pathlib import Path

from packright.use_ruff import add_ruff


def test_add_ruff_creates_config(minimal_project: Path) -> None:
    """Verify that add_ruff appends [tool.ruff] to pyproject.toml."""
    add_ruff(str(minimal_project))

    toml_path = minimal_project / "pyproject.toml"
    content = toml_path.read_text(encoding="utf-8")
    assert "[tool.ruff]" in content, "pyproject.toml should contain [tool.ruff]"
    assert "line-length = 88" in content, "ruff config should set line-length"
    assert "[tool.ruff.lint]" in content, (
        "pyproject.toml should contain [tool.ruff.lint]"
    )


def test_add_ruff_no_target_version(minimal_project: Path) -> None:
    """Verify that ruff config does not include target-version."""
    add_ruff(str(minimal_project))

    toml_path = minimal_project / "pyproject.toml"
    content = toml_path.read_text(encoding="utf-8")
    assert "target-version" not in content, (
        "ruff config should not include target-version (reads from requires-python)"
    )


def test_add_ruff_skips_if_exists(minimal_project: Path) -> None:
    """Verify that calling add_ruff twice does not duplicate the config."""
    add_ruff(str(minimal_project))

    toml_path = minimal_project / "pyproject.toml"
    original_content = toml_path.read_text(encoding="utf-8")

    # Call again — should skip gracefully
    add_ruff(str(minimal_project))

    assert toml_path.read_text(encoding="utf-8") == original_content, (
        "add_ruff should not duplicate [tool.ruff] in pyproject.toml"
    )
