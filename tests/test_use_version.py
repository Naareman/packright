"""Tests for packright.use_version."""

from __future__ import annotations

from pathlib import Path

import pytest

from packright.errors import ConfigError, PackrightError
from packright.use_version import bump_version


def test_bump_patch(minimal_project: Path) -> None:
    """Verify that bump_version increments the patch number."""
    bump_version(str(minimal_project), part="patch")

    toml_path = minimal_project / "pyproject.toml"
    content = toml_path.read_text(encoding="utf-8")
    assert '"0.1.1"' in content, "patch bump should go from 0.1.0 to 0.1.1"


def test_bump_minor(minimal_project: Path) -> None:
    """Verify that bump_version increments the minor number and resets patch."""
    bump_version(str(minimal_project), part="minor")

    toml_path = minimal_project / "pyproject.toml"
    content = toml_path.read_text(encoding="utf-8")
    assert '"0.2.0"' in content, "minor bump should go from 0.1.0 to 0.2.0"


def test_bump_major(minimal_project: Path) -> None:
    """Verify that bump_version increments the major number and resets minor/patch."""
    bump_version(str(minimal_project), part="major")

    toml_path = minimal_project / "pyproject.toml"
    content = toml_path.read_text(encoding="utf-8")
    assert '"1.0.0"' in content, "major bump should go from 0.1.0 to 1.0.0"


def test_bump_invalid_part(minimal_project: Path) -> None:
    """Verify that an invalid part raises PackrightError."""
    with pytest.raises(PackrightError, match="Invalid version part"):
        bump_version(str(minimal_project), part="hotfix")


def test_bump_missing_version(minimal_project: Path) -> None:
    """Verify that a missing version raises ConfigError."""
    toml_path = minimal_project / "pyproject.toml"
    toml_path.write_text(
        '[project]\nname = "test-pkg"\n',
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="No version found"):
        bump_version(str(minimal_project), part="patch")
