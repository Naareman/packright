"""Tests for packright.browse."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from packright.browse import browse_docs, browse_github, browse_pypi


def test_browse_pypi_opens_correct_url(minimal_project: Path) -> None:
    """Verify that browse_pypi opens the correct PyPI URL."""
    with patch("packright.browse.webbrowser.open") as mock_open:
        browse_pypi(str(minimal_project))
        mock_open.assert_called_once_with("https://pypi.org/project/test-pkg/")


def test_browse_github_opens_repo_url(minimal_project: Path) -> None:
    """Verify that browse_github opens the Repository URL from pyproject.toml."""
    pyproject = minimal_project / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")
    content += '\n[project.urls]\nRepository = "https://github.com/user/test-pkg"\n'
    pyproject.write_text(content, encoding="utf-8")

    with patch("packright.browse.webbrowser.open") as mock_open:
        browse_github(str(minimal_project))
        mock_open.assert_called_once_with("https://github.com/user/test-pkg")


def test_browse_github_warns_if_no_url(minimal_project: Path) -> None:
    """Verify that browse_github warns when no Repository URL is found."""
    with patch("packright.browse.webbrowser.open") as mock_open:
        browse_github(str(minimal_project))
        mock_open.assert_not_called()


def test_browse_docs_opens_docs_url(minimal_project: Path) -> None:
    """Verify that browse_docs opens the Documentation URL from pyproject.toml."""
    pyproject = minimal_project / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")
    content += '\n[project.urls]\nDocumentation = "https://test-pkg.readthedocs.io"\n'
    pyproject.write_text(content, encoding="utf-8")

    with patch("packright.browse.webbrowser.open") as mock_open:
        browse_docs(str(minimal_project))
        mock_open.assert_called_once_with("https://test-pkg.readthedocs.io")


def test_browse_docs_warns_if_no_url(minimal_project: Path) -> None:
    """Verify that browse_docs warns when no Documentation URL is found."""
    with patch("packright.browse.webbrowser.open") as mock_open:
        browse_docs(str(minimal_project))
        mock_open.assert_not_called()
