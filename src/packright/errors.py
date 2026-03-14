"""Structured exceptions for packright."""


class PackrightError(Exception):
    """Base exception for packright. Catch this to handle any packright error."""


class ScaffoldError(PackrightError):
    """Raised when package scaffolding fails.

    Args:
        message: Human-readable error description.
        path: The path where scaffolding was attempted.
    """

    def __init__(self, message: str, path: str | None = None) -> None:
        self.path = path
        super().__init__(message)


class FileExistsError(PackrightError):
    """Raised when a file already exists and would be overwritten.

    Args:
        message: Human-readable error description.
        path: The path that already exists.
    """

    def __init__(self, message: str, path: str | None = None) -> None:
        self.path = path
        super().__init__(message)


class ConfigError(PackrightError):
    """Raised when pyproject.toml or other config is invalid or missing.

    Args:
        message: Human-readable error description.
        field: The config field that's problematic.
    """

    def __init__(self, message: str, field: str | None = None) -> None:
        self.field = field
        super().__init__(message)
