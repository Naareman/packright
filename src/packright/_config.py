"""Shared configuration helpers for reading pyproject.toml.

Provides utilities to parse project metadata needed by use-* commands.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from packright._messages import abort
from packright.errors import ConfigError


def read_project_config(project_dir: str = ".") -> dict:
    """Read and parse pyproject.toml from the given directory.

    Uses tomllib (3.11+) with tomli fallback, then a regex fallback
    for minimal field extraction on Python 3.10.

    Args:
        project_dir: Directory containing pyproject.toml. Defaults to ".".

    Returns:
        Parsed dict of the TOML contents.

    Raises:
        ConfigError: If pyproject.toml is missing or cannot be parsed.
    """
    toml_path = Path(project_dir).resolve() / "pyproject.toml"

    if not toml_path.exists():
        abort(f"No pyproject.toml found in {toml_path.parent}")
        raise ConfigError(
            f"No pyproject.toml found in {toml_path.parent}",
            field="pyproject.toml",
        )

    raw = toml_path.read_text(encoding="utf-8")

    # Try tomllib (3.11+), then tomli, then regex fallback
    if sys.version_info >= (3, 11):
        import tomllib

        try:
            return tomllib.loads(raw)
        except tomllib.TOMLDecodeError as e:
            abort(f"Failed to parse pyproject.toml: {e}")
            raise ConfigError(str(e), field="pyproject.toml") from e

    try:
        import tomli

        try:
            return tomli.loads(raw)
        except tomli.TOMLDecodeError as e:
            abort(f"Failed to parse pyproject.toml: {e}")
            raise ConfigError(str(e), field="pyproject.toml") from e
    except ImportError:
        pass

    # Regex fallback for Python 3.10 without tomli
    return _regex_parse_toml(raw)


def _regex_parse_toml(raw: str) -> dict:
    """Minimal regex-based extraction of pyproject.toml fields.

    Only extracts [project] name — enough for use-* commands.

    Args:
        raw: Raw TOML file contents.

    Returns:
        A dict with at least {"project": {"name": ...}} if found.
    """
    result: dict = {}
    name_match = re.search(
        r'^\[project\]\s*\n(?:.*\n)*?name\s*=\s*"([^"]+)"',
        raw,
        re.MULTILINE,
    )
    if name_match:
        result["project"] = {"name": name_match.group(1)}
    return result


def get_package_name(project_dir: str = ".") -> str:
    """Return the [project] name from pyproject.toml.

    Args:
        project_dir: Directory containing pyproject.toml. Defaults to ".".

    Returns:
        The project name as declared in pyproject.toml.

    Raises:
        ConfigError: If pyproject.toml is missing or has no [project] name.
    """
    config = read_project_config(project_dir)
    try:
        return config["project"]["name"]
    except KeyError:
        abort("No [project] name found in pyproject.toml")
        raise ConfigError(
            "No [project] name found in pyproject.toml",
            field="project.name",
        )


def get_pkg_name(project_dir: str = ".") -> str:
    """Return the normalized importable name (hyphens replaced with underscores).

    Args:
        project_dir: Directory containing pyproject.toml. Defaults to ".".

    Returns:
        Normalized package name suitable for Python imports.

    Raises:
        ConfigError: If pyproject.toml is missing or has no [project] name.
    """
    return get_package_name(project_dir).replace("-", "_").replace(" ", "_").lower()


def detect_package_dir(project_dir: str = ".") -> Path:
    """Find the single package directory under src/.

    Args:
        project_dir: Root of the project.

    Returns:
        Path to the package directory (e.g., src/my_pkg/).

    Raises:
        ConfigError: If src/ is missing or contains no package directory.
    """
    src = Path(project_dir).resolve() / "src"
    if not src.is_dir():
        raise ConfigError("No src/ directory found.", field="src")

    candidates = [
        d for d in src.iterdir()
        if d.is_dir() and not d.name.startswith((".", "_"))
    ]

    if not candidates:
        raise ConfigError("No package directory found under src/.", field="src")
    if len(candidates) > 1:
        names = ", ".join(d.name for d in candidates)
        raise ConfigError(
            f"Multiple packages found under src/: {names}. Cannot auto-detect.",
            field="src",
        )

    return candidates[0]
