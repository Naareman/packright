"""Tests for packright.cli."""

from __future__ import annotations

from click.testing import CliRunner

from packright import __version__
from packright.cli import main


def test_scaffold_command(tmp_path: object) -> None:
    """Verify that the scaffold command creates a package directory."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["scaffold", "my-lib"])

        assert result.exit_code == 0, (
            f"scaffold should succeed, got: {result.output}"
        )
        assert "my-lib" in result.output


def test_check_command(tmp_path: object) -> None:
    """Verify that the check command runs against a project directory."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # First scaffold a project so check has something to audit
        runner.invoke(main, ["scaffold", "my-lib"])

        result = runner.invoke(main, ["check", "--path", "my-lib"])

        # check command should exit cleanly (0 or 1 depending on audit)
        assert result.exit_code in {0, 1}, (
            f"check should exit 0 or 1, got {result.exit_code}: {result.output}"
        )


def test_version_flag() -> None:
    """Verify that --version prints the current version."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output, (
        f"--version should include {__version__}, got: {result.output}"
    )
