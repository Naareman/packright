"""Add contributing guidelines, code of conduct, and issue templates.

Equivalent to usethis::use_tidy_contributing() in R.
"""

from __future__ import annotations

from pathlib import Path

from packright._config import get_package_name
from packright._messages import success, warn

_CONTRIBUTING_MD = """\
# Contributing

Thank you for considering contributing to this project!

## How to Report Issues

1. Search existing issues to avoid duplicates.
2. Open a new issue with a clear title and detailed description.
3. Include steps to reproduce bugs, expected vs actual behaviour, and your environment.

## How to Submit Pull Requests

1. Fork the repository and create a feature branch from `main`.
2. Install the development environment:
   ```bash
   uv sync
   ```
3. Make your changes, adding tests where appropriate.
4. Run the test suite:
   ```bash
   uv run pytest
   ```
5. Open a pull request with a clear description of your changes.

## Development Setup

```bash
# Clone your fork
git clone https://github.com/<you>/{name}.git
cd {name}

# Install dependencies (requires uv)
uv sync

# Run tests
uv run pytest

# Run linter
uv run ruff check .
```
"""

_CODE_OF_CONDUCT_MD = """\
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, caste, colour, religion, or sexual
identity and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards

Examples of behaviour that contributes to a positive environment for our
community include:

* Demonstrating empathy and kindness toward other people
* Being respectful of differing opinions, viewpoints, and experiences
* Giving and gracefully accepting constructive feedback
* Accepting responsibility and apologising to those affected by our mistakes,
  and learning from the experience
* Focusing on what is best not just for us as individuals, but for the overall
  community

Examples of unacceptable behaviour include:

* The use of sexualised language or imagery, and sexual attention or advances of
  any kind
* Trolling, insulting or derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or email address,
  without their explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behaviour may be
reported to the project maintainers. All complaints will be reviewed and
investigated and will result in a response that is deemed necessary and
appropriate to the circumstances.

## Attribution

This Code of Conduct is adapted from the
[Contributor Covenant](https://www.contributor-covenant.org), version 2.1,
available at
<https://www.contributor-covenant.org/version/2/1/code_of_conduct.html>.
"""

_BUG_REPORT_MD = """\
---
name: Bug report
about: Create a report to help us improve
title: "[BUG] "
labels: bug
assignees: ''
---

## Describe the bug
A clear and concise description of what the bug is.

## To Reproduce
Steps to reproduce the behaviour:
1. Install '...'
2. Run '...'
3. See error

## Expected behaviour
A clear and concise description of what you expected to happen.

## Environment
- OS: [e.g. macOS 14, Ubuntu 22.04]
- Python: [e.g. 3.12]
- Package version: [e.g. 0.1.0]

## Additional context
Add any other context about the problem here.
"""

_FEATURE_REQUEST_MD = """\
---
name: Feature request
about: Suggest an idea for this project
title: "[FEATURE] "
labels: enhancement
assignees: ''
---

## Is your feature request related to a problem?
A clear and concise description of what the problem is.

## Describe the solution you'd like
A clear and concise description of what you want to happen.

## Describe alternatives you've considered
A clear and concise description of any alternative solutions or features.

## Additional context
Add any other context or screenshots about the feature request here.
"""


def add_contributing(project_dir: str = ".") -> None:
    """Create CONTRIBUTING.md, CODE_OF_CONDUCT.md, and GitHub issue templates.

    Creates the following files (skipping any that already exist):
    - ``CONTRIBUTING.md``
    - ``CODE_OF_CONDUCT.md``
    - ``.github/ISSUE_TEMPLATE/bug_report.md``
    - ``.github/ISSUE_TEMPLATE/feature_request.md``

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    name = get_package_name(project_dir)

    # CONTRIBUTING.md
    _write_if_missing(
        root / "CONTRIBUTING.md",
        _CONTRIBUTING_MD.replace("{name}", name),
    )

    # CODE_OF_CONDUCT.md
    _write_if_missing(root / "CODE_OF_CONDUCT.md", _CODE_OF_CONDUCT_MD)

    # Issue templates
    templates_dir = root / ".github" / "ISSUE_TEMPLATE"
    templates_dir.mkdir(parents=True, exist_ok=True)

    _write_if_missing(templates_dir / "bug_report.md", _BUG_REPORT_MD)
    _write_if_missing(templates_dir / "feature_request.md", _FEATURE_REQUEST_MD)


def _write_if_missing(path: Path, content: str) -> None:
    """Write *content* to *path* unless it already exists.

    Args:
        path: Target file path.
        content: Text to write.
    """
    if path.exists():
        warn(f"{path.name} already exists — skipping.")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    success(f"Created {path.name}")
