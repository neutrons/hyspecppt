"""Main Qt window"""

from qtpy.QtWidgets import QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QWidget

from hyspecppt.help.help_model import help_function
from hyspecppt.hppt.hppt_model import HyspecPPTModel
from hyspecppt.hppt.hppt_presenter import HyspecPPTPresenter
from hyspecppt.hppt.hppt_view import HyspecPPTView


class MainWindow(QWidget):
    """Main widget"""

    def __init__(self, parent=None):
        """Constructor"""
        super().__init__(parent)

        ### Create tabs here ###

        ### Main tab
        self.tabs = QTabWidget()
        home = HyspecPPTView(self)
        home_model = HyspecPPTModel()
        self.home_presenter = HyspecPPTPresenter(home, home_model)
        self.tabs.addTab(home, "Home")

        ### Set tab layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

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
        self.home = home

    def handle_help(self):
        """Get current tab type and open the corresponding help page"""
        open_tab = self.tabs.currentWidget()
        if isinstance(open_tab, HyspecPPTView):
            context = "home"
        else:
            context = ""
        help_function(context=context)
