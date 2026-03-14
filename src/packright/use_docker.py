"""Add Docker configuration to an existing project.

Creates a multi-stage Dockerfile and .dockerignore.
"""

from __future__ import annotations

from pathlib import Path

from packright._config import get_package_name, get_pkg_name
from packright._messages import success, warn

_DOCKERIGNORE = """\
.venv/
.git/
__pycache__/
dist/
.mypy_cache/
htmlcov/
.pytest_cache/
"""


def add_docker(project_dir: str = ".") -> None:
    """Add a Dockerfile and .dockerignore to the project root.

    Creates a multi-stage Dockerfile that uses uv to install dependencies
    in a builder stage and copies only what is needed into a slim runtime
    image.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    pkg_name = get_pkg_name(project_dir)
    package_name = get_package_name(project_dir)

    # Build the COPY line for uv.lock conditionally
    has_lock = (root / "uv.lock").exists()
    copy_files = "pyproject.toml uv.lock" if has_lock else "pyproject.toml"

    dockerfile_content = f"""\
# --- builder stage ---
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY {copy_files} ./
RUN uv sync --no-dev

COPY src/ src/

# --- runtime stage ---
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app /app

CMD ["python", "-m", "{pkg_name}"]
"""

    # Dockerfile
    dockerfile_path = root / "Dockerfile"
    if dockerfile_path.exists():
        warn("Dockerfile already exists — skipping.")
    else:
        dockerfile_path.write_text(dockerfile_content, encoding="utf-8")
        success("Created Dockerfile")

    # .dockerignore
    dockerignore_path = root / ".dockerignore"
    if dockerignore_path.exists():
        warn(".dockerignore already exists — skipping.")
    else:
        dockerignore_path.write_text(_DOCKERIGNORE, encoding="utf-8")
        success("Created .dockerignore")
