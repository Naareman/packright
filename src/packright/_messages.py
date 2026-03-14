"""Centralized user-facing messages using rich.

This is the Python equivalent of R's cli package.
All user output goes through these functions — never bare print().
"""

from rich.console import Console

console = Console()
err_console = Console(stderr=True)


def info(message: str) -> None:
    """Informational message — something is happening."""
    console.print(f"[bold blue]i[/bold blue] {message}")


def success(message: str) -> None:
    """Something completed successfully."""
    console.print(f"[bold green]v[/bold green] {message}")


def warn(message: str) -> None:
    """Non-fatal warning — something unexpected but recoverable."""
    err_console.print(f"[bold yellow]![/bold yellow] {message}")


def abort(message: str) -> None:
    """Fatal error message before raising an exception."""
    err_console.print(f"[bold red]x[/bold red] {message}")
