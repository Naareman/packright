"""Create a GitHub repository and link it to the project.

Equivalent to usethis::use_github() in R.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from packright._config import get_package_name
from packright._messages import info, success, warn


def add_github(project_dir: str = ".") -> None:
    """Create a public GitHub repo and push the local project to it.

    Checks that the ``gh`` CLI is installed, creates a public repo named
    after the [project] name in pyproject.toml, pushes the current source,
    and adds the repository URL to ``[project.urls]``.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    name = get_package_name(project_dir)

    # Check gh CLI is available
    if not _gh_is_installed():
        warn("GitHub CLI (gh) is not installed — install from https://cli.github.com/")
        return

    # Create the repo
    info(f"Creating GitHub repository '{name}' ...")
    try:
        result = subprocess.run(
            ["gh", "repo", "create", name, "--public", "--source", ".", "--push"],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        warn("GitHub CLI (gh) is not installed — install from https://cli.github.com/")
        return

    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "already exists" in stderr.lower():
            warn(f"Repository '{name}' already exists on GitHub — skipping creation.")
            return
        warn(f"gh repo create failed: {stderr}")
        return

    # Parse the repo URL from gh output
    repo_url = result.stdout.strip()
    if not repo_url:
        repo_url = f"https://github.com/{name}"

    success(f"Created GitHub repository: {repo_url}")

    # Update pyproject.toml with the repo URL
    _update_project_urls(root, repo_url)


def _gh_is_installed() -> bool:
    """Check whether the GitHub CLI is available on PATH.

    Returns:
        True if ``gh --version`` succeeds, False otherwise.
    """
    try:
        subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return False
    return True


def _update_project_urls(root: Path, repo_url: str) -> None:
    """Append a [project.urls] section to pyproject.toml if missing.

    Args:
        root: Project root directory.
        repo_url: The GitHub repository URL to add.
    """
    toml_path = root / "pyproject.toml"
    if not toml_path.exists():
        return

    content = toml_path.read_text(encoding="utf-8")

    if "[project.urls]" in content:
        info("[project.urls] already present in pyproject.toml — skipping URL update.")
        return

    urls_block = (
        "\n[project.urls]\n"
        f'Homepage = "{repo_url}"\n'
        f'Repository = "{repo_url}"\n'
        f'Issues = "{repo_url}/issues"\n'
    )
    content += urls_block
    toml_path.write_text(content, encoding="utf-8")
    success("Added [project.urls] to pyproject.toml")
