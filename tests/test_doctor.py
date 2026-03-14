"""Tests for packright.doctor."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

from packright.doctor import check_environment


def _make_run_side_effect(passing_commands: set[str]):
    """Create a subprocess.run side effect that passes for given commands.

    Args:
        passing_commands: Set of command strings (first arg) that should succeed.

    Returns:
        A side effect function for unittest.mock.patch.
    """
    def side_effect(cmd, **kwargs):
        cmd_str = cmd[0] if cmd else ""
        # For git config, include the key in the lookup
        if cmd_str == "git" and len(cmd) >= 3 and cmd[1] == "config":
            lookup = f"git config {cmd[2]}"
        elif cmd_str == "gh" and len(cmd) >= 3 and cmd[1] == "auth":
            lookup = "gh auth status"
        elif cmd_str == "git" and len(cmd) >= 2 and cmd[1] == "--version":
            lookup = "git"
        elif cmd_str == "gh" and len(cmd) >= 2 and cmd[1] == "--version":
            lookup = "gh"
        else:
            lookup = cmd_str

        if lookup in passing_commands:
            return subprocess.CompletedProcess(
                cmd, 0, stdout=f"{lookup} 1.0.0\n", stderr=""
            )
        return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="error")

    return side_effect


def test_check_environment_all_pass() -> None:
    """Verify that all checks pass when all tools are available."""
    all_commands = {
        "uv", "git", "git config user.name",
        "git config user.email", "gh", "gh auth status",
        "ruff",
    }

    mock_run = _make_run_side_effect(all_commands)
    with patch("packright.doctor.subprocess.run", side_effect=mock_run):
        passed, total = check_environment()

    assert passed == total, (
        f"Expected all {total} checks to pass, got {passed}"
    )


def test_check_environment_some_fail() -> None:
    """Verify that missing tools are reported as failures."""
    # Only git and Python pass
    some_commands = {
        "git", "git config user.name", "git config user.email",
    }
    mock_run = _make_run_side_effect(some_commands)
    with patch(
        "packright.doctor.subprocess.run",
        side_effect=mock_run,
    ):
        passed, total = check_environment()

    assert total == 7, f"Expected 7 total checks, got {total}"
    # git + git user.name + git user.email = 3
    assert passed == 3, f"Expected 3 checks to pass, got {passed}"


def test_check_environment_tool_not_found() -> None:
    """Verify that FileNotFoundError is handled for missing commands."""
    def side_effect(cmd, **kwargs):
        raise FileNotFoundError(f"{cmd[0]} not found")

    with patch("packright.doctor.subprocess.run", side_effect=side_effect):
        passed, total = check_environment()

    # No checks pass (all use subprocess)
    assert passed == 0, f"Expected 0 checks to pass, got {passed}"
    assert total == 7
