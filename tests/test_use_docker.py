"""Tests for packright.use_docker."""

from __future__ import annotations

from pathlib import Path

from packright.use_docker import add_docker


def test_add_docker_creates_dockerfile(minimal_project: Path) -> None:
    """Verify that add_docker creates a Dockerfile."""
    add_docker(str(minimal_project))

    dockerfile = minimal_project / "Dockerfile"
    assert dockerfile.exists(), "Dockerfile should be created"

    content = dockerfile.read_text(encoding="utf-8")
    assert "FROM python:3.12-slim" in content
    assert "uv sync --no-dev" in content
    assert "COPY src/ src/" in content
    assert 'CMD ["python", "-m", "test_pkg"]' in content


def test_add_docker_creates_dockerignore(minimal_project: Path) -> None:
    """Verify that add_docker creates a .dockerignore."""
    add_docker(str(minimal_project))

    dockerignore = minimal_project / ".dockerignore"
    assert dockerignore.exists(), ".dockerignore should be created"

    content = dockerignore.read_text(encoding="utf-8")
    assert ".venv/" in content
    assert "__pycache__/" in content
    assert ".git/" in content


def test_add_docker_skips_if_dockerfile_exists(minimal_project: Path) -> None:
    """Verify that add_docker does not overwrite an existing Dockerfile."""
    dockerfile = minimal_project / "Dockerfile"
    dockerfile.write_text("# custom\n", encoding="utf-8")

    add_docker(str(minimal_project))

    content = dockerfile.read_text(encoding="utf-8")
    assert content == "# custom\n", "Dockerfile should not be overwritten"


def test_add_docker_skips_if_dockerignore_exists(minimal_project: Path) -> None:
    """Verify that add_docker does not overwrite an existing .dockerignore."""
    dockerignore = minimal_project / ".dockerignore"
    dockerignore.write_text("# custom\n", encoding="utf-8")

    add_docker(str(minimal_project))

    content = dockerignore.read_text(encoding="utf-8")
    assert content == "# custom\n", ".dockerignore should not be overwritten"


def test_add_docker_includes_uv_lock_if_exists(minimal_project: Path) -> None:
    """Verify that Dockerfile copies uv.lock when it exists."""
    (minimal_project / "uv.lock").write_text("", encoding="utf-8")

    add_docker(str(minimal_project))

    content = (minimal_project / "Dockerfile").read_text(encoding="utf-8")
    assert "uv.lock" in content, "Dockerfile should copy uv.lock when present"
