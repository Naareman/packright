"""Bump the project version in pyproject.toml.

Supports major, minor, and patch increments following semver.
"""

from __future__ import annotations

import re
from pathlib import Path

from packright._config import read_project_config
from packright._messages import info, success
from packright.errors import ConfigError, PackrightError


def bump_version(project_dir: str = ".", part: str = "patch") -> None:
    """Bump the version string in pyproject.toml.

    Reads the current version, increments the requested part
    (major, minor, or patch), and writes it back.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
        part: Which version part to bump. One of "major", "minor", "patch".

    Raises:
        PackrightError: If *part* is not major/minor/patch.
        ConfigError: If no version is found in pyproject.toml.
    """
    valid_parts = ("major", "minor", "patch")
    if part not in valid_parts:
        raise PackrightError(
            f"Invalid version part '{part}'. Must be one of: {', '.join(valid_parts)}"
        )

    root = Path(project_dir).resolve()
    toml_path = root / "pyproject.toml"

    config = read_project_config(project_dir)
    old_version = config.get("project", {}).get("version")

    if not old_version:
        raise ConfigError(
            "No version found in pyproject.toml [project] section.",
            field="project.version",
        )

    parts = old_version.split(".")
    if len(parts) != 3:
        raise ConfigError(
            f"Version '{old_version}' is not a valid semver (expected X.Y.Z).",
            field="project.version",
        )

    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"

    raw = toml_path.read_text(encoding="utf-8")
    updated = re.sub(
        r'(version\s*=\s*")[^"]+(")',
        rf"\g<1>{new_version}\2",
        raw,
        count=1,
    )
    toml_path.write_text(updated, encoding="utf-8")

    info(f"Version: {old_version} -> {new_version}")
    success(f"Bumped {part} version to {new_version}")
