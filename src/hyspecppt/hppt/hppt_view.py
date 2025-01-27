"""Widgets for the main window"""

from typing import Optional, Union

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from qtpy.QtCore import QObject, Signal
from qtpy.QtGui import QDoubleValidator, QValidator
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

from .experiment_settings import INVALID_QLINEEDIT, MAX_MODQ, PLOT_TYPES, alpha, beta, gamma
from .hppt_view_validators import AbsValidator, AngleValidator


class HyspecPPTView(QWidget):
    """Main widget"""

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the main widget

        Args:
            parent (QObject): Optional parent

        """
        super().__init__(parent)

        # callback functions defined by the presenter
        self.fields_callback = None
        self.powder_mode_switch_callback = None
        self.sc_mode_switch_callback = None

        # callback functions defined by the presenter
        self.fields_callback = None
        self.powder_mode_switch_callback = None
        self.sc_mode_switch_callback = None

        layout = QHBoxLayout()
        self.setLayout(layout)
        left_side_layout = QVBoxLayout()
        layout.addLayout(left_side_layout)
        self.experiment_widget = ExperimentWidget(self)
        left_side_layout.addWidget(self.experiment_widget)
        self.sc_widget = SingleCrystalWidget(self)
        self.crosshair_widget = CrosshairWidget(self)
        self.selection_widget = SelectorWidget(self)
        left_side_layout.addWidget(self.selection_widget)
        left_side_layout.addWidget(self.sc_widget)
        left_side_layout.addWidget(self.crosshair_widget)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        left_side_layout.addItem(spacer)
        self.plot_widget = PlotWidget(self)
        layout.addWidget(self.plot_widget)

        # signal handling for every valid field update
        self.experiment_widget.valid_signal.connect(self.values_update)
        self.sc_widget.valid_signal.connect(self.values_update)
        self.crosshair_widget.valid_signal.connect(self.values_update)
        # plot update
        self.crosshair_widget.valid_signal.connect(self.plot_widget.update_plot_crosshair)

    def connect_fields_update(self, callback):
        """Callback for the fields update - set by the presenter"""
        self.fields_callback = callback

    def connect_powder_mode_switch(self, callback):
        """Callback function setup for the switching to Powder mode from the radio button
        - function defined and set by the presenter
        """
        self.powder_mode_switch_callback = callback

    def connect_sc_mode_switch(self, callback):
        """Callback function setup for the switching to Single Crystal mode from the radio button
        - function defined and set by the presenter
        """
        self.sc_mode_switch_callback = callback

    def values_update(self, values):
        """Fields update"""
        self.fields_callback(values)

    def switch_to_sc(self) -> None:
        """Switch to Single Crystal mode"""
        if self.sc_mode_switch_callback:
            self.sc_mode_switch_callback()

    def switch_to_powder(self) -> None:
        """Switch to Powder mode"""
        if self.powder_mode_switch_callback:
            self.powder_mode_switch_callback()

    def field_visibility_in_SC(self) -> None:
        """Set visibility for Single Crystal mode"""
        self.sc_widget.setVisible(True)
        self.crosshair_widget.set_Qmod_enabled(False)

    def field_visibility_in_Powder(self) -> None:
        """Set visibility for Powder mode"""
        self.sc_widget.setVisible(False)
        self.crosshair_widget.set_Qmod_enabled(True)


class PlotWidget(QWidget):
    """Widget that displays the plot"""

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the plotting widget

        Args:
            parent (QObject): Optional parent

        """
        super().__init__(parent)
        layoutRight = QVBoxLayout()

        self.figure = Figure(figsize=(6, 4.5))
        self.static_canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.static_canvas, self)

        layoutRight.addWidget(self.static_canvas)
        layoutRight.addWidget(self.toolbar)
        self.setLayout(layoutRight)

        # heatmap initialization
        self.ax = self.static_canvas.figure.subplots()
        self.heatmap = self.ax.pcolormesh([[0, 0]], [[0, 0]], [[0, 0]])
        self.qmin_line = self.ax.plot([0, 0], [0, 0])[0]
        self.qmax_line = self.ax.plot([0, 0], [0, 0])[0]
        self.cb = self.figure.colorbar(self.heatmap, ax=self.ax, pad=0.0)

        # crosshair initialization
        self.eline_data = 0
        self.qline_data = 0
        self.eline = self.ax.axhline(y=self.eline_data)
        self.qline = self.ax.axvline(x=self.qline_data)

        # draw the plot
        self.static_canvas.draw()

    def update_plot_crosshair(self, crosshair_data: dict) -> None:
        """Update the plot with valid crosshair_data
        Args:
            eline (float): x
            qline (float): y

        """
        self.update_crosshair(crosshair_data["data"]["DeltaE"], crosshair_data["data"]["modQ"])

    def update_crosshair(self, eline: float, qline: float) -> None:
        """Update the plot with crosshair lines
        Args:
            eline (float): x
            qline (float): y

        """
        self.eline_data = eline
        self.qline_data = qline
        self.eline.set_data([0, 1], [self.eline_data, self.eline_data])
        self.qline.set_data([self.qline_data, self.qline_data], [0, 1])

        self.set_axes_meta_and_draw_plot()

    def update_plot(
        self,
        q_min: list[float],
        q_max: list[float],
        energy_transfer: list[float],
        q2d: list[list[float]],
        e2d: list[list[float]],
        scharpf_angle: list[list[float]],
        plot_label: str,
    ):
        """Update the colormesh, colorbar and redraw the crosshair

        Args:
            q_min: list of float numbers,
            q_max: list of float numbers,
            energy_transfer: list of float numbers,
            q2d: list of lists of float numbers,
            e2d: list of lists of float numbers,
            scharpf_angle: list of lists of float numbers,
            plot_label: used for colormap label,

        """
        # clear
        self.cb.remove()
        self.ax.clear()

        # update heatmap
        self.heatmap = self.ax.pcolormesh(q2d, e2d, scharpf_angle)
        self.ax.plot(q_min, energy_transfer)
        self.ax.plot(q_max, energy_transfer)

        # Add colorbar
        self.cb = self.figure.colorbar(self.heatmap, ax=self.ax, pad=0.0)
        self.cb.set_label(plot_label)

        # redraw crosshair
        self.eline = self.ax.axhline(y=self.eline_data)
        self.qline = self.ax.axvline(x=self.qline_data)

        self.set_axes_meta_and_draw_plot()

    def set_axes_meta_and_draw_plot(self):
        """Set labels, color and draw static canvas
        Args:
        """
        self.ax.set_ylabel(r"$\Delta E$")
        self.ax.set_xlabel("$|Q|$")
        self.ax.relim()
        self.ax.autoscale()
        # set the croshair color
        self.qline.set_color("darkred")
        self.eline.set_color("darkred")

        self.static_canvas.draw()


