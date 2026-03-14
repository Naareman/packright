"""Template rendering using Jinja2.

Templates live in the templates/ directory alongside this file.
"""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

_TEMPLATE_DIR = Path(__file__).parent / "templates"


def render_template(template_name: str, context: dict[str, str]) -> str:
    """Render a Jinja2 template with the given context.

    Args:
        template_name: Name of the template file (e.g., "pyproject.toml.j2").
        context: Variables to pass to the template.

    Returns:
        Rendered template as a string.
    """
    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATE_DIR)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_name)
    return template.render(**context)
