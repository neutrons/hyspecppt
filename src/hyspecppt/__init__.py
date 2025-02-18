"""Contains the entry point for the application"""

try:
    from ._version import __version__  # noqa: F401
except ImportError:
    __version__ = "unknown"


def Hyspecppt():  # noqa: N802
    """Start Class"""
    """
    This is needed for backward compatibility because mantid workbench does
    "from hyspecppt import Hyspecppt"
    """
    from .hyspecpptmain import HyspecPPT as hyspecppt  # noqa: E501, N813

    return hyspecppt()
