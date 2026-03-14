"""packright: Automate Python package development the right way."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("packright")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"

from packright.errors import PackrightError

__all__ = [
    "PackrightError",
    "__version__",
]
