"""Widgets for the main window"""

from typing import Optional

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from qtpy.QtCore import QObject
from qtpy.QtGui import QDoubleValidator
from qtpy.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from .experiment_settings import alpha, beta, gamma


class HyspecPPTView(QWidget):
    """Main widget"""

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the main widget

        Args:
            parent (QObject): Optional parent

        """
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

    def switch_to_SC(self) -> None:
        """Set visibility for Single Crystal mode"""
        self.SCW.setVisible(True)
        self.CW.set_Qmod_enabled(False)

    def switch_to_Powder(self) -> None:
        """Set visibility for Powder mode"""
        self.SCW.setVisible(False)
        self.CW.set_Qmod_enabled(True)


class PrintWidget(QWidget):
    """Widget that displays the plot"""

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the plotting widget

        Args:
            parent (QObject): Optional parent

        """
        super().__init__(parent)
        layoutRight = QVBoxLayout()
        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layoutRight.addWidget(self.static_canvas)
        layoutRight.addWidget(NavigationToolbar(self.static_canvas, self))
        self.setLayout(layoutRight)


class SelectorWidget(QWidget):
    """Widget that selects Powder/Single Crystal mode"""

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the selector widget

        Args:
            parent (QObject): Optional parent

        """
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

    def set_SC_toggle(self, toggle: bool) -> None:
        """Sets widget display based on the values dictionary

        Args:
            Bool
        """
        self.sc_rb.setChecked(toggle)

class SingleCrystalWidget(QWidget):
    """Widget for inputting single crystal parameters"""

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the single crystal input parameters widget

        Args:
            parent (QObject): Optional parent

        """
        super().__init__(parent)

        layout = QVBoxLayout()
        groupBox = QGroupBox("Lattice parameters")
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
        self.alpha_label = QLabel(alpha + ":", self)
        self.alpha_label.setBuddy(self.alpha_edit)

        self.beta_edit = QLineEdit(self)
        self.beta_label = QLabel(beta + ":", self)
        self.beta_label.setBuddy(self.beta_edit)

        self.gamma_edit = QLineEdit(self)
        self.gamma_label = QLabel(gamma + ":", self)
        self.gamma_label.setBuddy(self.gamma_edit)

        self.h_edit = QLineEdit(self)
        self.h_label = QLabel("H:", self)
        self.h_label.setBuddy(self.h_edit)

        self.k_edit = QLineEdit(self)
        self.k_label = QLabel("K:", self)
        self.k_label.setBuddy(self.k_edit)

        self.l_edit = QLineEdit(self)
        self.l_label = QLabel("L:", self)
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

        groupBox.setLayout(lattice_layout)
        layout.addWidget(groupBox)
        self.setLayout(layout)

    def set_values(self, values: dict[str, float]) -> None:
        """Sets widget display based on the values dictionary

        Args:
            values (dict): a dictionary that contains
            a, b, c, alpha, beta, gamma lattice parameters
            and h, k, l reciprocal lattice coordinates

        """
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
    """Widget for setting experiment parameters"""

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the experiment input parameters widget

        Args:
            parent (QObject): Optional parent

        """
        super().__init__(parent)

        self.Ei_edit = QLineEdit(self)
        self.Ei_label = QLabel("Incident energy &Ei:", self)
        self.Ei_label.setBuddy(self.Ei_edit)
        self.Ei_validator = QDoubleValidator(bottom=0, top=100, parent=self)
        self.Ei_validator.setNotation(QDoubleValidator.StandardNotation)
        self.Ei_edit.setValidator(self.Ei_validator)

        self.Pangle_edit = QLineEdit(self)
        self.Pangle_label = QLabel("&Polarization angle:", self)
        self.Pangle_label.setBuddy(self.Pangle_edit)

        self.S2_edit = QLineEdit(self)
        self.S2_label = QLabel("Detector angle &S2:", self)
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

    def initializeCombo(self, options: list[str]) -> None:
        """Initialize the plot types in the combo box

        Args:
            options (list): list of strings describing what the user can show
                            in the plot

        """
        self.Type_combobox.addItems(options)

    def validate_inputs(self, *dummy_args, **dummy_kwargs) -> None:
        """Check validity of the fields and set the stylesheet"""
        print(self.sender)
        print("args: ", dummy_args, " kwargs: ", dummy_kwargs)

    def set_values(self, values: dict[str, float]) -> None:
        """Sets widget display based on the values dictionary

        Args:
            values (dict): a dictionary that contains
            Ei, S2, alpha_p, plot_types values

        """
        self.Ei_edit.setText(str(values["Ei"]))
        self.S2_edit.setText(str(values["s2"]))
        self.Pangle_edit.setText(str(values["alpha_p"]))
        # self.Type_combobox.setItemText(0,str(values["plot_type"]))


class CrosshairWidget(QWidget):
    """Widget to enter/display crosshair parameters"""

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the crosshair input parameters widget

        Args:
            parent (QObject): Optional parent

        """
        super().__init__(parent)

        layout = QVBoxLayout()
        self.DeltaE_edit = QLineEdit(self)
        self.DeltaE_label = QLabel("&DeltaE:", self)
        self.DeltaE_label.setBuddy(self.DeltaE_edit)

        self.modQ_edit = QLineEdit(self)
        self.modQ_label = QLabel("|&Q|:", self)
        self.modQ_label.setBuddy(self.modQ_edit)

        box_layout = QHBoxLayout()
        box_layout.addWidget(self.DeltaE_label)
        box_layout.addWidget(self.DeltaE_edit)

        box_layout.addWidget(self.modQ_label)
        box_layout.addWidget(self.modQ_edit)

        groupBox = QGroupBox("Crosshair position")
        groupBox.setLayout(box_layout)
        layout.addWidget(groupBox)
        self.setLayout(layout)

    def set_Qmod_enabled(self, state: bool) -> None:
        """Enable/disable the modQ line edit

        Args:
            state (bool): enable editing modQ (True) or disable it(False)

        """
        self.modQ_edit.setEnabled(state)

    def set_values(self, values: dict[str, float]) -> None:
        """Sets widget display based on the values dictionary

        Args:
            values (dict): a dictionary that contains
            deltaE and mod_Q values

        """
        self.DeltaE_edit.setText(str(values["DeltaE"]))
        self.modQ_edit.setText(str(values["modQ"]))
