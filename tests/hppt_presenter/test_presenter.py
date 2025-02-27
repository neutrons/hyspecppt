from PySide6.QtCore import Qt
from pytest import approx

from hyspecppt.hppt.experiment_settings import INVALID_QLINEEDIT


def test_presenter_init(qtbot, hyspec_app):
    """Tests that presenter is initialized correctly"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    view = hyspec_app.main_window.HPPT_view

    # check the default values are populated
    assert view.experiment_widget.Ei_edit.text() == "20.0"
    assert view.experiment_widget.Pangle_edit.text() == "0.0"
    assert view.experiment_widget.S2_edit.text() == "30.0"
    assert view.experiment_widget.Type_combobox.currentText() == "cos" + "\u00b2" + "\u03b1" + "\u209b"


def test_selector_widget_powder_mode(hyspec_app, qtbot):
    """Test the Powder Mode in Selector widget when the radio button is pressed"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    hyspec_view.selection_widget.powder_rb.setChecked(True)

    assert not hyspec_view.sc_widget.isVisibleTo(hyspec_app)
    assert hyspec_view.crosshair_widget.modQ_edit.isEnabled()


def test_switch_to_sc(hyspec_app, qtbot):
    """Test switch_to_sc() set SingleCrystalWidget visible"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    hyspec_view.switch_to_sc()
    assert hyspec_view.sc_widget.isVisibleTo(hyspec_view)
    assert not hyspec_view.crosshair_widget.modQ_edit.isEnabled()


def test_switch_to_powder(hyspec_app, qtbot):
    """Test switch_to_powder() set SingleCrystalWidget visible"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    hyspec_view = hyspec_app.main_window.HPPT_view
    hyspec_view.switch_to_powder()
    assert not hyspec_view.sc_widget.isVisibleTo(hyspec_view)
    assert hyspec_view.crosshair_widget.modQ_edit.isEnabled()


def test_switch_to_powder_ei(hyspec_app, qtbot):
    """Test switch to Powder check Ei value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    experiment_widget = hyspec_view.experiment_widget

    # set Ei invalid value
    qtbot.keyClicks(experiment_widget.Ei_edit, "\b\b4")
    assert experiment_widget.Ei_edit.text() == "204"
    assert experiment_widget.Ei_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # Ei value should have the default valid value
    assert experiment_widget.Ei_edit.text() == "20.0"
    assert experiment_widget.Ei_edit.styleSheet() != INVALID_QLINEEDIT


def test_switch_to_powder_pangle(hyspec_app, qtbot):
    """Test switch to Powder check P angle value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    experiment_widget = hyspec_view.experiment_widget

    # empty p angle value
    experiment_widget.Pangle_edit.clear()
    assert experiment_widget.Pangle_edit.text() == ""
    assert experiment_widget.Pangle_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # P angle value should have the default valid value
    assert experiment_widget.Pangle_edit.text() == "0.0"
    assert experiment_widget.Pangle_edit.styleSheet() != INVALID_QLINEEDIT


