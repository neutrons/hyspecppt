"""Main Qt application"""

import logging
import sys

from qtpy.QtWidgets import QApplication, QMainWindow

from hyspecplanningtools import __version__
from hyspecplanningtools.configuration import Configuration
from hyspecplanningtools.mainwindow import MainWindow

logger = logging.getLogger("hyspecplanningtools")


class HyspecPlanningTool(QMainWindow):
    """Main Package window"""

    __instance = None

    def __new__(cls):
        if HyspecPlanningTool.__instance is None:
            HyspecPlanningTool.__instance = QMainWindow.__new__(cls)  # pylint: disable=no-value-for-parameter
        return HyspecPlanningTool.__instance

    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info(f"HyspecPlanningTool version: {__version__}")
        config = Configuration()

        if not config.is_valid():
            msg = (
                "Error with configuration settings!",
                f"Check and update your file: {config.config_file_path}",
                "with the latest settings found here:",
                f"{config.template_file_path} and start the application again.",
            )

            print(" ".join(msg))
            sys.exit(-1)
        self.setWindowTitle(f"HyspecPlanning Tools - {__version__}")
        self.main_window = MainWindow(self)
        self.setCentralWidget(self.main_window)


def gui():
    """Main entry point for Qt application"""
    input_flags = sys.argv[1::]
    if "--v" in input_flags or "--version" in input_flags:
        print(__version__)
        sys.exit()
    else:
        app = QApplication(sys.argv)
        window = HyspecPlanningTool()
        window.show()
        sys.exit(app.exec_())
