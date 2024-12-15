"""PyQt widget for the main tab"""

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from qtpy.QtGui import QDoubleValidator
from qtpy.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


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
        self.SelW = SelectorWidget(self)
        layoutLeft.addWidget(self.SelW)
        self.SCW = SingleCrystalWidget(self)
        layoutLeft.addWidget(self.SCW)
        self.CW = CrosshairWidget(self)
        layoutLeft.addWidget(self.CW)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layoutLeft.addItem(spacer)
        self.PW = PrintWidget(self)
        layout.addWidget(self.PW)

        self.switch_to_SC()

        self.EW.initalizeCombo(["1", "2", "3"])
        self.SCW.set_values(dict(a=1, b=2, c=3, alpha=90, beta=90, gamma=120, h=1, k=1, l=0))

    def switch_to_SC(self):
        self.SCW.setVisible(True)
        self.CW.set_Qmod_enabled(False)

    def switch_to_Powder(self):
        self.SCW.setVisible(False)
        self.CW.set_Qmod_enabled(True)


class PrintWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layoutRight = QVBoxLayout()
        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layoutRight.addWidget(self.static_canvas)
        layoutRight.addWidget(NavigationToolbar(self.static_canvas, self))
        self.setLayout(layoutRight)


class SelectorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        selector_layout = QHBoxLayout()

        self.powder_rb = QRadioButton("Po&wder")
        self.sc_rb = QRadioButton("Single C&rystal")

        selector_group = QButtonGroup(self)
        selector_group.addButton(self.powder_rb)
        selector_group.addButton(self.sc_rb)

        selector_layout.addWidget(self.powder_rb)
        selector_layout.addWidget(self.sc_rb)
        self.setLayout(selector_layout)


class SingleCrystalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        lattice_layout = QGridLayout()
        self.a_edit = QLineEdit(self)
        self.a_label = QLabel("&a:", self)
        self.a_label.setBuddy(self.a_edit)

        self.b_edit = QLineEdit(self)
        self.b_label = QLabel("b:", self)
        self.b_label.setBuddy(self.b_edit)

        self.c_edit = QLineEdit(self)
        self.c_label = QLabel("c:", self)
        self.c_label.setBuddy(self.c_edit)

        self.alpha_edit = QLineEdit(self)
        self.alpha_label = QLabel("alpha:", self)
        self.alpha_label.setBuddy(self.alpha_edit)

        self.beta_edit = QLineEdit(self)
        self.beta_label = QLabel("beta:", self)
        self.beta_label.setBuddy(self.beta_edit)

        self.gamma_edit = QLineEdit(self)
        self.gamma_label = QLabel("gamma:", self)
        self.gamma_label.setBuddy(self.gamma_edit)

        self.h_edit = QLineEdit(self)
        self.h_label = QLabel("h:", self)
        self.h_label.setBuddy(self.h_edit)

        self.k_edit = QLineEdit(self)
        self.k_label = QLabel("k:", self)
        self.k_label.setBuddy(self.k_edit)

        self.l_edit = QLineEdit(self)
        self.l_label = QLabel("l:", self)
        self.l_label.setBuddy(self.l_edit)

        lattice_layout.addWidget(self.a_label, 0, 0)
        lattice_layout.addWidget(self.a_edit, 0, 1)
        lattice_layout.addWidget(self.b_label, 0, 2)
        lattice_layout.addWidget(self.b_edit, 0, 3)
        lattice_layout.addWidget(self.c_label, 0, 4)
        lattice_layout.addWidget(self.c_edit, 0, 5)
        lattice_layout.addWidget(self.alpha_label, 1, 0)
        lattice_layout.addWidget(self.alpha_edit, 1, 1)
        lattice_layout.addWidget(self.beta_label, 1, 2)
        lattice_layout.addWidget(self.beta_edit, 1, 3)
        lattice_layout.addWidget(self.gamma_label, 1, 4)
        lattice_layout.addWidget(self.gamma_edit, 1, 5)
        lattice_layout.addWidget(self.h_label, 2, 0)
        lattice_layout.addWidget(self.h_edit, 2, 1)
        lattice_layout.addWidget(self.k_label, 2, 2)
        lattice_layout.addWidget(self.k_edit, 2, 3)
        lattice_layout.addWidget(self.l_label, 2, 4)
        lattice_layout.addWidget(self.l_edit, 2, 5)

        self.setLayout(lattice_layout)

    def set_values(self, values):
        self.a_edit.setText(str(values["a"]))
        self.b_edit.setText(str(values["b"]))
        self.c_edit.setText(str(values["c"]))
        self.alpha_edit.setText(str(values["alpha"]))
        self.beta_edit.setText(str(values["beta"]))
        self.gamma_edit.setText(str(values["gamma"]))
        self.h_edit.setText(str(values["h"]))
        self.k_edit.setText(str(values["k"]))
        self.l_edit.setText(str(values["l"]))


class ExperimentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.Ei_edit = QLineEdit(self)
        self.Ei_label = QLabel("&Ei:", self)
        self.Ei_label.setBuddy(self.Ei_edit)
        self.Ei_validator = QDoubleValidator(bottom=0, top=100, parent=self)
        self.Ei_validator.setNotation(QDoubleValidator.StandardNotation)
        self.Ei_edit.setValidator(self.Ei_validator)

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

        # connections
        self.Ei_edit.editingFinished.connect(self.validate_inputs)

    def initalizeCombo(self, options):
        self.Type_combobox.addItems(options)

    def validate_inputs(self, *dummy_args, **dummy_kwargs):
        """Check validity of the fields and set the stylesheet"""
        print(self.sender)


class CrosshairWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        DeltaE_edit = QLineEdit(self)
        DeltaE_label = QLabel("&DeltaE:", self)
        DeltaE_label.setBuddy(DeltaE_edit)

        self.modQ_edit = QLineEdit(self)
        self.modQ_label = QLabel("|&Q|:", self)
        self.modQ_label.setBuddy(self.modQ_edit)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(DeltaE_label)
        layout.addWidget(DeltaE_edit)

        layout.addWidget(self.modQ_label)
        layout.addWidget(self.modQ_edit)

    def set_Qmod_enabled(self, state):
        self.modQ_edit.setEnabled(state)
