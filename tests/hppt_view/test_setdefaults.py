import hyspecppt.hppt.hppt_view as hppt_view
from hyspecppt.hppt.experiment_settings import DEFAULT_CROSSHAIR, DEFAULT_EXPERIMENT, DEFAULT_LATTICE, PLOT_TYPES


def test_set_Experimentwidget_Default_Values(qtbot):
    """Test the default values of SC widget are set correctly"""
    ExpWidget = hppt_view.ExperimentWidget()
    ExpWidget.set_values(DEFAULT_EXPERIMENT)
    qtbot.addWidget(ExpWidget)
    assert ExpWidget.Ei_edit.text() == "20"
    assert ExpWidget.S2_edit.text() == "30"
    assert ExpWidget.Pangle_edit.text() == "0"
    # check QCombobox has been correctly initialized. All items are added.
    # check QCombobox has been correctly initialized. All items are added.
    ExpWidget.initializeCombo(PLOT_TYPES)
    for i in range(len(PLOT_TYPES)):
        assert ExpWidget.Type_combobox.findText(PLOT_TYPES[i]) == i


def test_set_SC_Default_Values(qtbot):
    """Test the default SC values are set correctly"""
    SCWidget = hppt_view.SingleCrystalWidget()
    SCWidget.set_values(DEFAULT_LATTICE)
    qtbot.addWidget(SCWidget)
    assert SCWidget.a_edit.text() == "1"
    assert SCWidget.b_edit.text() == "1"
    assert SCWidget.c_edit.text() == "1"

    assert SCWidget.alpha_edit.text() == "90"
    assert SCWidget.beta_edit.text() == "90"
    assert SCWidget.gamma_edit.text() == "90"

    assert SCWidget.h_edit.text() == "0"
    assert SCWidget.k_edit.text() == "0"
    assert SCWidget.l_edit.text() == "0"


def test_set_Crosshair_widget_Default_Values(qtbot):
    """Test the default crosshair values are set correctly"""
    CHWidget = hppt_view.CrosshairWidget()
    CHWidget.set_values(DEFAULT_CROSSHAIR)
    qtbot.addWidget(CHWidget)

    assert CHWidget.DeltaE_edit.text() == "0"

    assert CHWidget.modQ_edit.text() == "0"


def test_set_Selector_widget_Default_Values(qtbot):
    """Test the default SC mode is toggled"""
    SelWidget = hppt_view.SelectorWidget()
    qtbot.addWidget(SelWidget)
    label = "Single C&rystal"
    SelWidget.selector_init(label)

    assert SelWidget.sc_rb.isChecked()
    assert not SelWidget.powder_rb.isChecked()
