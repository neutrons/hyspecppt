import hyspecppt.hppt.hppt_view as hppt_view
from hyspecppt.hppt.experiment_settings import INVALID_QLINEEDIT


def test_Experiment_validators(qtbot):
    """test validators for the experiment widget"""
    ExpWidget = hppt_view.ExperimentWidget()
    qtbot.addWidget(ExpWidget)

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


def test_Single_Crystal_validators(qtbot):
    """test validators for the single crystal widget"""
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

def test_Crosshairs_validators(qtbot):
    """test validators for the single crystal widget"""
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