class SelectorWidget(QWidget):
    """Widget that selects Powder/Single Crystal mode"""

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the selector widget

        Args:
            parent (QObject): Optional parent

        """
        super().__init__(parent)
        selector_layout = QHBoxLayout()

        self.powder_label = "Po&wder"
        self.sc_label = "Single C&rystal"
        self.powder_rb = QRadioButton(self.powder_label)
        self.sc_rb = QRadioButton(self.sc_label)
        tooltip = "Selection of cursor momentum transfer calculation:" +\
            "\n   - for Powder user enters |Q| directly" +\
            "\n   - for Single Crystal user enters |Q| vial lattice parameters and H, K, L values"
        self.powder_rb.setToolTip(tooltip)
        self.sc_rb.setToolTip(tooltip)

        selector_group = QButtonGroup(self)
        selector_group.addButton(self.powder_rb)
        selector_group.addButton(self.sc_rb)

        selector_layout.addWidget(self.powder_rb)
        selector_layout.addWidget(self.sc_rb)
        self.setLayout(selector_layout)

        if parent:
            self.powder_rb.toggled.connect(self.sc_toggle)
            self.sc_rb.toggled.connect(self.sc_toggle)

    def selector_init(self, selected_label: str):
        """Initialize the default selected mode
        Args:
            selected_label: it contains either sc_label or powder_label
            based on the selected label the mode is set during initialization
        """
        if selected_label == self.sc_label:
            self.sc_rb.setChecked(True)
        else:
            self.powder_rb.setChecked(True)

    def sc_toggle(self) -> None:
        """Update fields based on selected mode
        Args:
        """
        if self.parent():
            sender = self.sender().text()

            if sender == self.powder_label and self.powder_rb.isChecked():
                self.parent().switch_to_powder()
            if sender == self.sc_label and self.sc_rb.isChecked():
                self.parent().switch_to_sc()

    def get_selected_mode_label(self) -> str:
        """Return the label of the selected mode
        Args:
        """
        if self.powder_rb.isChecked():
            return self.powder_label
        else:
            return self.sc_label


class SingleCrystalWidget(QWidget):
    """Widget for inputting single crystal parameters"""

    valid_signal = Signal(dict)

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the single crystal input parameters widget

        Args:
            parent (QObject): Optional parent

        """
        super().__init__(parent)

        layout = QVBoxLayout()
        groupBox = QGroupBox("Lattice parameters")
        lattice_layout = QGridLayout()

        self.lattice_length_validator = QDoubleValidator(bottom=1, top=100, parent=self)
        self.lattice_length_validator.setNotation(QDoubleValidator.StandardNotation)

        self.lattice_angle_validator = QDoubleValidator(bottom=30, top=150, parent=self)
        self.lattice_angle_validator.setNotation(QDoubleValidator.StandardNotation)

        self.rlu_validator = QDoubleValidator(bottom=-100, top=100, parent=self)
        self.rlu_validator.setNotation(QDoubleValidator.StandardNotation)

        # tooltips
        tooltip_lattice_length = "Lattice parameter {} in Angstroms, a number between 1 and 100." +\
            "\nSee help for validation rules."
        tooltip_lattice_angle = "Lattice angle {} in degrees, a number between 30 and 150." +\
            "\nSee help for validation rules."
        tooltip_hkl = "Single crystal {} coordinate in r.l.u., a number between -100 and 100" +\
            "\nSee help for validation rules."

        self.a_edit = QLineEdit(self)
        self.a_label = QLabel("&a:", self)
        self.a_label.setBuddy(self.a_edit)
        self.a_edit.setToolTip(tooltip_lattice_length.format("a"))
        self.a_label.setToolTip(tooltip_lattice_length.format("a"))
        self.a_edit.setValidator(self.lattice_length_validator)

        self.b_edit = QLineEdit(self)
        self.b_label = QLabel("b:", self)
        self.b_label.setBuddy(self.b_edit)
        self.b_edit.setToolTip(tooltip_lattice_length.format("b"))
        self.b_label.setToolTip(tooltip_lattice_length.format("b"))
        self.b_edit.setValidator(self.lattice_length_validator)

        self.c_edit = QLineEdit(self)
        self.c_label = QLabel("c:", self)
        self.c_label.setBuddy(self.c_edit)
        self.c_edit.setToolTip(tooltip_lattice_length.format("c"))
        self.c_label.setToolTip(tooltip_lattice_length.format("c"))
        self.c_edit.setValidator(self.lattice_length_validator)

        self.alpha_edit = QLineEdit(self)
        self.alpha_label = QLabel(alpha + ":", self)
        self.alpha_label.setBuddy(self.alpha_edit)
        self.alpha_edit.setToolTip(tooltip_lattice_angle.format(alpha))
        self.alpha_label.setToolTip(tooltip_lattice_angle.format(alpha))
        self.alpha_edit.setObjectName("alpha")

        self.beta_edit = QLineEdit(self)
        self.beta_label = QLabel(beta + ":", self)
        self.beta_label.setBuddy(self.beta_edit)
        self.beta_edit.setToolTip(tooltip_lattice_angle.format(beta))
        self.beta_label.setToolTip(tooltip_lattice_angle.format(beta))
        self.beta_edit.setObjectName("beta")

        self.gamma_edit = QLineEdit(self)
        self.gamma_label = QLabel(gamma + ":", self)
        self.gamma_label.setBuddy(self.gamma_edit)
        self.gamma_edit.setToolTip(tooltip_lattice_angle.format(gamma))
        self.gamma_label.setToolTip(tooltip_lattice_angle.format(gamma))
        self.gamma_edit.setObjectName("gamma")

        self.h_edit = QLineEdit(self)
        self.h_label = QLabel("H:", self)
        self.h_label.setBuddy(self.h_edit)
        self.h_edit.setToolTip(tooltip_hkl.format("H"))
        self.h_label.setToolTip(tooltip_hkl.format("H"))
        self.h_edit.setValidator(self.rlu_validator)

        self.k_edit = QLineEdit(self)
        self.k_label = QLabel("K:", self)
        self.k_label.setBuddy(self.k_edit)
        self.k_edit.setToolTip(tooltip_hkl.format("K"))
        self.k_label.setToolTip(tooltip_hkl.format("K"))
        self.k_edit.setValidator(self.rlu_validator)

        self.l_edit = QLineEdit(self)
        self.l_label = QLabel("L:", self)
        self.l_label.setBuddy(self.l_edit)
        self.l_edit.setToolTip(tooltip_hkl.format("L"))
        self.l_label.setToolTip(tooltip_hkl.format("L"))
        self.l_edit.setValidator(self.rlu_validator)

        # cumulative angle validator
        # including the validation of each individual field
        self.angle_validator = AngleValidator(
            parent=self,
            alpha=self.alpha_edit,
            beta=self.beta_edit,
            gamma=self.gamma_edit,
            individual=self.lattice_angle_validator,
        )
        self.alpha_edit.setValidator(self.angle_validator)
        self.beta_edit.setValidator(self.angle_validator)
        self.gamma_edit.setValidator(self.angle_validator)

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

        # connections
        self.a_edit.editingFinished.connect(self.validate_all_inputs)
        self.a_edit.textChanged.connect(self.validate_inputs)
        self.b_edit.editingFinished.connect(self.validate_all_inputs)
        self.b_edit.textChanged.connect(self.validate_inputs)
        self.c_edit.editingFinished.connect(self.validate_all_inputs)
        self.c_edit.textChanged.connect(self.validate_inputs)
        self.alpha_edit.editingFinished.connect(self.validate_all_inputs)
        self.alpha_edit.textChanged.connect(self.validate_inputs)
        self.beta_edit.editingFinished.connect(self.validate_all_inputs)
        self.beta_edit.textChanged.connect(self.validate_inputs)
        self.gamma_edit.editingFinished.connect(self.validate_all_inputs)
        self.gamma_edit.textChanged.connect(self.validate_inputs)
        self.h_edit.editingFinished.connect(self.validate_all_inputs)
        self.h_edit.textChanged.connect(self.validate_inputs)
        self.k_edit.editingFinished.connect(self.validate_all_inputs)
        self.k_edit.textChanged.connect(self.validate_inputs)
        self.l_edit.editingFinished.connect(self.validate_all_inputs)
        self.l_edit.textChanged.connect(self.validate_inputs)

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

    def validate_inputs(self, *_, **__) -> None:
        """Check validity of the fields and set the stylesheet"""
        if not self.sender().hasAcceptableInput():
            self.sender().setStyleSheet(INVALID_QLINEEDIT)
        else:
            self.sender().setStyleSheet("")
        # cumulative validation style for angles
        if self.sender().objectName() in ["alpha", "beta", "gamma"]:
            self.validate_angles()

    def validate_angles(self) -> None:
        """Check validity of the angles and set the stylesheet"""
        fields = [
            self.alpha_edit,
            self.beta_edit,
            self.gamma_edit,
        ]
        for field in fields:
            state = field.validator().validate(field.text(), 0)[0]
            if state != QValidator.Acceptable:
                field.setStyleSheet(INVALID_QLINEEDIT)
            else:
                field.setStyleSheet("")

    def validate_all_inputs(self):
        inputs = [
            self.a_edit,
            self.b_edit,
            self.c_edit,
            self.alpha_edit,
            self.beta_edit,
            self.gamma_edit,
            self.h_edit,
            self.k_edit,
            self.l_edit,
        ]
        keys = ["a", "b", "c", "alpha", "beta", "gamma", "h", "k", "l"]
        out_signal = dict(name="sc_lattice", data=dict())

        for k, edit in zip(keys, inputs):
            if edit.hasAcceptableInput():
                out_signal["data"][k] = float(edit.text())

        if len(out_signal["data"]) == 9:
            self.valid_signal.emit(out_signal)


