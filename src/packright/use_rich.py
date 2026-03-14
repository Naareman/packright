"""Add rich-based messaging to an existing package.

Creates a _messages.py module with info/success/warn/abort functions
using the rich library for beautiful terminal output.
"""

from __future__ import annotations

from pathlib import Path

from packright._config import detect_package_dir
from packright._messages import info, success, warn
from packright._templates import render_template


def add_rich(project_dir: str = ".") -> Path:
    """Create a _messages.py module in the target package.

    Args:
        project_dir: Root of the project (must contain src/<pkg>/).

    Returns:
        Path to the created _messages.py file.

    Raises:
        ConfigError: If no package directory is found under src/.
    """
    pkg_dir = detect_package_dir(project_dir)
    target = pkg_dir / "_messages.py"

    if target.exists():
        warn(f"[bold]{target}[/bold] already exists — skipping.")
        return target

    content = render_template("_messages.py.j2", {})
    target.write_text(content, encoding="utf-8")
    success(f"Created [bold]{target}[/bold]")
    info("Import with: from <pkg>._messages import info, success, warn, abort")
    return target
