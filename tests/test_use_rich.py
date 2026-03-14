"""Tests for packright.use_rich."""

from __future__ import annotations

from pathlib import Path


def test_add_rich_creates_messages_module(minimal_project: Path) -> None:
    """add_rich() creates _messages.py in the package directory."""
    from packright.use_rich import add_rich

    add_rich(project_dir=str(minimal_project))

    messages_py = minimal_project / "src" / "test_pkg" / "_messages.py"
    assert messages_py.exists()
    content = messages_py.read_text()
    assert "Console" in content
    assert "def info" in content
    assert "def success" in content
    assert "def warn" in content
    assert "def abort" in content


def test_add_rich_skips_if_exists(minimal_project: Path) -> None:
    """add_rich() warns and skips if _messages.py already exists."""
    from packright.use_rich import add_rich

    messages_py = minimal_project / "src" / "test_pkg" / "_messages.py"
    messages_py.write_text("# existing", encoding="utf-8")

    add_rich(project_dir=str(minimal_project))

    assert messages_py.read_text() == "# existing"
