"""Add structured error classes to an existing package.

Creates an errors.py module with a base exception class named after the
package (e.g., MyPkgError for my-pkg).
"""

from __future__ import annotations

from pathlib import Path

from packright._messages import info, success, warn
from packright._templates import render_template
from packright.errors import ConfigError


def add_errors(project_dir: str = ".", base_name: str | None = None) -> Path:
    """Create an errors.py module in the target package.

    Args:
        project_dir: Root of the project (must contain src/<pkg>/).
        base_name: Custom base exception name (e.g., "MyAppError"). If not
            given, derived from the package name.

    Returns:
        Path to the created errors.py file.

    Raises:
        ConfigError: If no package directory is found under src/.
    """
    pkg_dir = _detect_package_dir(project_dir)
    target = pkg_dir / "errors.py"

    if target.exists():
        warn(f"[bold]{target}[/bold] already exists — skipping.")
        return target

    pkg_name = pkg_dir.name
    project_name = pkg_name.replace("_", "-")

    if base_name is None:
        base_name = _derive_error_name(pkg_name)

    context = {"name": project_name, "pkg_name": pkg_name}
    content = render_template("errors.py.j2", context)
    target.write_text(content, encoding="utf-8")
    success(f"Created [bold]{target}[/bold]")
    info(f"Base exception: [bold]{base_name}[/bold]")
    return target


def _derive_error_name(pkg_name: str) -> str:
    """Derive a PascalCase error class name from a package name.

    Args:
        pkg_name: Normalized package name (e.g., "my_pkg").

    Returns:
        Error class name (e.g., "MyPkgError").
    """
    parts = pkg_name.replace("-", "_").split("_")
    return "".join(part.capitalize() for part in parts) + "Error"


def _detect_package_dir(project_dir: str) -> Path:
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
