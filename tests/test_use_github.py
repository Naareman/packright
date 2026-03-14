"""Tests for packright.use_github."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from packright.use_github import add_github


def test_add_github_warns_when_gh_not_installed(minimal_project: Path) -> None:
    """Warn gracefully when the gh CLI is not found."""
    with patch(
        "packright.use_github._gh_is_installed", return_value=False
    ):
        # Should not raise
        add_github(str(minimal_project))


def test_add_github_handles_existing_repo(minimal_project: Path) -> None:
    """Handle the case where the repo already exists on GitHub."""
    with (
        patch("packright.use_github._gh_is_installed", return_value=True),
        patch("packright.use_github.subprocess.run") as mock_run,
    ):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "already exists on GitHub"
        mock_run.return_value.stdout = ""

        add_github(str(minimal_project))

        # pyproject.toml should NOT have [project.urls] added
        content = (minimal_project / "pyproject.toml").read_text(encoding="utf-8")
        assert "[project.urls]" not in content


def test_add_github_creates_repo_and_updates_urls(minimal_project: Path) -> None:
    """On success, add [project.urls] to pyproject.toml."""
    with (
        patch("packright.use_github._gh_is_installed", return_value=True),
        patch("packright.use_github.subprocess.run") as mock_run,
    ):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "https://github.com/user/test-pkg"
        mock_run.return_value.stderr = ""

        add_github(str(minimal_project))

        content = (minimal_project / "pyproject.toml").read_text(encoding="utf-8")
        assert "[project.urls]" in content
        assert "https://github.com/user/test-pkg" in content
