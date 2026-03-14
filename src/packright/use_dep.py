"""Add project dependencies via uv.

Wraps ``uv add`` for both runtime and development dependencies.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from packright._messages import info, success, warn


def add_dep(
    project_dir: str = ".",
    name: str = "",
    version: str | None = None,
) -> None:
    """Add a runtime dependency using ``uv add``.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
        name: Package name to add (e.g. ``"requests"``).
        version: Optional minimum version constraint (e.g. ``"2.31"``).
    """
    if not name:
        warn("No dependency name provided.")
        return

    spec = f"{name}>={version}" if version else name
    info(f"Adding dependency: {spec}")

    _run_uv_add(project_dir, [spec])


def add_dev_dep(
    project_dir: str = ".",
    name: str = "",
    version: str | None = None,
) -> None:
    """Add a development dependency using ``uv add --group dev``.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
        name: Package name to add (e.g. ``"pytest"``).
        version: Optional minimum version constraint (e.g. ``"8.0"``).
    """
    if not name:
        warn("No dependency name provided.")
        return

    spec = f"{name}>={version}" if version else name
    info(f"Adding dev dependency: {spec}")

    _run_uv_add(project_dir, ["--group", "dev", spec])


def _run_uv_add(project_dir: str, args: list[str]) -> None:
    """Run ``uv add`` with the given arguments.

    Args:
        project_dir: Root directory of the project.
        args: Additional arguments for ``uv add``.
    """
    root = Path(project_dir).resolve()

    try:
        result = subprocess.run(
            ["uv", "add", *args],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        warn("uv is not installed — install from https://docs.astral.sh/uv/")
        return

    if result.returncode != 0:
        stderr = result.stderr.strip()
        warn(f"uv add failed: {stderr}")
        return

    success(f"uv add {' '.join(args)} — done")
