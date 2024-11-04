"""Version Tests"""

import sys

import pytest

from hyspecplanningtools import __version__


def test_version():
    """Test that the version is imported"""
    assert __version__ != "unknown"


def test_version_error(monkeypatch):
    """Test that the version is set to unknown."""
    monkeypatch.setitem(sys.modules, "hyspecplanningtools", None)
    with pytest.raises(ImportError):
        from hyspecplanningtools import __version__

        assert __version__ == "unknown"
