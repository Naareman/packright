"""Shared test fixtures for packright."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """A temporary directory for scaffolding test packages into."""
    return tmp_path


@pytest.fixture
def minimal_project(tmp_path: Path) -> Path:
    """Create a minimal valid packright-style project in tmp_path.

    Includes:
        - pyproject.toml with [project], [build-system], [dependency-groups]
        - src/test_pkg/__init__.py
        - src/test_pkg/py.typed
    """
    project_dir = tmp_path / "test-pkg"
    project_dir.mkdir()

    # pyproject.toml
    pyproject = project_dir / "pyproject.toml"
    pyproject.write_text(
        '[project]\n'
        'name = "test-pkg"\n'
        'version = "0.1.0"\n'
        'description = "A test package."\n'
        'requires-python = ">=3.10"\n'
        'dependencies = []\n'
        "\n"
        "[build-system]\n"
        'requires = ["hatchling"]\n'
        'build-backend = "hatchling.build"\n'
        "\n"
        "[dependency-groups]\n"
        'dev = ["pytest>=8.0", "ruff>=0.4"]\n'
        "\n"
        "[tool.hatch.build.targets.wheel]\n"
        'packages = ["src/test_pkg"]\n',
        encoding="utf-8",
    )

    # Source layout
    src_dir = project_dir / "src" / "test_pkg"
    src_dir.mkdir(parents=True)
    (src_dir / "__init__.py").write_text(
        '"""test-pkg: A test package."""\n',
        encoding="utf-8",
    )
    (src_dir / "py.typed").write_text("", encoding="utf-8")

    return project_dir
