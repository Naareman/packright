"""Tests for packright.errors."""

from packright.errors import (
    ConfigError,
    FileExistsError,
    PackrightError,
    ScaffoldError,
)


def test_packright_error_is_base():
    assert issubclass(ScaffoldError, PackrightError)
    assert issubclass(FileExistsError, PackrightError)
    assert issubclass(ConfigError, PackrightError)


def test_scaffold_error_has_path():
    err = ScaffoldError("something failed", path="/tmp/pkg")
    assert err.path == "/tmp/pkg"
    assert "something failed" in str(err)


def test_file_exists_error_has_path():
    err = FileExistsError("already exists", path="/tmp/pkg")
    assert err.path == "/tmp/pkg"


def test_config_error_has_field():
    err = ConfigError("invalid config", field="license")
    assert err.field == "license"
