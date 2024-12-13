"""Main Qt window"""

from qtpy.QtWidgets import QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QWidget, QLabel, QLineEdit, QGridLayout

from hyspecppt.help.help_model import help_function
from hyspecppt.hppt.hppt_model import HyspecPPTModel
from hyspecppt.hppt.hppt_presenter import HyspecPPTPresenter
from hyspecppt.hppt.hppt_view import HyspecPPTView


class MainWindow(QWidget):
    """Main widget"""

    def __init__(self, parent=None):
        """Constructor"""
        super().__init__(parent)

        ### Create widgets here ###

        ### Main tab
        # self.tabs = QTabWidget()
        HPPT_view = HyspecPPTView(self)
        HPPT_model = HyspecPPTModel()
        self.HPPT_presenter = HyspecPPTPresenter(HPPT_view, HPPT_model)
        # self.tabs.addTab(home, "Home")

        ### Set tab layout
        layout = QVBoxLayout()
        layout.addWidget(HPPT_view)

        ### Create bottom interface here ###

        # Help button
        help_button = QPushButton("Help")
        help_button.clicked.connect(self.handle_help)

        # Set bottom interface layout
        hor_layout = QHBoxLayout()
        hor_layout.addWidget(help_button)

        layout.addLayout(hor_layout)

        self.setLayout(layout)

        # register child widgets to make testing easier
        self.HPPT_view = HPPT_view

    def handle_help(self):
        """Get current tab type and open the corresponding help page"""
        open_tab = self.HPPT_view.parentWidget()
        if isinstance(open_tab, HyspecPPTView):
            context = "HPPT_View"
        else:
            context = ""
        help_function(context=context)