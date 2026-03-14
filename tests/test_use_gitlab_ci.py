"""Tests for packright.use_gitlab_ci."""

from __future__ import annotations

from pathlib import Path

from packright.use_gitlab_ci import add_gitlab_ci


def test_add_gitlab_ci_creates_config(minimal_project: Path) -> None:
    """Verify that add_gitlab_ci creates .gitlab-ci.yml."""
    add_gitlab_ci(str(minimal_project))

    ci_file = minimal_project / ".gitlab-ci.yml"
    assert ci_file.exists(), ".gitlab-ci.yml should be created"

    content = ci_file.read_text(encoding="utf-8")
    assert "stages:" in content
    assert "lint" in content
    assert "test" in content
    assert "publish" in content
    assert "ruff check" in content
    assert "pytest" in content


def test_add_gitlab_ci_skips_if_exists(minimal_project: Path) -> None:
    """Verify that add_gitlab_ci does not overwrite an existing file."""
    ci_file = minimal_project / ".gitlab-ci.yml"
    ci_file.write_text("# custom\n", encoding="utf-8")

    add_gitlab_ci(str(minimal_project))

    content = ci_file.read_text(encoding="utf-8")
    assert content == "# custom\n", ".gitlab-ci.yml should not be overwritten"
