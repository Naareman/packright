"""Add a LICENSE file to a project.

Currently supports MIT license. More license types can be added later.
"""

from __future__ import annotations

import datetime
from pathlib import Path

from packright._messages import info, success, warn
from packright.errors import ConfigError

_MIT_TEXT = """\
MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

_SUPPORTED_LICENSES = {"MIT"}


def add_license(
    project_dir: str = ".",
    license_type: str = "MIT",
    author: str = "Your Name",
) -> Path:
    """Create a LICENSE file at the project root.

    Args:
        project_dir: Root of the project.
        license_type: License type. Only "MIT" is supported currently.
        author: Copyright holder name.

    Returns:
        Path to the created LICENSE file.

    Raises:
        ConfigError: If the license type is not supported.
    """
    license_type = license_type.upper()
    if license_type not in _SUPPORTED_LICENSES:
        raise ConfigError(
            f"Unsupported license type: {license_type!r}. "
            f"Supported: {', '.join(sorted(_SUPPORTED_LICENSES))}.",
            field="license",
        )

    root = Path(project_dir).resolve()
    target = root / "LICENSE"

    if target.exists():
        warn(f"[bold]{target}[/bold] already exists — skipping.")
        return target

    year = datetime.datetime.now(tz=datetime.timezone.utc).year
    content = _MIT_TEXT.format(year=year, author=author)
    target.write_text(content, encoding="utf-8")
    success(f"Created [bold]{target}[/bold] ({license_type})")
    info(f"Copyright (c) {year} {author}")
    return target