def test_switch_to_powder_s2(hyspec_app, qtbot):
    """Test switch to Powder check S2 value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    experiment_widget = hyspec_view.experiment_widget

    # set Ei invalid value
    qtbot.keyClicks(experiment_widget.S2_edit, "\b\b6")
    assert experiment_widget.S2_edit.text() == "306"
    assert experiment_widget.S2_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # Ei value should have the default valid value
    assert experiment_widget.S2_edit.text() == "30.0"
    assert experiment_widget.S2_edit.styleSheet() != INVALID_QLINEEDIT


def test_switch_to_powder_deltae_default_value(hyspec_app, qtbot):
    """Test switch to Powder check DeltaE value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    crosshair_widget = hyspec_view.crosshair_widget

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
    crosshair_widget = hyspec_view.crosshair_widget

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
    crosshair_widget = hyspec_view.crosshair_widget
    plot_widget = hyspec_view.plot_widget

    # set a valid DeltaE value
    crosshair_widget.DeltaE_edit.clear()

    qtbot.keyClicks(crosshair_widget.DeltaE_edit, "4.1")
    assert crosshair_widget.DeltaE_edit.text() == "4.1"

    # Simulate gaining/losing focus
    crosshair_widget.DeltaE_edit.setFocus()
    qtbot.keyPress(crosshair_widget.DeltaE_edit, Qt.Key_Return)

    # plot crosshair lines are updated
    assert plot_widget.eline_data == 4.1

    # empty DeltaE value
    crosshair_widget.DeltaE_edit.clear()
    assert crosshair_widget.DeltaE_edit.text() == ""
    assert crosshair_widget.DeltaE_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # Delta E value should be back to its default value
    assert crosshair_widget.DeltaE_edit.text() == "4.1"
    assert crosshair_widget.DeltaE_edit.styleSheet() != INVALID_QLINEEDIT

    # plot crosshair lines are updated
    assert plot_widget.eline_data == 4.1
    assert plot_widget.qline_data == 0


def test_switch_to_powder_qmod_updated_values(hyspec_app, qtbot):
    """Test switch to Powder check Qmod value with a new value"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    crosshair_widget = hyspec_view.crosshair_widget
    plot_widget = hyspec_view.plot_widget

    assert crosshair_widget.modQ_edit.text() == "0.000"

    # plot crosshair lines default values
    assert plot_widget.eline_data == 0
    assert plot_widget.qline_data == 0

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

    # plot crosshair lines are updated
    assert plot_widget.qline_data == 2.35

    # empty Qmod value
    crosshair_widget.modQ_edit.clear()
    assert crosshair_widget.modQ_edit.text() == ""
    assert crosshair_widget.modQ_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_sc()

    # Qmod value should be back to its default value
    assert crosshair_widget.modQ_edit.text() == "0.000"
    assert crosshair_widget.modQ_edit.styleSheet() != INVALID_QLINEEDIT

    # plot crosshair lines are updated
    assert plot_widget.eline_data == 0
    assert plot_widget.qline_data == 0


def test_handle_field_values_update(hyspec_app, qtbot):
    """Test switch to Single Crystal check sc parameters"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    sc_widget = hyspec_view.sc_widget
    crosshair_widget = hyspec_view.crosshair_widget

    # switch to single crystal
    hyspec_view.switch_to_sc()

    # set a valid a h value
    sc_widget.h_edit.clear()
    qtbot.keyClicks(sc_widget.h_edit, "1")
    assert sc_widget.h_edit.text() == "1"

    # set a valid a k value
    sc_widget.k_edit.clear()
    qtbot.keyClicks(sc_widget.k_edit, "2")
    assert sc_widget.k_edit.text() == "2"

    # Simulate gaining/losing focus
    sc_widget.k_edit.setFocus()
    qtbot.keyPress(sc_widget.k_edit, Qt.Key_Return)

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
    sc_widget = hyspec_view.sc_widget
    crosshair_widget = hyspec_view.crosshair_widget
    plot_widget = hyspec_view.plot_widget

    # switch to single crystal
    hyspec_view.switch_to_sc()

    # set an invalid alpha value
    qtbot.keyClicks(sc_widget.alpha_edit, "00")
    assert sc_widget.alpha_edit.text() == "900"
    assert sc_widget.alpha_edit.styleSheet() == INVALID_QLINEEDIT

    # set an invalid H value
    sc_widget.h_edit.clear()
    assert sc_widget.h_edit.text() == ""
    assert sc_widget.h_edit.styleSheet() == INVALID_QLINEEDIT

    # switch to powder
    hyspec_view.switch_to_powder()

    # qmod has default value
    assert crosshair_widget.modQ_edit.text() == "0.000"

    # switch to single crystal
    hyspec_view.switch_to_sc()

    # single crystals fields back to default values
    assert sc_widget.alpha_edit.text() == "90"
    assert sc_widget.alpha_edit.styleSheet() != INVALID_QLINEEDIT

    assert sc_widget.h_edit.text() == "0"
    assert sc_widget.h_edit.styleSheet() != INVALID_QLINEEDIT

    # qmod has default value
    assert crosshair_widget.modQ_edit.text() == "0.000"

    # plot crosshair lines are default
    assert plot_widget.eline_data == 0
    assert plot_widget.qline_data == 0


