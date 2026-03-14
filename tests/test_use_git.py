"""Tests for packright.use_git."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from packright.use_git import add_git


def test_add_git_initializes_repo(minimal_project: Path) -> None:
    """Verify that add_git creates a .git directory and .gitignore."""
    add_git(str(minimal_project))

    assert (minimal_project / ".git").exists(), ".git directory should be created"
    assert (minimal_project / ".gitignore").exists(), ".gitignore should be created"


def test_add_git_creates_initial_commit(minimal_project: Path) -> None:
    """Verify that add_git makes an initial commit."""
    import subprocess

    add_git(str(minimal_project))

    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=minimal_project,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "git log should succeed"
    assert "initial commit" in result.stdout, "should contain the initial commit message"


def test_add_git_skips_if_exists(minimal_project: Path) -> None:
    """Verify that calling add_git twice does not re-initialize."""
    add_git(str(minimal_project))

    import subprocess

    # Count commits before second call
    result_before = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=minimal_project,
        capture_output=True,
        text=True,
    )

    # Call again — should skip gracefully
    add_git(str(minimal_project))

    result_after = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=minimal_project,
        capture_output=True,
        text=True,
    )
    assert result_before.stdout == result_after.stdout, (
        "add_git should not create additional commits when .git already exists"
    )


def test_add_git_keeps_existing_gitignore(minimal_project: Path) -> None:
    """Verify that add_git does not overwrite an existing .gitignore."""
    gitignore = minimal_project / ".gitignore"
    gitignore.write_text("custom-ignore\n", encoding="utf-8")

    add_git(str(minimal_project))

    content = gitignore.read_text(encoding="utf-8")
    assert "custom-ignore" in content, (
        "add_git should not overwrite an existing .gitignore"
    )
