"""Tests for packright.check."""

from __future__ import annotations

from pathlib import Path


def test_audit_project_on_minimal_project(minimal_project: Path) -> None:
    """audit_project() runs without errors on a minimal project."""
    from packright.check import audit_project

    passed, total = audit_project(project_dir=str(minimal_project))

    assert total > 0
    assert passed <= total
    assert passed > 0


def test_audit_project_on_full_scaffold(tmp_path: Path) -> None:
    """audit_project() gives 22/22 on a fully scaffolded package."""
    from packright.check import audit_project
    from packright.scaffold import create_package

    pkg = create_package("full-test", parent=str(tmp_path))
    passed, total = audit_project(project_dir=str(pkg))

    assert passed == total
    assert total == 22
