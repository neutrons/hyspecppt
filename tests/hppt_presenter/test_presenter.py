import unittest
from unittest.mock import Mock

from hyspecppt.hppt.experiment_settings import DEFAULT_CROSSHAIR, DEFAULT_EXPERIMENT, DEFAULT_LATTICE, PLOT_TYPES
from hyspecppt.hppt.hppt_presenter import HyspecPPTPresenter


class PresenterTests(unittest.TestCase):
    def test_presenter_init(self):
        """Tests that presenter is initialized correctly"""
        mock_view = Mock()
        mock_model = Mock()
        presenter = HyspecPPTPresenter(mock_view, mock_model)
        mock_view.SCW.set_values.assert_called_once_with(DEFAULT_LATTICE)
        mock_view.EW.initializeCombo.assert_called_once_with(PLOT_TYPES)
        mock_view.EW.set_values.assert_called_once_with(DEFAULT_EXPERIMENT)
        mock_view.CW.set_values.assert_called_once_with(DEFAULT_CROSSHAIR)
        # maybe move these to a function in the view
        mock_view.EW.Ei_edit.text.assert_called_once()
        mock_view.EW.Pangle_edit.text.assert_called_once()
        mock_view.EW.S2_edit.text.assert_called_once()
        mock_view.EW.Type_combobox.currentText.assert_called_once()
        assert presenter.view == mock_view
        assert presenter.model == mock_model


def test_Selector_widget_powder_mode(hyspec_app, qtbot):
    """Test the Powder Mode in Selector widget when the radio button is pressed"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    hyspec_view = hyspec_app.main_window.HPPT_view
    hyspec_view.SelW.powder_rb.setChecked(True)

    assert not hyspec_view.SCW.isVisibleTo(hyspec_app)
    assert hyspec_view.CW.modQ_edit.isEnabled()
