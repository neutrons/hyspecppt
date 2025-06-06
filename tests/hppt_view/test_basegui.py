import hyspecppt.hppt.hppt_view as hppt_view
from hyspecppt.hppt.experiment_settings import PLOT_TYPES, alpha, beta, gamma


def test_Experiment_widget(qtbot):
    """Test the names of the Qlabel are correct and line edits can takes in values (assumes values are valid)"""
    ExpWidget = hppt_view.ExperimentWidget()
    qtbot.addWidget(ExpWidget)
    qtbot.keyClicks(ExpWidget.Ei_edit, "10")
    assert ExpWidget.Ei_label.text() == "Incident energy &Ei:"
    assert ExpWidget.Ei_edit.text() == "10"

    qtbot.keyClicks(ExpWidget.Pangle_edit, "45")
    assert ExpWidget.Pangle_label.text() == "&Polarization angle:"
    assert ExpWidget.Pangle_edit.text() == "45"

    qtbot.keyClicks(ExpWidget.S2_edit, "50")
    assert ExpWidget.S2_label.text() == "Detector angle &S2:"
    assert ExpWidget.S2_edit.text() == "50"

    assert ExpWidget.Type_label.text() == "&Type:"
    # check QCombobox has been correctly initialized. All items are added.
    ExpWidget.initializeCombo(PLOT_TYPES)
    for i in range(len(PLOT_TYPES)):
        assert ExpWidget.Type_combobox.findText(PLOT_TYPES[i]) == i


def test_SC_widget(qtbot):
    """Test the names of the Qlabel are correct and line edits can takes in values (assumes values are valid)"""
    SCWidget = hppt_view.SingleCrystalWidget()
    qtbot.addWidget(SCWidget)

    qtbot.keyClicks(SCWidget.a_edit, "5.0")
    assert SCWidget.a_label.text() == "&a:"
    assert SCWidget.a_edit.text() == "5.0"

    qtbot.keyClicks(SCWidget.b_edit, "5.0")
    assert SCWidget.b_label.text() == "b:"
    assert SCWidget.b_edit.text() == "5.0"

    qtbot.keyClicks(SCWidget.c_edit, "5.0")
    assert SCWidget.c_label.text() == "c:"
    assert SCWidget.c_edit.text() == "5.0"

    qtbot.keyClicks(SCWidget.alpha_edit, "90.0")
    assert SCWidget.alpha_label.text() == alpha + ":"
    assert SCWidget.alpha_edit.text() == "90.0"

    qtbot.keyClicks(SCWidget.beta_edit, "90.0")
    assert SCWidget.beta_label.text() == beta + ":"
    assert SCWidget.beta_edit.text() == "90.0"

    qtbot.keyClicks(SCWidget.gamma_edit, "90.0")
    assert SCWidget.gamma_label.text() == gamma + ":"
    assert SCWidget.gamma_edit.text() == "90.0"

    qtbot.keyClicks(SCWidget.h_edit, "2.5")
    assert SCWidget.h_label.text() == "H:"
    assert SCWidget.h_edit.text() == "2.5"

    qtbot.keyClicks(SCWidget.k_edit, "2.5")
    assert SCWidget.k_label.text() == "K:"
    assert SCWidget.k_edit.text() == "2.5"

    qtbot.keyClicks(SCWidget.l_edit, "2.5")
    assert SCWidget.l_label.text() == "L:"
    assert SCWidget.l_edit.text() == "2.5"


def test_crosshair_widget(qtbot):
    """Test the names of the Qlabel are correct and line edits can takes in values (assumes values are valid)"""
    crosshair_widget = hppt_view.CrosshairWidget()
    qtbot.addWidget(crosshair_widget)

    qtbot.keyClicks(crosshair_widget.DeltaE_edit, "20.0")
    assert crosshair_widget.DeltaE_label.text() == "&DeltaE:"
    assert crosshair_widget.DeltaE_edit.text() == "20.0"

    assert crosshair_widget.modQ_label.text() == "|&Q|:"


def test_selector_widget(qtbot):
    """Test the names of the Qlabel are correct and line edits can takes in values (assumes values are valid)"""
    selector_widget = hppt_view.SelectorWidget()
    qtbot.addWidget(selector_widget)

    assert selector_widget.powder_rb.text() == "Po&wder"
    assert selector_widget.sc_rb.text() == "Single C&rystal"


def test_combo_box_plot_options():
    """Test the combo box text are set correctly"""
    # unicode
    alpha = "\u03b1"
    square = "\u00b2"
    subscript_s = "\u209b"

    ExpWidget = hppt_view.ExperimentWidget()
    ExpWidget.initializeCombo(PLOT_TYPES)
    assert ExpWidget.Type_combobox.currentText() == alpha + subscript_s
    ExpWidget.Type_combobox.setCurrentIndex(1)
    assert ExpWidget.Type_combobox.currentText() == "cos" + square + alpha + subscript_s

    ExpWidget.Type_combobox.setCurrentIndex(2)
    assert ExpWidget.Type_combobox.currentText() == "(1+cos" + square + alpha + subscript_s + ")/2"

    ExpWidget.Type_combobox.setCurrentIndex(3)
    assert (
        ExpWidget.Type_combobox.currentText()
        == "cos" + square + alpha + subscript_s + "-sin" + square + alpha + subscript_s
    )


def test_crosshair_widget_Q_beam_ang():
    """Test the names of the Qlabel and line edits are correct"""
    crosshair_widget = hppt_view.CrosshairWidget()

    assert crosshair_widget.QZ_angle_label.text() == "Q-Beam Angle:"
    assert crosshair_widget.QZ_angle_edit.text() == ""
    assert not crosshair_widget.QZ_angle_edit.isEnabled()
