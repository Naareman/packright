"""Command-line interface for packright.

Usage:
    packright scaffold my-app
    packright init
    packright doctor
    packright check
    packright bump-version
    packright use-pytest
    packright use-mkdocs
    packright use-pre-commit
    packright use-github-actions
    packright use-github
    packright use-rich
    packright use-errors
    packright use-license
    packright use-readme
    packright use-ruff
    packright use-coverage
    packright use-git
    packright use-docker
    packright use-mypy
    packright use-gitlab-ci
    packright use-changelog
    packright use-contributing
    packright use-module
    packright use-dep
    packright use-dev-dep
    packright browse-pypi
    packright browse-github
    packright browse-docs
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
@click.option(
    "--path", default=".", help="Project directory."
)
def use_pytest(path: str) -> None:
    """Add pytest configuration and test scaffolding."""
    try:
        add_pytest(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-mkdocs")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_mkdocs(path: str) -> None:
    """Add MkDocs documentation scaffolding."""
    try:
        add_mkdocs(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-pre-commit")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_pre_commit(path: str) -> None:
    """Add pre-commit configuration with ruff, mypy, and standard hooks."""
    try:
        add_pre_commit(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-github-actions")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_github_actions_cmd(path: str) -> None:
    """Add GitHub Actions workflows for CI, release, and docs."""
    try:
        add_github_actions(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-rich")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_rich(path: str) -> None:
    """Add a rich-based _messages.py module for user output."""
    from packright.use_rich import add_rich

    try:
        add_rich(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-errors")
@click.option(
    "--path", default=".", help="Project directory."
)
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
@click.option(
    "--path", default=".", help="Project directory."
)
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


@main.command("use-readme")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_readme(path: str) -> None:
    """Add a README.md with badges, install instructions, and quickstart."""
    from packright.use_readme import add_readme

    try:
        add_readme(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-ruff")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_ruff(path: str) -> None:
    """Add ruff linter configuration to pyproject.toml."""
    from packright.use_ruff import add_ruff

    try:
        add_ruff(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-coverage")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_coverage(path: str) -> None:
    """Add coverage configuration to pyproject.toml."""
    from packright.use_coverage import add_coverage

    try:
        add_coverage(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-git")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_git(path: str) -> None:
    """Initialize a git repository with .gitignore and initial commit."""
    from packright.use_git import add_git

    try:
        add_git(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("bump-version")
@click.option(
    "--path", default=".", help="Project directory."
)
@click.option(
    "--part",
    default="patch",
    type=click.Choice(["major", "minor", "patch"]),
    help="Which version part to bump. Defaults to patch.",
)
def bump_version_cmd(path: str, part: str) -> None:
    """Bump the project version in pyproject.toml."""
    from packright.use_version import bump_version

    try:
        bump_version(project_dir=path, part=part)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command()
@click.option(
    "--path", default=".", help="Project directory."
)
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


@main.command("use-docker")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_docker(path: str) -> None:
    """Add Dockerfile and .dockerignore to the project."""
    from packright.use_docker import add_docker

    try:
        add_docker(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-mypy")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_mypy(path: str) -> None:
    """Add mypy configuration to pyproject.toml and create py.typed marker."""
    from packright.use_mypy import add_mypy

    try:
        add_mypy(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("browse-pypi")
@click.option(
    "--path", default=".", help="Project directory."
)
def browse_pypi_cmd(path: str) -> None:
    """Open the project's PyPI page in the browser."""
    from packright.browse import browse_pypi

    try:
        browse_pypi(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("browse-github")
@click.option(
    "--path", default=".", help="Project directory."
)
def browse_github_cmd(path: str) -> None:
    """Open the project's GitHub repository in the browser."""
    from packright.browse import browse_github

    try:
        browse_github(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("browse-docs")
@click.option(
    "--path", default=".", help="Project directory."
)
def browse_docs_cmd(path: str) -> None:
    """Open the project's documentation in the browser."""
    from packright.browse import browse_docs

    try:
        browse_docs(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-gitlab-ci")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_gitlab_ci(path: str) -> None:
    """Add GitLab CI configuration with lint, test, and publish stages."""
    from packright.use_gitlab_ci import add_gitlab_ci

    try:
        add_gitlab_ci(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("init")
@click.option(
    "--path",
    default=".",
    help="Parent directory to create the package in.",
)
def init(path: str) -> None:
    """Interactively create a new Python package."""
    from packright.init_interactive import init_project

    try:
        init_project(parent=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("doctor")
def doctor() -> None:
    """Check the development environment for required tools."""
    from packright.doctor import check_environment

    passed, total = check_environment()
    if passed < total:
        sys.exit(1)


@main.command("use-github")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_github(path: str) -> None:
    """Create a GitHub repository and link it to the project."""
    from packright.use_github import add_github

    try:
        add_github(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-changelog")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_changelog(path: str) -> None:
    """Add a CHANGELOG.md following the Keep a Changelog format."""
    from packright.use_changelog import add_changelog

    try:
        add_changelog(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-contributing")
@click.option(
    "--path", default=".", help="Project directory."
)
def use_contributing(path: str) -> None:
    """Add contributing guidelines, code of conduct, and issue templates."""
    from packright.use_contributing import add_contributing

    try:
        add_contributing(project_dir=path)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-module")
@click.option(
    "--path", default=".", help="Project directory."
)
@click.argument("name")
def use_module(path: str, name: str) -> None:
    """Scaffold a new module and its matching test file."""
    from packright.use_module import add_module_with_test

    try:
        add_module_with_test(project_dir=path, name=name)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-dep")
@click.argument("name")
@click.option(
    "--path", default=".", help="Project directory."
)
@click.option(
    "--version", default=None, help="Minimum version constraint (e.g., 2.31).",
)
def use_dep(name: str, path: str, version: str | None) -> None:
    """Add a runtime dependency via uv."""
    from packright.use_dep import add_dep

    try:
        add_dep(project_dir=path, name=name, version=version)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e


@main.command("use-dev-dep")
@click.argument("name")
@click.option(
    "--path", default=".", help="Project directory."
)
@click.option(
    "--version", default=None, help="Minimum version constraint (e.g., 2.31).",
)
def use_dev_dep(name: str, path: str, version: str | None) -> None:
    """Add a development dependency via uv."""
    from packright.use_dep import add_dev_dep

    try:
        add_dev_dep(project_dir=path, name=name, version=version)
    except PackrightError as e:
        abort(str(e))
        raise SystemExit(1) from e
