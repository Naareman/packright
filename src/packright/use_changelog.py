"""Add a CHANGELOG.md following the Keep a Changelog format.

Equivalent to usethis::use_news_md() in R.
"""

from __future__ import annotations

from pathlib import Path

from packright._messages import success, warn

_CHANGELOG_CONTENT = """\
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- Initial release
"""


def add_changelog(project_dir: str = ".") -> None:
    """Create a CHANGELOG.md in the project root.

    Uses the `Keep a Changelog <https://keepachangelog.com/>`_ format with
    an ``[Unreleased]`` section seeded with "Initial release".

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    changelog_path = root / "CHANGELOG.md"

    if changelog_path.exists():
        warn("CHANGELOG.md already exists — skipping.")
        return

    changelog_path.write_text(_CHANGELOG_CONTENT, encoding="utf-8")
    success("Created CHANGELOG.md")
