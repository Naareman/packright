"""Interactive project initialization.

Prompts the user for project metadata and scaffolds a new package.
"""

from __future__ import annotations

import re
from pathlib import Path

import click

from packright._messages import info, success
from packright.scaffold import create_package


def init_project(parent: str = ".") -> None:
    """Interactively create a new Python package.

    Prompts the user for project name, description, author details,
    license, and minimum Python version, then scaffolds the project
    and patches pyproject.toml with the collected metadata.

    Args:
        parent: Parent directory to create the package in. Defaults to ".".
    """
    info("Initializing a new Python package...")

    name = click.prompt("Package name")
    description = click.prompt("Description", default="")
    author_name = click.prompt("Author name", default="")
    author_email = click.prompt("Author email", default="")
    license_type = click.prompt("License", default="MIT")
    python_version = click.prompt("Minimum Python version", default=">=3.10")

    # Scaffold the project
    project_path = create_package(name, parent=parent)

    # Patch pyproject.toml with collected metadata
    pyproject_path = project_path / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")

    # Update description
    if description:
        content = re.sub(
            r'description\s*=\s*"[^"]*"',
            f'description = "{description}"',
            content,
            count=1,
        )

    # Add authors if provided
    if author_name or author_email:
        author_entry = "["
        if author_name:
            author_entry += f'name = "{author_name}"'
        if author_name and author_email:
            author_entry += ", "
        if author_email:
            author_entry += f'email = "{author_email}"'
        author_entry += "]"

        # Insert authors after description line
        content = content.replace(
            'requires-python',
            f'authors = [{author_entry}]\nrequires-python',
        )

    # Update license
    if license_type:
        content = content.replace(
            'requires-python',
            f'license = "{license_type}"\nrequires-python',
        )

    # Update Python version
    if python_version != ">=3.10":
        content = content.replace(
            'requires-python = ">=3.10"',
            f'requires-python = "{python_version}"',
        )

    pyproject_path.write_text(content, encoding="utf-8")

    # Print summary
    success(f"Package [bold]{name}[/bold] created at {project_path}")
    info("Summary:")
    info(f"  Name:        {name}")
    if description:
        info(f"  Description: {description}")
    if author_name:
        info(f"  Author:      {author_name}")
    if author_email:
        info(f"  Email:       {author_email}")
    info(f"  License:     {license_type}")
    info(f"  Python:      {python_version}")
    info("")
    info("Next steps:")
    info(f"  cd {project_path}")
    info("  uv sync")
    info("  uv run pytest")
