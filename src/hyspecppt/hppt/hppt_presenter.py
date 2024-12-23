"""Presenter for the Main tab"""

from .experiment_settings import DEFAULT_LATTICE, PLOT_TYPES


class HyspecPPTPresenter:
    """Main presenter"""

    def __init__(self, view, model):
        """Constructor"""
        self._view = view
        self._model = model
        self.view.SCW.set_values(DEFAULT_LATTICE)
        self.view.EW.initializeCombo(PLOT_TYPES)

    @property
    def view(self):
        """Return the view for this presenter"""
        return self._view

    @property
    def model(self):
        """Return the model for this presenter"""
        return self._model