def test_switch_to_sc_invalid_updated_new(hyspec_app, qtbot):
    """Test switch to Single Crystal - check sc parameters and qmod new values when switching to powder and back"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    sc_widget = hyspec_view.sc_widget
    crosshair_widget = hyspec_view.crosshair_widget
    plot_widget = hyspec_view.plot_widget

    # switch to single crystal
    hyspec_view.switch_to_sc()

    # set a valid a k value
    sc_widget.h_edit.clear()
    qtbot.keyClicks(sc_widget.h_edit, "2.2")
    assert sc_widget.h_edit.text() == "2.2"

    # Simulate gaining/losing focus
    sc_widget.h_edit.setFocus()
    qtbot.keyPress(sc_widget.h_edit, Qt.Key_Return)

    # set an invalid alpha value
    qtbot.keyClicks(sc_widget.alpha_edit, "00")
    assert sc_widget.alpha_edit.text() == "900"
    assert sc_widget.alpha_edit.styleSheet() == INVALID_QLINEEDIT

    # Simulate gaining/losing focus
    sc_widget.alpha_edit.setFocus()
    qtbot.keyPress(sc_widget.alpha_edit, Qt.Key_Return)

    # set an invalid H value
    sc_widget.h_edit.clear()
    assert sc_widget.h_edit.text() == ""
    assert sc_widget.h_edit.styleSheet() == INVALID_QLINEEDIT

    # Simulate gaining/losing focus
    sc_widget.h_edit.setFocus()
    qtbot.keyPress(sc_widget.h_edit, Qt.Key_Return)

    # switch to powder
    hyspec_view.switch_to_powder()

    # qmod has the calculated value
    assert crosshair_widget.modQ_edit.text() == "13.823"
    # qmod value updated manually
    crosshair_widget.modQ_edit.clear()
    qtbot.keyClicks(crosshair_widget.modQ_edit, "5")
    assert crosshair_widget.modQ_edit.text() == "5"

    # switch to single crystal
    hyspec_view.switch_to_sc()

    # single crystals fields back to default values
    assert sc_widget.alpha_edit.text() == "90.0"
    assert sc_widget.alpha_edit.styleSheet() != INVALID_QLINEEDIT

    # single crystals fields back to the last valid value
    assert sc_widget.h_edit.text() == "2.2"
    assert sc_widget.h_edit.styleSheet() != INVALID_QLINEEDIT

    # qmod has the calculated value
    assert crosshair_widget.modQ_edit.text() == "13.823"

    # plot crosshair lines are updated
    assert plot_widget.eline_data == 0
    assert plot_widget.qline_data == approx(13.823, rel=1e-6)
    assert plot_widget.eline.get_color() == "darkgrey"
    assert plot_widget.qline.get_color() == "darkgrey"


def test_return_invalid_qmod(hyspec_app, qtbot):
    """Test to calculate and return invalid Qmod value greater than 15"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    crosshair_widget = hyspec_view.crosshair_widget
    sc_widget = hyspec_view.sc_widget
    plot_widget = hyspec_view.plot_widget

    # switch to single crystal
    hyspec_view.switch_to_sc()

    # lattice parameter H update
    sc_widget.h_edit.clear()
    qtbot.keyClicks(sc_widget.h_edit, "1")
    assert sc_widget.h_edit.text() == "1"
    assert sc_widget.h_edit.styleSheet() != INVALID_QLINEEDIT

    # lattice parameter K update
    sc_widget.k_edit.clear()
    qtbot.keyClicks(sc_widget.k_edit, "2")
    assert sc_widget.k_edit.text() == "2"
    assert sc_widget.k_edit.styleSheet() != INVALID_QLINEEDIT

    # lattice parameter L update
    sc_widget.l_edit.clear()
    qtbot.keyClicks(sc_widget.l_edit, "1")
    assert sc_widget.l_edit.text() == "1"
    assert sc_widget.l_edit.styleSheet() != INVALID_QLINEEDIT

    # Simulate gaining/losing focus
    sc_widget.h_edit.setFocus()
    qtbot.keyPress(sc_widget.h_edit, Qt.Key_Return)

    # Qmod has the calculated invalid value
    assert crosshair_widget.modQ_edit.text() == "15.391"
    assert crosshair_widget.modQ_edit.styleSheet() == INVALID_QLINEEDIT

    # plot crosshair lines are not updated / stay default
    assert plot_widget.eline_data == 0
    assert plot_widget.qline_data == 0
    assert plot_widget.eline.get_color() == "darkgrey"
    assert plot_widget.qline.get_color() == "darkgrey"


