"""Tests for packright.use_dep."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from packright.use_dep import add_dep, add_dev_dep


def test_add_dep_calls_uv(minimal_project: Path) -> None:
    """Verify that add_dep invokes ``uv add <name>``."""
    with patch("packright.use_dep.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""

        add_dep(str(minimal_project), name="requests")

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args == ["uv", "add", "requests"]


def test_add_dep_with_version(minimal_project: Path) -> None:
    """Verify that add_dep passes the version constraint."""
    with patch("packright.use_dep.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""

        add_dep(str(minimal_project), name="requests", version="2.31")

        args = mock_run.call_args[0][0]
        assert args == ["uv", "add", "requests>=2.31"]


def test_add_dev_dep_calls_uv_with_group(minimal_project: Path) -> None:
    """Verify that add_dev_dep invokes ``uv add --group dev <name>``."""
    with patch("packright.use_dep.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""

        add_dev_dep(str(minimal_project), name="pytest")

        args = mock_run.call_args[0][0]
        assert args == ["uv", "add", "--group", "dev", "pytest"]


def test_add_dep_warns_on_failure(minimal_project: Path) -> None:
    """Verify that a failed uv add does not raise."""
    with patch("packright.use_dep.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = "Package not found"

        # Should not raise
        add_dep(str(minimal_project), name="nonexistent-pkg-xyz")
