"""Open project-related URLs in the default browser.

Provides shortcuts to open PyPI, GitHub, and documentation pages.
"""

from __future__ import annotations

import webbrowser

from packright._config import get_package_name, read_project_config
from packright._messages import info, warn


def browse_pypi(project_dir: str = ".") -> None:
    """Open the project's PyPI page in the default browser.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    name = get_package_name(project_dir)
    url = f"https://pypi.org/project/{name}/"
    info(f"Opening {url}")
    webbrowser.open(url)


def browse_github(project_dir: str = ".") -> None:
    """Open the project's GitHub repository in the default browser.

    Reads the Repository URL from ``[project.urls]`` in pyproject.toml.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    url = _get_project_url(project_dir, "Repository")
    if url is None:
        warn("No [project.urls] Repository found in pyproject.toml.")
        return
    info(f"Opening {url}")
    webbrowser.open(url)


def browse_docs(project_dir: str = ".") -> None:
    """Open the project's documentation in the default browser.

    Reads the Documentation URL from ``[project.urls]`` in pyproject.toml.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    url = _get_project_url(project_dir, "Documentation")
    if url is None:
        warn("No [project.urls] Documentation found in pyproject.toml.")
        return
    info(f"Opening {url}")
    webbrowser.open(url)


def _get_project_url(project_dir: str, key: str) -> str | None:
    """Look up a URL from [project.urls] in pyproject.toml.

    Args:
        project_dir: Root directory of the project.
        key: The URL key to look up (e.g., "Repository", "Documentation").

    Returns:
        The URL string if found, or None.
    """
    config = read_project_config(project_dir)
    urls = config.get("project", {}).get("urls", {})
    return urls.get(key)
