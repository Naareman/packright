"""Tests for packright.use_changelog."""

from __future__ import annotations

from pathlib import Path

from packright.use_changelog import add_changelog


def test_add_changelog_creates_file(minimal_project: Path) -> None:
    """Verify that add_changelog creates CHANGELOG.md."""
    add_changelog(str(minimal_project))

    changelog = minimal_project / "CHANGELOG.md"
    assert changelog.exists(), "CHANGELOG.md should be created"

    content = changelog.read_text(encoding="utf-8")
    assert "Keep a Changelog" in content
    assert "[Unreleased]" in content
    assert "Initial release" in content


def test_add_changelog_skips_if_exists(minimal_project: Path) -> None:
    """Verify that add_changelog does not overwrite an existing file."""
    changelog = minimal_project / "CHANGELOG.md"
    changelog.write_text("# Existing changelog\n", encoding="utf-8")

    add_changelog(str(minimal_project))

    content = changelog.read_text(encoding="utf-8")
    assert content == "# Existing changelog\n", (
        "add_changelog should not overwrite an existing CHANGELOG.md"
    )
