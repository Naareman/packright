"""Tests for packright.use_contributing."""

from __future__ import annotations

from pathlib import Path

from packright.use_contributing import add_contributing


def test_add_contributing_creates_all_files(minimal_project: Path) -> None:
    """Verify that add_contributing creates all four files."""
    add_contributing(str(minimal_project))

    assert (minimal_project / "CONTRIBUTING.md").exists()
    assert (minimal_project / "CODE_OF_CONDUCT.md").exists()
    assert (minimal_project / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").exists()
    assert (
        minimal_project / ".github" / "ISSUE_TEMPLATE" / "feature_request.md"
    ).exists()


def test_contributing_contains_uv_instructions(minimal_project: Path) -> None:
    """Verify that CONTRIBUTING.md mentions uv for development setup."""
    add_contributing(str(minimal_project))

    content = (minimal_project / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "uv sync" in content
    assert "uv run pytest" in content


def test_code_of_conduct_is_contributor_covenant(minimal_project: Path) -> None:
    """Verify that CODE_OF_CONDUCT.md uses the Contributor Covenant."""
    add_contributing(str(minimal_project))

    content = (minimal_project / "CODE_OF_CONDUCT.md").read_text(encoding="utf-8")
    assert "Contributor Covenant" in content


def test_add_contributing_skips_existing_files(minimal_project: Path) -> None:
    """Verify that existing files are not overwritten."""
    existing = minimal_project / "CONTRIBUTING.md"
    existing.write_text("# My custom contributing guide\n", encoding="utf-8")

    add_contributing(str(minimal_project))

    content = existing.read_text(encoding="utf-8")
    assert content == "# My custom contributing guide\n", (
        "add_contributing should not overwrite an existing CONTRIBUTING.md"
    )

    # Other files should still be created
    assert (minimal_project / "CODE_OF_CONDUCT.md").exists()


def test_issue_templates_have_frontmatter(minimal_project: Path) -> None:
    """Verify that issue templates contain YAML frontmatter."""
    add_contributing(str(minimal_project))

    bug = (
        minimal_project / ".github" / "ISSUE_TEMPLATE" / "bug_report.md"
    ).read_text(encoding="utf-8")
    assert bug.startswith("---")
    assert "name: Bug report" in bug

    feature = (
        minimal_project / ".github" / "ISSUE_TEMPLATE" / "feature_request.md"
    ).read_text(encoding="utf-8")
    assert feature.startswith("---")
    assert "name: Feature request" in feature
