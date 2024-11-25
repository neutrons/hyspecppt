"""Version Tests"""

import sys

import pytest

from hyspecppt import __version__


def test_version():
    """Test that the version is imported"""
    assert __version__ != "unknown"


def test_version_error(monkeypatch):
    """Test that the version is set to unknown."""
    monkeypatch.setitem(sys.modules, "hyspecppt", None)
    with pytest.raises(ImportError):
        from hyspecppt import __version__

        assert __version__ == "unknown"
