from PySide6.QtCore import Qt

from hyspecppt.hppt.experiment_settings import INVALID_QLINEEDIT


def test_presenter_init(qtbot, hyspec_app):
    """Tests that presenter is initialized correctly"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    view = hyspec_app.main_window.HPPT_view

    # check the default values are populated
    assert view.EW.Ei_edit.text() == "20"
    assert view.EW.Pangle_edit.text() == "0"
    assert view.EW.S2_edit.text() == "30"
    assert view.EW.Type_combobox.currentText() == "cos" + "\u03b1" + "\u209b" + "\u00b2"


def test_selector_widget_powder_mode(hyspec_app, qtbot):
    """Test the Powder Mode in Selector widget when the radio button is pressed"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    hyspec_view.SelW.powder_rb.setChecked(True)

    assert not hyspec_view.SCW.isVisibleTo(hyspec_app)
    assert hyspec_view.CW.modQ_edit.isEnabled()


def test_switch_to_sc(hyspec_app, qtbot):
    """Test switch_to_SC() set SingleCrystalWidget visible"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    hyspec_view.switch_to_SC()
    assert hyspec_view.SCW.isVisibleTo(hyspec_view)
    assert not hyspec_view.CW.modQ_edit.isEnabled()


def test_switch_to_powder(hyspec_app, qtbot):
    """Test switch_to_powder() set SingleCrystalWidget visible"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    hyspec_view = hyspec_app.main_window.HPPT_view
    hyspec_view.switch_to_powder()
    assert not hyspec_view.SCW.isVisibleTo(hyspec_view)
    assert hyspec_view.CW.modQ_edit.isEnabled()


def test_switch_to_powder_ei(hyspec_app, qtbot):
    """Test switch to Powder check Ei value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    experiment_widget = hyspec_view.EW

    # set Ei invalid value
    qtbot.keyClicks(experiment_widget.Ei_edit, "4")
    assert experiment_widget.Ei_edit.text() == "204"
    assert experiment_widget.Ei_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # Ei value should have the default valid value
    assert experiment_widget.Ei_edit.text() == "20"
    assert experiment_widget.Ei_edit.styleSheet() != INVALID_QLINEEDIT


def test_switch_to_powder_pangle(hyspec_app, qtbot):
    """Test switch to Powder check P angle value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    experiment_widget = hyspec_view.EW

    # empty p angle value
    experiment_widget.Pangle_edit.clear()
    assert experiment_widget.Pangle_edit.text() == ""
    assert experiment_widget.Pangle_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # P angle value should have the default valid value
    assert experiment_widget.Pangle_edit.text() == "0"
    assert experiment_widget.Pangle_edit.styleSheet() != INVALID_QLINEEDIT


def test_switch_to_powder_s2(hyspec_app, qtbot):
    """Test switch to Powder check S2 value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    experiment_widget = hyspec_view.EW

    # set Ei invalid value
    qtbot.keyClicks(experiment_widget.S2_edit, "6")
    assert experiment_widget.S2_edit.text() == "306"
    assert experiment_widget.S2_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # Ei value should have the default valid value
    assert experiment_widget.S2_edit.text() == "30"
    assert experiment_widget.S2_edit.styleSheet() != INVALID_QLINEEDIT


def test_switch_to_powder_deltae_default_value(hyspec_app, qtbot):
    """Test switch to Powder check DeltaE value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    crosshair_widget = hyspec_view.CW

    # empty DeltaE value
    crosshair_widget.DeltaE_edit.clear()
    assert crosshair_widget.DeltaE_edit.text() == ""
    assert crosshair_widget.DeltaE_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # Delta E value should be back to its default value
    assert crosshair_widget.DeltaE_edit.text() == "0"
    assert crosshair_widget.DeltaE_edit.styleSheet() != INVALID_QLINEEDIT


def test_switch_to_powder_qmod_default_value(hyspec_app, qtbot):
    """Test switch to Powder check Qmod value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    crosshair_widget = hyspec_view.CW

    # empty Qmod value
    crosshair_widget.modQ_edit.clear()
    assert crosshair_widget.modQ_edit.text() == ""
    assert crosshair_widget.modQ_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # Qmod value should be back to its default value
    assert crosshair_widget.modQ_edit.text() == "0.000"
    assert crosshair_widget.modQ_edit.styleSheet() != INVALID_QLINEEDIT


def test_switch_to_powder_deltae_updated_values(hyspec_app, qtbot):
    """Test switch to Powder check DeltaE value with a new value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    crosshair_widget = hyspec_view.CW

    # set a valid DeltaE value
    crosshair_widget.DeltaE_edit.clear()

    qtbot.keyClicks(crosshair_widget.DeltaE_edit, "4.1")
    assert crosshair_widget.DeltaE_edit.text() == "4.1"

    # Simulate gaining/losing focus
    crosshair_widget.DeltaE_edit.setFocus()
    qtbot.keyPress(crosshair_widget.DeltaE_edit, Qt.Key_Return)

    # empty DeltaE value
    crosshair_widget.DeltaE_edit.clear()
    assert crosshair_widget.DeltaE_edit.text() == ""
    assert crosshair_widget.DeltaE_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # Delta E value should be back to its default value
    assert crosshair_widget.DeltaE_edit.text() == "4.1"
    assert crosshair_widget.DeltaE_edit.styleSheet() != INVALID_QLINEEDIT


