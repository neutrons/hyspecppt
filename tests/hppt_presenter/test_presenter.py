from unittest.mock import Mock

import hyspecppt.hppt.hppt_presenter as hppt_presenter
from hyspecppt.hppt.experiment_settings import DEFAULT_CROSSHAIR, DEFAULT_EXPERIMENT, DEFAULT_LATTICE, PLOT_TYPES


def test_presenter_init(qtbot):
    """Tests that presenter is initialized correctly"""
    mock_view = Mock()
    mock_model = Mock()
    presenter = hppt_presenter.HyspecPPTPresenter(mock_view, mock_model)
    mock_view.SCW.set_values.assert_called_once_with(DEFAULT_LATTICE)
    mock_view.EW.initializeCombo.assert_called_once_with(PLOT_TYPES)
    mock_view.EW.set_values.assert_called_once_with(DEFAULT_EXPERIMENT)
    mock_view.CW.set_values.assert_called_once_with(DEFAULT_CROSSHAIR)
    mock_view.SelW.set_SC_toggle.assert_called_once_with(True)
    # maybe move these to a function in the view
    mock_view.EW.Ei_edit.text.assert_called_once()
    mock_view.EW.Pangle_edit.text.assert_called_once()
    mock_view.EW.S2_edit.text.assert_called_once()
    mock_view.EW.Type_combobox.currentText.assert_called_once()