class ExperimentWidget(QWidget):
    """Widget for setting experiment parameters"""

    valid_signal = Signal(dict)

    def __init__(self, parent: Optional["QObject"] = None) -> None:
        """Constructor for the experiment input parameters widget

        Args:
            parent (QObject): Optional parent

        """
        super().__init__(parent)

        self.Ei_edit = QLineEdit(self)
        self.Ei_label = QLabel("Incident energy &Ei:", self)
        self.Ei_label.setBuddy(self.Ei_edit)
        tooltip_Ei = "Incident energy in meV, a number between 0 and 100."
        self.Ei_edit.setToolTip(tooltip_Ei)
        self.Ei_label.setToolTip(tooltip_Ei)
        self.Ei_validator = QDoubleValidator(bottom=0, top=100, parent=self)
        self.Ei_validator.setNotation(QDoubleValidator.StandardNotation)
        self.Ei_edit.setValidator(self.Ei_validator)

        self.Pangle_edit = QLineEdit(self)
        self.Pangle_label = QLabel("&Polarization angle:", self)
        self.Pangle_label.setBuddy(self.Pangle_edit)
        tooltip_P_angle = "Polarization angle with respect to incident beam, in degrees, a number between -180 and 180."
        self.Pangle_edit.setToolTip(tooltip_P_angle)
        self.Pangle_label.setToolTip(tooltip_P_angle)
        self.Pangle_validator = QDoubleValidator(bottom=-180, top=180, parent=self)
        self.Pangle_validator.setNotation(QDoubleValidator.StandardNotation)
        self.Pangle_edit.setValidator(self.Pangle_validator)

        self.S2_edit = QLineEdit(self)
        self.S2_label = QLabel("Detector angle &S2:", self)
        self.S2_label.setBuddy(self.S2_edit)
        tooltip_S2 = "Detector tank angle in degrees, a number between -100 and 100," +\
            "\nbut not between -30 and 30. The detector coverage is +/- 30 degrees"
        self.S2_edit.setToolTip(tooltip_S2)
        self.S2_label.setToolTip(tooltip_S2)
        self.S2_validator = AbsValidator(bottom=30, top=100, parent=self)
        self.S2_validator.setNotation(QDoubleValidator.StandardNotation)
        self.S2_edit.setValidator(self.S2_validator)

        self.Type_combobox = QComboBox(self)
        self.Type_label = QLabel("&Type:", self)
        self.Type_label.setBuddy(self.Type_combobox)
        tooltip_type = "Quantity to plot. " + PLOT_TYPES[0] + " is the angle between" +\
            "momentum transfer vector Q and the polarization direction."
        self.Type_combobox.setToolTip(tooltip_type)
        self.Type_label.setToolTip(tooltip_type)

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
        self.Ei_edit.editingFinished.connect(self.validate_all_inputs)
        self.Ei_edit.textChanged.connect(self.validate_inputs)
        self.S2_edit.editingFinished.connect(self.validate_all_inputs)
        self.S2_edit.textChanged.connect(self.validate_inputs)
        self.Pangle_edit.editingFinished.connect(self.validate_all_inputs)
        self.Pangle_edit.textChanged.connect(self.validate_inputs)
        self.Type_combobox.currentIndexChanged.connect(self.validate_all_inputs)

    def initializeCombo(self, options: list[str]) -> None:
        """Initialize the plot types in the combo box

        Args:
            options (list): list of strings describing what the user can show
                            in the plot

        """
        self.Type_combobox.addItems(options)

    def validate_inputs(self, *_, **__) -> None:
        """Check validity of the fields and set the stylesheet"""
        if not self.sender().hasAcceptableInput():
            self.sender().setStyleSheet(INVALID_QLINEEDIT)
        else:
            self.sender().setStyleSheet("")

    def validate_all_inputs(self) -> None:
        """If all inputs are valid emit a valid_signal"""
        inputs = [self.Ei_edit, self.S2_edit, self.Pangle_edit]
        keys = ["Ei", "S2", "alpha_p"]

        out_signal = dict(name="experiment", data=dict())
        out_signal["data"] = dict(plot_type=self.Type_combobox.currentText())
        for k, edit in zip(keys, inputs):
            if edit.hasAcceptableInput():
                out_signal["data"][k] = float(edit.text())
        if len(out_signal["data"]) == 4:
            self.valid_signal.emit(out_signal)

    def set_values(self, values: dict[str, Union[float, str]]) -> None:
        """Sets widget display based on the values dictionary

        Args:
            values (dict): a dictionary that contains
            Ei, S2, alpha_p, plot_types values

        """
        self.Ei_edit.setText(str(values["Ei"]))
        self.S2_edit.setText(str(values["S2"]))
        self.Pangle_edit.setText(str(values["alpha_p"]))
        self.Type_combobox.setCurrentIndex(PLOT_TYPES.index(values["plot_type"]))