def test_switch_to_powder_qmod_updated_values(hyspec_app, qtbot):
    """Test switch to Powder check Qmod value with a new value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    crosshair_widget = hyspec_view.CW

    assert crosshair_widget.modQ_edit.text() == "0.000"

    # switch to powder
    hyspec_view.switch_to_powder()

    # set a valid Qmod value
    crosshair_widget.modQ_edit.clear()
    assert crosshair_widget.modQ_edit.text() == ""

    qtbot.keyClicks(crosshair_widget.modQ_edit, "2.35")
    assert crosshair_widget.modQ_edit.text() == "2.35"

    # Simulate gaining/losing focus
    crosshair_widget.modQ_edit.setFocus()
    qtbot.keyPress(crosshair_widget.modQ_edit, Qt.Key_Return)

    # empty Qmod value
    crosshair_widget.modQ_edit.clear()
    assert crosshair_widget.modQ_edit.text() == ""
    assert crosshair_widget.modQ_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_SC()

    # Qmod value should be back to its default value
    assert crosshair_widget.modQ_edit.text() == "0.000"
    assert crosshair_widget.modQ_edit.styleSheet() != INVALID_QLINEEDIT


def test_handle_field_values_update(hyspec_app, qtbot):
    """Test switch to Single Crystal check sc parameters"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    experiment_widget = hyspec_view.SCW
    crosshair_widget = hyspec_view.CW

    # switch to single crystal
    hyspec_view.switch_to_SC()

    # set a valid a h value
    experiment_widget.h_edit.clear()
    qtbot.keyClicks(experiment_widget.h_edit, "1")
    assert experiment_widget.h_edit.text() == "1"

    # set a valid a k value
    experiment_widget.k_edit.clear()
    qtbot.keyClicks(experiment_widget.k_edit, "2")
    assert experiment_widget.k_edit.text() == "2"

    # Simulate gaining/losing focus
    experiment_widget.k_edit.setFocus()
    qtbot.keyPress(experiment_widget.k_edit, Qt.Key_Return)

    # Qmod value should be updated with the new value
    assert crosshair_widget.modQ_edit.text() == "14.050"
    assert crosshair_widget.modQ_edit.styleSheet() != INVALID_QLINEEDIT


def test_switch_to_sc_invalid_updated_default(hyspec_app, qtbot):
    """Test switch to Single Crystal - check sc parameters default values when switching to powder and back"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    experiment_widget = hyspec_view.SCW
    crosshair_widget = hyspec_view.CW

    # switch to single crystal
    hyspec_view.switch_to_SC()

    # set an invalid alpha value
    qtbot.keyClicks(experiment_widget.alpha_edit, "00")
    assert experiment_widget.alpha_edit.text() == "900"
    assert experiment_widget.alpha_edit.styleSheet() == INVALID_QLINEEDIT

    # set an invalid H value
    experiment_widget.h_edit.clear()
    assert experiment_widget.h_edit.text() == ""
    assert experiment_widget.h_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # qmod has default value
    assert crosshair_widget.modQ_edit.text() == "0.000"

    # switch to single crystal
    hyspec_view.switch_to_SC()

    # single crystals fields back to default values
    assert experiment_widget.alpha_edit.text() == "90"
    assert experiment_widget.alpha_edit.styleSheet() != INVALID_QLINEEDIT

    assert experiment_widget.h_edit.text() == "0"
    assert experiment_widget.h_edit.styleSheet() != INVALID_QLINEEDIT

    # qmod has default value
    assert crosshair_widget.modQ_edit.text() == "0.000"


def test_switch_to_sc_invalid_updated_new(hyspec_app, qtbot):
    """Test switch to Single Crystal - check sc parameters and qmod new values when switching to powder and back"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    experiment_widget = hyspec_view.SCW
    crosshair_widget = hyspec_view.CW

    # switch to single crystal
    hyspec_view.switch_to_SC()

    # set a valid a k value
    experiment_widget.h_edit.clear()
    qtbot.keyClicks(experiment_widget.h_edit, "2.2")
    assert experiment_widget.h_edit.text() == "2.2"

    # Simulate gaining/losing focus
    experiment_widget.h_edit.setFocus()
    qtbot.keyPress(experiment_widget.h_edit, Qt.Key_Return)

    # set an invalid alpha value
    qtbot.keyClicks(experiment_widget.alpha_edit, "00")
    assert experiment_widget.alpha_edit.text() == "900"
    assert experiment_widget.alpha_edit.styleSheet() == INVALID_QLINEEDIT

    # Simulate gaining/losing focus
    experiment_widget.alpha_edit.setFocus()
    qtbot.keyPress(experiment_widget.alpha_edit, Qt.Key_Return)

    # set an invalid H value
    experiment_widget.h_edit.clear()
    assert experiment_widget.h_edit.text() == ""
    assert experiment_widget.h_edit.styleSheet() == INVALID_QLINEEDIT

    # Simulate gaining/losing focus
    experiment_widget.h_edit.setFocus()
    qtbot.keyPress(experiment_widget.h_edit, Qt.Key_Return)

    # switch to powder
    hyspec_view.switch_to_powder()

    # qmod has the calculated value
    assert crosshair_widget.modQ_edit.text() == "13.823"
    # qmod value updated manually
    crosshair_widget.modQ_edit.clear()
    qtbot.keyClicks(crosshair_widget.modQ_edit, "5")
    assert crosshair_widget.modQ_edit.text() == "5"

    # switch to single crystal
    hyspec_view.switch_to_SC()

    # single crystals fields back to default values
    assert experiment_widget.alpha_edit.text() == "90.0"
    assert experiment_widget.alpha_edit.styleSheet() != INVALID_QLINEEDIT

    # single crystals fields back to the last valid value
    assert experiment_widget.h_edit.text() == "2.2"
    assert experiment_widget.h_edit.styleSheet() != INVALID_QLINEEDIT

    # qmod has the calculated value
    assert crosshair_widget.modQ_edit.text() == "13.823"
