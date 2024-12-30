import hyspecppt.hppt.hppt_view as hppt_view
from hyspecppt.hppt.experiment_settings import INVALID_QLINEEDIT, PLOT_TYPES
from unittest.mock import MagicMock


def test_Experiment_validators(qtbot):
    """Test validators for the experiment widget"""
    ExpWidget = hppt_view.ExperimentWidget()
    qtbot.addWidget(ExpWidget)

    ExpWidget.initializeCombo(PLOT_TYPES)

    qtbot.keyClicks(ExpWidget.Ei_edit, "3034")
    assert ExpWidget.Ei_edit.text() == "303"
    assert ExpWidget.Ei_edit.styleSheet() == INVALID_QLINEEDIT
    qtbot.keyClicks(ExpWidget.Ei_edit, "\b")
    assert ExpWidget.Ei_edit.text() == "30"
    assert ExpWidget.Ei_edit.styleSheet() == ""

    qtbot.keyClicks(ExpWidget.Pangle_edit, "-450")
    assert ExpWidget.Pangle_edit.text() == "-450"
    assert ExpWidget.Pangle_edit.styleSheet() == INVALID_QLINEEDIT
    qtbot.keyClicks(ExpWidget.Pangle_edit, "\b")
    assert ExpWidget.Pangle_edit.text() == "-45"
    assert ExpWidget.Pangle_edit.styleSheet() == ""

    qtbot.keyClicks(ExpWidget.S2_edit, "-450")
    assert ExpWidget.S2_edit.text() == "-450"
    assert ExpWidget.S2_edit.styleSheet() == INVALID_QLINEEDIT
    qtbot.keyClicks(ExpWidget.S2_edit, "\b")
    assert ExpWidget.S2_edit.text() == "-45"
    assert ExpWidget.S2_edit.styleSheet() == ""
    qtbot.keyClicks(ExpWidget.S2_edit, "\b")
    assert ExpWidget.S2_edit.text() == "-4"
    assert ExpWidget.S2_edit.styleSheet() == INVALID_QLINEEDIT

    #validate_all_inputs
    mock_slot = MagicMock()
    ExpWidget.validSignal.connect(mock_slot)
    #invalid S2
    ExpWidget.S2_edit.editingFinished.emit()
    mock_slot.assert_not_called()
    #all valid
    qtbot.keyClicks(ExpWidget.S2_edit, "0")
    ExpWidget.S2_edit.editingFinished.emit()
    mock_slot.assert_called_once_with({'Ei': 30.0, 'S2': -40.0, 'alpha_p': -45.0, 'plot_type': PLOT_TYPES[0]})


def test_Single_Crystal_validators(qtbot):
    """Test validators for the single crystal widget"""
    SCWidget = hppt_view.SingleCrystalWidget()
    qtbot.addWidget(SCWidget)

    lattice = [SCWidget.a_edit, SCWidget.b_edit, SCWidget.c_edit]
    for latt_edit in lattice:
        qtbot.keyClicks(latt_edit, "450")
        assert latt_edit.text() == "450"
        assert latt_edit.styleSheet() == INVALID_QLINEEDIT
        qtbot.keyClicks(latt_edit, "\b")
        assert latt_edit.text() == "45"
        assert latt_edit.styleSheet() == ""

    angle = [SCWidget.alpha_edit, SCWidget.beta_edit, SCWidget.gamma_edit]
    for ang_edit in angle:
        qtbot.keyClicks(ang_edit, "450")
        assert ang_edit.text() == "450"
        assert ang_edit.styleSheet() == INVALID_QLINEEDIT
        qtbot.keyClicks(ang_edit, "\b")
        assert ang_edit.text() == "45"
        assert ang_edit.styleSheet() == ""

    hkls = [SCWidget.h_edit, SCWidget.k_edit, SCWidget.l_edit]
    for hkl_edit in hkls:
        qtbot.keyClicks(hkl_edit, "-450")
        assert hkl_edit.text() == "-450"
        assert hkl_edit.styleSheet() == INVALID_QLINEEDIT
        qtbot.keyClicks(hkl_edit, "\b")
        assert hkl_edit.text() == "-45"
        assert hkl_edit.styleSheet() == ""

    #validate_all_inputs
    mock_slot = MagicMock()
    SCWidget.validSignal.connect(mock_slot)
    #invalid h
    qtbot.keyClicks(SCWidget.h_edit, "0")
    SCWidget.a_edit.editingFinished.emit()
    mock_slot.assert_not_called()
    #all valid
    qtbot.keyClicks(SCWidget.h_edit, "\b")
    SCWidget.a_edit.editingFinished.emit()
    mock_slot.assert_called_once_with({'a': 45.0, 'alpha': 45.0, 'b': 45.0, 'beta': 45.0, 'c': 45.0, 'gamma': 45.0, 'h': -45.0, 'k': -45.0, 'l': -45.0})


def test_Crosshairs_validators(qtbot):
    """Test validators for the single crystal widget"""
    CHWidget = hppt_view.CrosshairWidget()
    qtbot.addWidget(CHWidget)

    qtbot.keyClicks(CHWidget.DeltaE_edit, "-1")
    assert CHWidget.DeltaE_edit.text() == "-1"
    assert CHWidget.DeltaE_edit.styleSheet() == ""

    qtbot.keyClicks(CHWidget.modQ_edit, "-2")
    assert CHWidget.modQ_edit.text() == "2"
    assert CHWidget.DeltaE_edit.styleSheet() == ""
    qtbot.keyClicks(CHWidget.modQ_edit, "0")
    assert CHWidget.modQ_edit.text() == "20"
    assert CHWidget.modQ_edit.styleSheet() == INVALID_QLINEEDIT

    #validate_all_inputs
    mock_slot = MagicMock()
    CHWidget.validSignal.connect(mock_slot)
    #invalid modQ
    CHWidget.DeltaE_edit.editingFinished.emit()
    mock_slot.assert_not_called()
    #all valid
    qtbot.keyClicks(CHWidget.modQ_edit, "\b")
    CHWidget.DeltaE_edit.editingFinished.emit()
    mock_slot.assert_called_once_with({'DeltaE': -1.0, 'modQ': 2.0})
