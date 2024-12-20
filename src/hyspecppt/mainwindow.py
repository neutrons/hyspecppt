"""Main Qt window"""

from qtpy.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

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
        HPPT_view = HyspecPPTView(self)
        HPPT_model = HyspecPPTModel()
        self.HPPT_presenter = HyspecPPTPresenter(HPPT_view, HPPT_model)

        ### Set the layout
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
        help_function(context="HPPT_View")
