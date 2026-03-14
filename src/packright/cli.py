"""Command-line interface for packright.

Usage:
    packright scaffold my-app
    packright use-pytest
    packright use-mkdocs
    packright use-pre-commit
    packright use-github-actions
    packright use-rich
    packright use-errors
    packright use-license
    packright check
"""

from __future__ import annotations

import sys

import click

from packright import __version__
from packright._messages import abort, info, success
from packright.errors import PackrightError
from packright.scaffold import create_package
from packright.use_github_actions import add_github_actions
from packright.use_mkdocs import add_mkdocs
from packright.use_pre_commit import add_pre_commit
from packright.use_pytest import add_pytest


@click.group()
@click.version_option(version=__version__, prog_name="packright")
def main() -> None:
    """Automate Python package development the right way."""


@main.command()
@click.argument("name")
@click.option(
    "--path",
    default=".",
    help="Parent directory to create the package in. Defaults to current directory.",
)
def scaffold(name: str, path: str) -> None:
    """Create a new Python package with all conventions in place."""
    info(f"Creating package [bold]{name}[/bold]...")
    try:
        result_path = create_package(name, parent=path)
        success(f"Package created at [bold]{result_path}[/bold]")
        info("Next steps:")
        info(f"  cd {result_path}")
        info("  uv sync")
        info("  uv run pytest")
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-pytest")
@click.option("--path", default=".", help="Project directory. Defaults to current directory.")
def use_pytest(path: str) -> None:
    """Add pytest configuration and test scaffolding."""
    try:
        add_pytest(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-mkdocs")
@click.option("--path", default=".", help="Project directory. Defaults to current directory.")
def use_mkdocs(path: str) -> None:
    """Add MkDocs documentation scaffolding."""
    try:
        add_mkdocs(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-pre-commit")
@click.option("--path", default=".", help="Project directory. Defaults to current directory.")
def use_pre_commit(path: str) -> None:
    """Add pre-commit configuration with ruff, mypy, and standard hooks."""
    try:
        add_pre_commit(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-github-actions")
@click.option("--path", default=".", help="Project directory. Defaults to current directory.")
def use_github_actions_cmd(path: str) -> None:
    """Add GitHub Actions workflows for CI, release, and docs."""
    try:
        add_github_actions(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-rich")
@click.option("--path", default=".", help="Project directory. Defaults to current directory.")
def use_rich(path: str) -> None:
    """Add a rich-based _messages.py module for user output."""
    from packright.use_rich import add_rich

    try:
        add_rich(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-errors")
@click.option("--path", default=".", help="Project directory. Defaults to current directory.")
@click.option(
    "--base-name",
    default=None,
    help="Custom base exception name (e.g., MyAppError). Auto-derived if omitted.",
)
def use_errors(path: str, base_name: str | None) -> None:
    """Add structured error classes (errors.py) to the package."""
    from packright.use_errors import add_errors

    try:
        add_errors(project_dir=path, base_name=base_name)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-license")
@click.option("--path", default=".", help="Project directory. Defaults to current directory.")
@click.option(
    "--type",
    "license_type",
    default="MIT",
    help="License type. Only MIT is supported currently.",
)
@click.option(
    "--author",
    default="Your Name",
    help="Copyright holder name.",
)
def use_license(path: str, license_type: str, author: str) -> None:
    """Add a LICENSE file to the project root."""
    from packright.use_license import add_license

    try:
        add_license(project_dir=path, license_type=license_type, author=author)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command()
@click.option("--path", default=".", help="Project directory. Defaults to current directory.")
def check(path: str) -> None:
    """Audit the project structure against best practices (22 checks)."""
    from packright.check import audit_project

    try:
        passed, total = audit_project(project_dir=path)
        if passed < total:
            sys.exit(1)
    except PackrightError as e:
        abort(str(e))
        sys.exit(1)
