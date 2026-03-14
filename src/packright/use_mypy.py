"""Add mypy configuration to an existing project.

Appends [tool.mypy] to pyproject.toml and creates a py.typed marker.
"""

from __future__ import annotations

from pathlib import Path

from packright._config import get_pkg_name
from packright._messages import info, success, warn

_MYPY_CONFIG = """
[tool.mypy]
python_version = "3.10"
strict = true
"""


def add_mypy(project_dir: str = ".") -> None:
    """Add mypy configuration to pyproject.toml and create py.typed marker.

    Appends a ``[tool.mypy]`` section with strict mode enabled and creates
    a ``py.typed`` marker file in the package source directory.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    pyproject_path = root / "pyproject.toml"

    # Check if [tool.mypy] already exists
    content = pyproject_path.read_text(encoding="utf-8")
    if "[tool.mypy]" in content:
        warn("[tool.mypy] already exists in pyproject.toml — skipping.")
        return

    # Append mypy config
    with pyproject_path.open("a", encoding="utf-8") as f:
        f.write(_MYPY_CONFIG)
    success("Added [tool.mypy] to pyproject.toml")

    # Create py.typed marker
    pkg_name = get_pkg_name(project_dir)
    py_typed_path = root / "src" / pkg_name / "py.typed"
    if py_typed_path.exists():
        info("py.typed already exists — keeping it.")
    else:
        py_typed_path.parent.mkdir(parents=True, exist_ok=True)
        py_typed_path.write_text("", encoding="utf-8")
        success(f"Created src/{pkg_name}/py.typed")

    success("mypy setup complete")
