"""Tests for packright.use_license."""

from __future__ import annotations

from pathlib import Path


def test_add_license_creates_license_file(minimal_project: Path) -> None:
    """add_license() creates a LICENSE file at project root."""
    from packright.use_license import add_license

    add_license(project_dir=str(minimal_project))

    license_file = minimal_project / "LICENSE"
    assert license_file.exists()
    content = license_file.read_text()
    assert "MIT License" in content


def test_add_license_skips_if_exists(minimal_project: Path) -> None:
    """add_license() warns and skips if LICENSE already exists."""
    from packright.use_license import add_license

    license_file = minimal_project / "LICENSE"
    license_file.write_text("# existing", encoding="utf-8")

    add_license(project_dir=str(minimal_project))

    assert license_file.read_text() == "# existing"
