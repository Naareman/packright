"""Tests for packright.use_pre_commit."""

from __future__ import annotations

from pathlib import Path

from packright.use_pre_commit import add_pre_commit


def test_add_pre_commit_creates_config(minimal_project: Path) -> None:
    """Verify that add_pre_commit creates .pre-commit-config.yaml."""
    add_pre_commit(str(minimal_project))

    config = minimal_project / ".pre-commit-config.yaml"
    assert config.exists(), ".pre-commit-config.yaml should be created"

    content = config.read_text(encoding="utf-8")
    assert "repos:" in content or "repos" in content, (
        ".pre-commit-config.yaml should define repos"
    )


def test_add_pre_commit_config_has_ruff(minimal_project: Path) -> None:
    """Verify that the pre-commit config includes a ruff hook."""
    add_pre_commit(str(minimal_project))

    config = minimal_project / ".pre-commit-config.yaml"
    content = config.read_text(encoding="utf-8")
    assert "ruff" in content.lower(), (
        ".pre-commit-config.yaml should include a ruff hook"
    )


def test_add_pre_commit_skips_if_exists(minimal_project: Path) -> None:
    """Verify that calling add_pre_commit twice does not overwrite."""
    add_pre_commit(str(minimal_project))

    config = minimal_project / ".pre-commit-config.yaml"
    original_content = config.read_text(encoding="utf-8")

    # Call again — should skip gracefully
    add_pre_commit(str(minimal_project))

    assert config.read_text(encoding="utf-8") == original_content, (
        "add_pre_commit should not overwrite existing .pre-commit-config.yaml"
    )
