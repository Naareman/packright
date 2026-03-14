"""Tests for packright.scaffold."""

from pathlib import Path

import pytest

from packright.errors import FileExistsError
from packright.scaffold import _normalize_name, create_package


def test_normalize_name_replaces_hyphens():
    assert _normalize_name("my-analytics-lib") == "my_analytics_lib"


def test_normalize_name_replaces_spaces():
    assert _normalize_name("my package") == "my_package"


def test_normalize_name_lowercases():
    assert _normalize_name("MyPackage") == "mypackage"


def test_create_package_creates_directory(tmp_project: Path):
    result = create_package("test-pkg", parent=str(tmp_project))

    assert result.exists()
    assert result.name == "test-pkg"


def test_create_package_creates_src_layout(tmp_project: Path):
    result = create_package("test-pkg", parent=str(tmp_project))

    assert (result / "src" / "test_pkg" / "__init__.py").exists()
    assert (result / "src" / "test_pkg" / "py.typed").exists()
    assert (result / "src" / "test_pkg" / "errors.py").exists()
    assert (result / "src" / "test_pkg" / "_messages.py").exists()
    assert (result / "src" / "test_pkg" / "core.py").exists()


def test_create_package_creates_tests(tmp_project: Path):
    result = create_package("test-pkg", parent=str(tmp_project))

    assert (result / "tests" / "conftest.py").exists()
    assert (result / "tests" / "test_core.py").exists()
    assert not (result / "tests" / "__init__.py").exists()


def test_create_package_creates_config_files(tmp_project: Path):
    result = create_package("test-pkg", parent=str(tmp_project))

    assert (result / "pyproject.toml").exists()
    assert (result / "README.md").exists()
    assert (result / "CHANGELOG.md").exists()
    assert (result / "LICENSE").exists()
    assert (result / ".gitignore").exists()
    assert (result / ".python-version").exists()
    assert (result / "mkdocs.yml").exists()


def test_create_package_creates_docs(tmp_project: Path):
    result = create_package("test-pkg", parent=str(tmp_project))

    assert (result / "docs" / "index.md").exists()
    assert (result / "docs" / "api.md").exists()


def test_create_package_pyproject_has_correct_name(tmp_project: Path):
    result = create_package("test-pkg", parent=str(tmp_project))

    content = (result / "pyproject.toml").read_text()
    assert 'name = "test-pkg"' in content
    assert 'packages = ["src/test_pkg"]' in content
    assert "--cov=test_pkg" in content


def test_create_package_raises_on_existing_directory(tmp_project: Path):
    (tmp_project / "test-pkg").mkdir()

    with pytest.raises(FileExistsError) as exc_info:
        create_package("test-pkg", parent=str(tmp_project))

    assert exc_info.value.path is not None
    assert "already exists" in str(exc_info.value)
