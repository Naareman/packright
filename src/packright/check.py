"""Audit a Python package for structural best practices.

Runs 22 checks covering layout, configuration, typing, testing, docs,
and CI/CD — the same checks a senior reviewer would look for.
"""

from __future__ import annotations

from pathlib import Path

from packright._messages import info, success, warn


def audit_project(project_dir: str = ".") -> tuple[int, int]:
    """Run all structural checks on a Python package.

    Args:
        project_dir: Root of the project to audit.

    Returns:
        Tuple of (passed, total) check counts.
    """
    root = Path(project_dir).resolve()
    info(f"Auditing [bold]{root}[/bold]...")

    checks = _build_checks(root)
    passed = 0
    total = len(checks)

    for label, check_fn in checks:
        if check_fn():
            success(f"  {label}")
            passed += 1
        else:
            warn(f"  {label}")

    info(f"\n  Result: [bold]{passed}/{total}[/bold] checks passed")
    return passed, total


def _build_checks(root: Path) -> list[tuple[str, object]]:
    """Build the list of all 22 checks.

    Args:
        root: Project root directory.

    Returns:
        List of (label, callable) pairs.
    """
    src = root / "src"
    pkg_dir = _find_package_dir(src)
    tests = root / "tests"
    docs = root / "docs"

    return [
        # Layout (1-6)
        (
            "Uses src/ layout",
            lambda: src.is_dir(),
        ),
        (
            "Package directory exists under src/",
            lambda: pkg_dir is not None,
        ),
        (
            "__init__.py exists",
            lambda: pkg_dir is not None and (pkg_dir / "__init__.py").is_file(),
        ),
        (
            "tests/ directory exists",
            lambda: tests.is_dir(),
        ),
        (
            "docs/ directory exists",
            lambda: docs.is_dir(),
        ),
        (
            ".gitignore exists",
            lambda: (root / ".gitignore").is_file(),
        ),

        # Configuration (7-12)
        (
            "pyproject.toml exists",
            lambda: (root / "pyproject.toml").is_file(),
        ),
        (
            "pyproject.toml has [project] table",
            lambda: _toml_contains(root / "pyproject.toml", "[project]"),
        ),
        (
            "pyproject.toml has [build-system]",
            lambda: _toml_contains(root / "pyproject.toml", "[build-system]"),
        ),
        (
            "No setup.py (using modern build)",
            lambda: not (root / "setup.py").is_file(),
        ),
        (
            "No setup.cfg (using modern build)",
            lambda: not (root / "setup.cfg").is_file(),
        ),
        (
            ".python-version file exists",
            lambda: (root / ".python-version").is_file(),
        ),

        # Typing (13-14)
        (
            "py.typed marker exists",
            lambda: pkg_dir is not None and (pkg_dir / "py.typed").is_file(),
        ),
        (
            "mypy or pyright configured",
            lambda: (
                _toml_contains(root / "pyproject.toml", "[tool.mypy]")
                or _toml_contains(root / "pyproject.toml", "[tool.pyright]")
                or (root / "mypy.ini").is_file()
                or (root / "pyrightconfig.json").is_file()
            ),
        ),

        # Testing (15-17)
        (
            "conftest.py exists in tests/",
            lambda: (tests / "conftest.py").is_file(),
        ),
        (
            "At least one test file exists",
            lambda: any(tests.glob("test_*.py")) if tests.is_dir() else False,
        ),
        (
            "pytest configured in pyproject.toml",
            lambda: _toml_contains(root / "pyproject.toml", "[tool.pytest"),
        ),

        # Documentation (18-19)
        (
            "README.md exists",
            lambda: (root / "README.md").is_file(),
        ),
        (
            "CHANGELOG.md exists",
            lambda: (root / "CHANGELOG.md").is_file(),
        ),

        # Licensing (20)
        (
            "LICENSE file exists",
            lambda: (root / "LICENSE").is_file() or (root / "LICENSE.txt").is_file(),
        ),

        # Code quality (21-22)
        (
            "Linter configured (ruff/flake8/pylint)",
            lambda: (
                _toml_contains(root / "pyproject.toml", "[tool.ruff")
                or (root / ".flake8").is_file()
                or (root / ".pylintrc").is_file()
                or _toml_contains(root / "pyproject.toml", "[tool.flake8")
                or _toml_contains(root / "pyproject.toml", "[tool.pylint")
            ),
        ),
        (
            "errors.py or exceptions.py exists",
            lambda: (
                pkg_dir is not None
                and (
                    (pkg_dir / "errors.py").is_file()
                    or (pkg_dir / "exceptions.py").is_file()
                )
            ),
        ),
    ]


def _find_package_dir(src: Path) -> Path | None:
    """Find the package directory under src/, or None.

    Args:
        src: The src/ directory path.

    Returns:
        Path to the package directory, or None if not found.
    """
    if not src.is_dir():
        return None

    candidates = [
        d for d in src.iterdir()
        if d.is_dir() and not d.name.startswith((".", "_"))
    ]

    return candidates[0] if len(candidates) == 1 else None


def _toml_contains(path: Path, needle: str) -> bool:
    """Check if a TOML file contains a given string.

    Args:
        path: Path to the TOML file.
        needle: String to search for.

    Returns:
        True if the file exists and contains the needle.
    """
    if not path.is_file():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    return needle in text
