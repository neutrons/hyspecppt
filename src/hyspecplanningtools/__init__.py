"""Contains the entry point for the application"""

try:
    from ._version import __version__  # noqa: F401
except ImportError:
    __version__ = "unknown"


def HyspecPlanningTool():  # noqa: N802
    """This is needed for backward compatibility because mantid workbench does
    "from hyspecplanningtools import HyspecPlanningTool"
    """
    from .hyspecplanningtools import HyspecPlanningTool as hyspecplanningtools  # noqa: E501, N813

    return hyspecplanningtools()
