"""PyQt widget for the main tab"""

from qtpy.QtWidgets import QHBoxLayout, QWidget, QLineEdit, QGridLayout, QLabel, QVBoxLayout, QComboBox


class HyspecPPTView(QWidget):
    """Main widget"""

    def __init__(self, parent=None):
        """Constructor"""
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layoutLeft = QVBoxLayout()
        layout.addLayout(layoutLeft)
        self.EW = ExperimentWidget(self)
        layoutLeft.addWidget(self.EW)
        self.CW = CrosshairWidget(self)
        layoutLeft.addWidget(self.CW)

        self.PW = QLineEdit() # replace this with plot
        layout.addWidget(self.PW)
        self.EW.initalizeCombo(['1','2','3'])
        
class ExperimentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.Ei_edit = QLineEdit(self)
        self.Ei_label = QLabel("&Ei:", self)
        self.Ei_label.setBuddy(self.Ei_edit)

        self.Pangle_edit = QLineEdit(self)
        self.Pangle_label = QLabel("&Polarization angle:", self)
        self.Pangle_label.setBuddy(self.Pangle_edit)

        self.S2_edit = QLineEdit(self)
        self.S2_label = QLabel("&S2:", self)
        self.S2_label.setBuddy(self.S2_edit)

        self.Type_combobox = QComboBox(self)
        self.Type_label = QLabel("&Type:", self)
        self.Type_label.setBuddy(self.Type_combobox)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.Ei_label, 0, 0)
        layout.addWidget(self.Ei_edit, 0, 1)
        
        layout.addWidget(self.Pangle_label, 0, 2)
        layout.addWidget(self.Pangle_edit, 0, 3)

        layout.addWidget(self.S2_label, 1, 0)
        layout.addWidget(self.S2_edit, 1, 1)

        layout.addWidget(self.Type_label, 1, 2)
        layout.addWidget(self.Type_combobox, 1, 3)

    def initalizeCombo(self,options):
        self.Type_combobox.addItems(options)


class CrosshairWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        DeltaE_edit = QLineEdit(self)
        DeltaE_label = QLabel("&DeltaE:", self)
        DeltaE_label.setBuddy(DeltaE_edit)

        modQ_edit = QLineEdit(self)
        modQ_label = QLabel("|&Q|:", self)
        modQ_label.setBuddy(modQ_edit)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(DeltaE_label)
        layout.addWidget(DeltaE_edit)

        layout.addWidget(modQ_label)
        layout.addWidget(modQ_edit)