class CrosshairWidget(QWidget):
    """Widget to enter/display crosshair parameters"""

    valid_signal = Signal(dict)

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
        tooltip_DeltaE = "Energy transfer in meV"
        self.DeltaE_edit.setToolTip(tooltip_DeltaE)
        self.DeltaE_label.setToolTip(tooltip_DeltaE)

        self.modQ_edit = QLineEdit(self)
        self.modQ_label = QLabel("|&Q|:", self)
        self.modQ_label.setBuddy(self.modQ_edit)
        tooltip_modQ = "Magnitude of momentum transfer in inverse Angstroms, " +\
            f"\na number between 0 and {MAX_MODQ}. Users can enter it directly in powder mode," +\
            "or calculate it based on lattice parameters and H, K, L for single crystal experiments."
        self.modQ_edit.setToolTip(tooltip_modQ)
        self.modQ_label.setToolTip(tooltip_modQ)

        box_layout = QHBoxLayout()
        box_layout.addWidget(self.DeltaE_label)
        box_layout.addWidget(self.DeltaE_edit)

        box_layout.addWidget(self.modQ_label)
        box_layout.addWidget(self.modQ_edit)

        self.DeltaE_validator = QDoubleValidator(parent=self)
        self.DeltaE_validator.setNotation(QDoubleValidator.StandardNotation)
        self.DeltaE_edit.setValidator(self.DeltaE_validator)
        self.modQ_validator = QDoubleValidator(bottom=0, top=MAX_MODQ, parent=self)
        self.modQ_validator.setNotation(QDoubleValidator.StandardNotation)
        self.modQ_edit.setValidator(self.modQ_validator)

        # connections
        self.DeltaE_edit.editingFinished.connect(self.validate_all_inputs)
        self.DeltaE_edit.textChanged.connect(self.validate_inputs)
        self.modQ_edit.editingFinished.connect(self.validate_all_inputs)
        self.modQ_edit.textChanged.connect(self.validate_inputs)

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
        self.modQ_edit.setText("{:.3f}".format(values["modQ"]))

    def validate_inputs(self, *_, **__) -> None:
        """Check validity of the fields and set the stylesheet"""
        if not self.sender().hasAcceptableInput():
            self.sender().setStyleSheet(INVALID_QLINEEDIT)
        else:
            self.sender().setStyleSheet("")

    def validation_status_all_inputs(self) -> bool:
        """Return validation status of all inpus, if all are valid returns True, else False"""
        inputs = [self.DeltaE_edit, self.modQ_edit]
        for edit in inputs:
            if not edit.hasAcceptableInput():
                return False
        return True

    def validate_all_inputs(self):
        """If all inputs are valid emit a valid_signal"""
        inputs = [self.DeltaE_edit, self.modQ_edit]
        keys = ["DeltaE", "modQ"]

        out_signal = dict(name="crosshair", data=dict())
        for k, edit in zip(keys, inputs):
            if edit.hasAcceptableInput():
                out_signal["data"][k] = float(edit.text())
        if len(out_signal["data"]) == 2:
            self.valid_signal.emit(out_signal)
