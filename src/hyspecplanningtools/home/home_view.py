"""PyQt widget for the main tab"""

from qtpy.QtWidgets import QHBoxLayout, QWidget


class Home(QWidget):
    """Main widget"""

    def __init__(self, parent=None):
        """Constructor"""
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