def test_default_plot_data(hyspec_app, qtbot):
    """Test to compare the plot meta data for default values"""
    # unicode
    alpha = "\u03b1"
    square = "\u00b2"
    subscript_s = "\u209b"

    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    plot_widget = hyspec_view.plot_widget

    # switch to single crystal
    hyspec_view.switch_to_sc()

    # plot should exist

    # assert crosshair
    assert plot_widget.eline_data == 0
    assert plot_widget.qline_data == 0
    assert plot_widget.eline.get_color() == "darkgrey"
    assert plot_widget.qline.get_color() == "darkgrey"

    # assert heatmap
    assert plot_widget.ax.get_ylabel() == r"$\Delta E$"
    assert plot_widget.ax.get_xlabel() == "$|Q|$"
    assert plot_widget.cb.ax.get_ylabel() == "cos" + square + alpha + subscript_s


def test_update_plot_data(hyspec_app, qtbot):
    """Test to compare the updated plot meta data for default values"""
    # unicode
    alpha = "\u03b1"
    subscript_s = "\u209b"

    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    sc_widget = hyspec_view.sc_widget
    experiment_widget = hyspec_view.experiment_widget
    plot_widget = hyspec_view.plot_widget

    # switch to single crystal
    hyspec_view.switch_to_sc()

    # update type to first item
    # choice = alpha + subscript_s
    experiment_widget.Type_combobox.setCurrentIndex(0)

    # set a valid H value
    sc_widget.h_edit.clear()
    qtbot.keyClicks(sc_widget.h_edit, "1.2")

    # Simulate gaining/losing focus
    sc_widget.h_edit.setFocus()
    qtbot.keyPress(sc_widget.h_edit, Qt.Key_Return)

    # plot should exist

    # assert crosshair
    assert plot_widget.eline_data == 0
    assert round(plot_widget.qline_data, 2) == approx(7.540)
    assert plot_widget.eline.get_color() == "darkgrey"
    assert plot_widget.qline.get_color() == "darkgrey"

    # assert heatmap
    assert plot_widget.ax.get_ylabel() == r"$\Delta E$"
    assert plot_widget.ax.get_xlabel() == "$|Q|$"
    assert plot_widget.cb.ax.get_ylabel() == alpha + subscript_s


