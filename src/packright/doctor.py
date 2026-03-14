"""Check the development environment for required tools.

Reports on Python version, uv, git, gh CLI, and ruff availability.
"""

from __future__ import annotations

import subprocess
import sys

from packright._messages import info, success, warn


def check_environment() -> tuple[int, int]:
    """Check and report on the development environment.

    Verifies that required and recommended tools are installed and
    configured correctly.

    Returns:
        A tuple of (passed, total) check counts.
    """
    passed = 0
    total = 0

    info("Checking development environment...\n")

    # 1. Python version >= 3.10
    total += 1
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 10):
        success(f"Python {py_version}")
        passed += 1
    else:
        warn(f"Python {py_version} — 3.10+ required")

    # 2. uv installed
    total += 1
    if _check_command(["uv", "--version"], "uv"):
        passed += 1

    # 3. git installed
    total += 1
    if _check_command(["git", "--version"], "git"):
        passed += 1

    # 4. git user.name configured
    total += 1
    if _check_git_config("user.name"):
        passed += 1

    # 5. git user.email configured
    total += 1
    if _check_git_config("user.email"):
        passed += 1

    # 6. gh CLI installed
    total += 1
    if _check_command(["gh", "--version"], "gh CLI"):
        passed += 1

    # 7. gh authenticated
    total += 1
    if _check_command(["gh", "auth", "status"], "gh auth"):
        passed += 1

    # 8. ruff installed
    total += 1
    if _check_command(["ruff", "--version"], "ruff"):
        passed += 1

    info(f"\n{passed}/{total} checks passed")
    return passed, total


def _check_command(cmd: list[str], label: str) -> bool:
    """Run a command and report pass/fail.

    Args:
        cmd: Command and arguments to run.
        label: Human-readable label for the check.

    Returns:
        True if the command succeeded, False otherwise.
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            version_line = result.stdout.strip().split("\n")[0]
            success(f"{label}: {version_line}")
            return True
        warn(f"{label}: not working")
        return False
    except FileNotFoundError:
        warn(f"{label}: not installed")
        return False
    except subprocess.TimeoutExpired:
        warn(f"{label}: timed out")
        return False


def _check_git_config(key: str) -> bool:
    """Check if a git config key is set.

    Args:
        key: Git config key (e.g., "user.name").

    Returns:
        True if the key is configured, False otherwise.
    """
    try:
        result = subprocess.run(
            ["git", "config", key],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            success(f"git {key}: {result.stdout.strip()}")
            return True
        warn(f"git {key}: not configured")
        return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        warn(f"git {key}: cannot check (git not available)")
        return False
