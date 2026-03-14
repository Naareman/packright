"""Add GitLab CI configuration to an existing project.

Creates a .gitlab-ci.yml with lint, test, and publish stages.
"""

from __future__ import annotations

from pathlib import Path

from packright._messages import success, warn

_GITLAB_CI = """\
stages:
  - lint
  - test
  - publish

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip

lint:
  stage: lint
  image: python:3.12-slim
  before_script:
    - pip install uv
    - uv sync --no-dev
  script:
    - uv run ruff check .

test:
  stage: test
  image: python:3.12-slim
  before_script:
    - pip install uv
    - uv sync
  script:
    - uv run pytest

publish:
  stage: publish
  image: python:3.12-slim
  only:
    - tags
  before_script:
    - pip install uv
    - uv sync --no-dev
  script:
    - uv build
    - uv publish
"""


def add_gitlab_ci(project_dir: str = ".") -> None:
    """Add a .gitlab-ci.yml with lint, test, and publish stages.

    The configuration uses a Python 3.12 image, installs uv for dependency
    management, runs ruff for linting, pytest for testing, and builds and
    publishes on tagged commits.

    Args:
        project_dir: Root directory of the project. Defaults to ".".
    """
    root = Path(project_dir).resolve()
    ci_path = root / ".gitlab-ci.yml"

    if ci_path.exists():
        warn(".gitlab-ci.yml already exists — skipping.")
        return

    ci_path.write_text(_GITLAB_CI, encoding="utf-8")
    success("Created .gitlab-ci.yml")
