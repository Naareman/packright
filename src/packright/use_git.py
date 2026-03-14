"""Initialize a git repository for an existing project.

Creates .gitignore from a template, runs git init, and makes an initial commit.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from packright._messages import info, success, warn
from packright._templates import render_template
from packright.errors import PackrightError


def add_git(project_dir: str = ".") -> None:
    """Initialize a git repository with .gitignore and an initial commit.

    Creates a .gitignore from the gitignore template (if one does not exist),
    runs ``git init``, stages all files, and creates an initial commit.

    Args:
        project_dir: Root directory of the project. Defaults to ".".

    Raises:
        PackrightError: If a git command fails unexpectedly.
    """
    root = Path(project_dir).resolve()

    if (root / ".git").exists():
        warn(".git already exists — skipping.")
        return

    # Create .gitignore from template if missing
    gitignore_path = root / ".gitignore"
    if not gitignore_path.exists():
        content = render_template("gitignore.j2", {})
        gitignore_path.write_text(content, encoding="utf-8")
        success("Created .gitignore")
    else:
        info(".gitignore already exists — keeping it.")

    # Run git commands
    _run_git(["git", "init"], cwd=root)
    success("Initialized git repository")

    _run_git(["git", "add", "."], cwd=root)
    _run_git(
        ["git", "commit", "-m", "chore: initial commit"],
        cwd=root,
    )
    success("Created initial commit")


def _run_git(cmd: list[str], cwd: Path) -> None:
    """Run a git command and raise on failure.

    Args:
        cmd: The git command as a list of arguments.
        cwd: Working directory for the command.

    Raises:
        PackrightError: If the command exits with a non-zero status.
    """
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise PackrightError(
            f"git command failed: {' '.join(cmd)}\n{result.stderr.strip()}"
        )