def test_emin_deltae_updated_values(hyspec_app, qtbot):
    """Test deltae value the causes replotting"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    hyspec_model = hyspec_app.main_window.HPPT_presenter.model
    crosshair_widget = hyspec_view.crosshair_widget
    plot_widget = hyspec_view.plot_widget

    assert hyspec_model.Emin == -20
    default_axes = plot_widget.heatmap.get_array()
    # set a valid DeltaE value
    crosshair_widget.DeltaE_edit.clear()

    qtbot.keyClicks(crosshair_widget.DeltaE_edit, "-30")
    assert crosshair_widget.DeltaE_edit.text() == "-30"

    # Simulate gaining/losing focus
    crosshair_widget.DeltaE_edit.setFocus()
    qtbot.keyPress(crosshair_widget.DeltaE_edit, Qt.Key_Return)

    # assert emin has changed
    assert hyspec_model.Emin == -36

    # plot should be updated
    assert not (default_axes == plot_widget.heatmap.get_array()).all()

    # assert crosshair
    assert plot_widget.eline_data == -30.0
    assert round(plot_widget.qline_data, 2) == 0.0
    assert plot_widget.eline.get_color() == "darkgrey"
    assert plot_widget.qline.get_color() == "darkgrey"

    # assert heatmap
    assert plot_widget.ax.get_ylabel() == r"$\Delta E$"
    assert plot_widget.ax.get_xlabel() == "$|Q|$"


def test_handle_Q_beam_ang_values_update(hyspec_app, qtbot):
    """Test switch to Single Crystal mode and powder mode will update the Q-beam angle"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    sc_widget = hyspec_view.sc_widget
    crosshair_widget = hyspec_view.crosshair_widget

    # switch to single crystal
    hyspec_view.switch_to_sc()

    # set a valid a value
    sc_widget.a_edit.clear()
    qtbot.keyClicks(sc_widget.a_edit, "10")
    assert sc_widget.a_edit.text() == "10"

    # set a valid b value
    sc_widget.b_edit.clear()
    qtbot.keyClicks(sc_widget.b_edit, "10")
    assert sc_widget.b_edit.text() == "10"

    # set a valid c value
    sc_widget.c_edit.clear()
    qtbot.keyClicks(sc_widget.c_edit, "10")
    assert sc_widget.c_edit.text() == "10"

    # set a valid h value
    sc_widget.h_edit.clear()
    qtbot.keyClicks(sc_widget.h_edit, "1")
    assert sc_widget.h_edit.text() == "1"

    # set a valid a k value
    sc_widget.k_edit.clear()
    qtbot.keyClicks(sc_widget.k_edit, "1")
    assert sc_widget.k_edit.text() == "1"

    # # set a valid a l value
    sc_widget.l_edit.clear()
    qtbot.keyClicks(sc_widget.l_edit, "0")
    assert sc_widget.l_edit.text() == "0"

    # # Simulate gaining/losing focus
    sc_widget.l_edit.setFocus()
    qtbot.keyPress(sc_widget.l_edit, Qt.Key_Return)

    # # Qmod value should be updated with the new value
    assert crosshair_widget.modQ_edit.text() == "0.889"
    assert crosshair_widget.DeltaE_edit.text() == "0"
    assert crosshair_widget.modQ_edit.styleSheet() != INVALID_QLINEEDIT
    assert crosshair_widget.QZ_angle_edit.text() == "-81.778"

    # Switch to powder and change DeltaE
    hyspec_view.switch_to_powder()
    hyspec_view.selection_widget.powder_rb.setChecked(True)

    assert crosshair_widget.QZ_angle_edit.text() == "-81.778"
    crosshair_widget.DeltaE_edit.clear()
    qtbot.keyClicks(crosshair_widget.DeltaE_edit, "5.0")
    assert crosshair_widget.DeltaE_edit.text() == "5.0"
    crosshair_widget.DeltaE_edit.setFocus()
    qtbot.keyPress(crosshair_widget.DeltaE_edit, Qt.Key_Return)

    assert crosshair_widget.QZ_angle_edit.text() == "-54.556"


