"""Tests for packright.use_mkdocs."""

from __future__ import annotations

from pathlib import Path

from packright.use_mkdocs import add_mkdocs


def test_add_mkdocs_creates_mkdocs_yml_at_root(minimal_project: Path) -> None:
    """Verify that add_mkdocs creates mkdocs.yml at the project root."""
    add_mkdocs(str(minimal_project))

    mkdocs_yml = minimal_project / "mkdocs.yml"
    assert mkdocs_yml.exists(), "mkdocs.yml should exist at project root"

    content = mkdocs_yml.read_text(encoding="utf-8")
    assert "site_name" in content or "site-name" in content.lower(), (
        "mkdocs.yml should contain a site_name key"
    )


def test_add_mkdocs_creates_docs_dir(minimal_project: Path) -> None:
    """Verify that add_mkdocs creates a docs/ directory with an index file."""
    add_mkdocs(str(minimal_project))

    docs_dir = minimal_project / "docs"
    assert docs_dir.is_dir(), "docs/ directory should be created"

    index_md = docs_dir / "index.md"
    assert index_md.exists(), "docs/index.md should be created"


def test_add_mkdocs_skips_if_exists(minimal_project: Path) -> None:
    """Verify that calling add_mkdocs twice does not overwrite existing files."""
    add_mkdocs(str(minimal_project))

    mkdocs_yml = minimal_project / "mkdocs.yml"
    original_content = mkdocs_yml.read_text(encoding="utf-8")

    # Call again — should skip gracefully
    add_mkdocs(str(minimal_project))

    assert mkdocs_yml.read_text(encoding="utf-8") == original_content, (
        "add_mkdocs should not overwrite existing mkdocs.yml"
    )
