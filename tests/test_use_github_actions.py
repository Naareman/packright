"""Tests for packright.use_github_actions."""

from __future__ import annotations

from pathlib import Path

from packright.use_github_actions import add_github_actions


def test_add_github_actions_creates_ci_yml(minimal_project: Path) -> None:
    """Verify that add_github_actions creates a CI workflow file."""
    add_github_actions(str(minimal_project))

    ci_yml = minimal_project / ".github" / "workflows" / "ci.yml"
    assert ci_yml.exists(), ".github/workflows/ci.yml should be created"

    content = ci_yml.read_text(encoding="utf-8")
    assert "pytest" in content or "test" in content.lower(), (
        "CI workflow should include test steps"
    )


def test_add_github_actions_creates_release_yml(minimal_project: Path) -> None:
    """Verify that add_github_actions creates a release workflow file."""
    add_github_actions(str(minimal_project))

    release_yml = minimal_project / ".github" / "workflows" / "release.yml"
    assert release_yml.exists(), ".github/workflows/release.yml should be created"

    content = release_yml.read_text(encoding="utf-8")
    assert "pypi" in content.lower() or "publish" in content.lower(), (
        "Release workflow should reference PyPI or publishing"
    )


def test_add_github_actions_creates_docs_yml(minimal_project: Path) -> None:
    """Verify that add_github_actions creates a docs workflow file."""
    add_github_actions(str(minimal_project))

    docs_yml = minimal_project / ".github" / "workflows" / "docs.yml"
    assert docs_yml.exists(), ".github/workflows/docs.yml should be created"

    content = docs_yml.read_text(encoding="utf-8")
    assert "mkdocs" in content.lower() or "docs" in content.lower(), (
        "Docs workflow should reference mkdocs or documentation"
    )