def test_handle_Q_beam_ang_values_powder(hyspec_app, qtbot):
    """Test switch to Single Crystal mode and powder mode will update the Q-beam angle"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    crosshair_widget = hyspec_view.crosshair_widget

    # Switch to powder and change DeltaE
    hyspec_view.switch_to_powder()
    hyspec_view.selection_widget.powder_rb.setChecked(True)

    crosshair_widget.DeltaE_edit.clear()
    qtbot.keyClicks(crosshair_widget.DeltaE_edit, "5.0")
    assert crosshair_widget.DeltaE_edit.text() == "5.0"
    crosshair_widget.DeltaE_edit.setFocus()

    crosshair_widget.modQ_edit.clear()
    qtbot.keyClicks(crosshair_widget.modQ_edit, "2.000")
    assert crosshair_widget.modQ_edit.text() == "2.000"
    crosshair_widget.modQ_edit.setFocus()
    qtbot.keyPress(crosshair_widget.modQ_edit, Qt.Key_Return)

    assert crosshair_widget.QZ_angle_edit.text() == "-58.932"


def test_handle_Q_beam_ang_values_S2(hyspec_app, qtbot):
    """Test switch to Single Crystal mode and powder mode will update the Q-beam angle"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    crosshair_widget = hyspec_view.crosshair_widget

    # Switch to powder and change DeltaE
    hyspec_view.switch_to_powder()
    hyspec_view.selection_widget.powder_rb.setChecked(True)

    crosshair_widget.DeltaE_edit.clear()
    qtbot.keyClicks(crosshair_widget.DeltaE_edit, "5.0")
    assert crosshair_widget.DeltaE_edit.text() == "5.0"
    crosshair_widget.DeltaE_edit.setFocus()

    exp_widget = hyspec_view.experiment_widget
    crosshair_widget.modQ_edit.clear()
    qtbot.keyClicks(crosshair_widget.modQ_edit, "2.000")
    assert crosshair_widget.modQ_edit.text() == "2.000"
    crosshair_widget.modQ_edit.setFocus()
    qtbot.keyPress(crosshair_widget.modQ_edit, Qt.Key_Return)

    assert exp_widget.S2_edit.text() == "30.0"  # positive S2
    assert crosshair_widget.QZ_angle_edit.text() == "-58.932"  # negative Q-beam ang

    # change S2 to -30
    exp_widget.S2_edit.clear()
    qtbot.keyClicks(exp_widget.S2_edit, "-30")  # negative S2
    exp_widget.S2_edit.setFocus()
    qtbot.keyPress(exp_widget.S2_edit, Qt.Key_Return)
    assert crosshair_widget.QZ_angle_edit.text() == "58.932"  # positive Q-beam ang


def test_handle_Q_beam_ang_values_scattering_triangle_not_closed(hyspec_app, qtbot):
    """Test switch to Single Crystal mode and powder mode will update the Q-beam angle"""
    # show the app
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()

    hyspec_view = hyspec_app.main_window.HPPT_view
    crosshair_widget = hyspec_view.crosshair_widget

    # Switch to powder and change DeltaE
    hyspec_view.switch_to_powder()
    hyspec_view.selection_widget.powder_rb.setChecked(True)

    crosshair_widget.DeltaE_edit.clear()
    qtbot.keyClicks(crosshair_widget.DeltaE_edit, "5.0")
    assert crosshair_widget.DeltaE_edit.text() == "5.0"
    crosshair_widget.DeltaE_edit.setFocus()

    exp_widget = hyspec_view.experiment_widget
    crosshair_widget.modQ_edit.clear()
    qtbot.keyClicks(crosshair_widget.modQ_edit, "2.000")
    assert crosshair_widget.modQ_edit.text() == "2.000"
    crosshair_widget.modQ_edit.setFocus()
    qtbot.keyPress(crosshair_widget.modQ_edit, Qt.Key_Return)

    assert exp_widget.S2_edit.text() == "30.0"
    assert crosshair_widget.QZ_angle_edit.text() == "-58.932"

    # now user change modQ to 0 while deltaE left at 5

    exp_widget = hyspec_view.experiment_widget
    crosshair_widget.modQ_edit.clear()
    qtbot.keyClicks(crosshair_widget.modQ_edit, "0.000")
    assert crosshair_widget.modQ_edit.text() == "0.000"
    crosshair_widget.modQ_edit.setFocus()
    qtbot.keyPress(crosshair_widget.modQ_edit, Qt.Key_Return)

    assert crosshair_widget.QZ_angle_edit.text() == "nan"
