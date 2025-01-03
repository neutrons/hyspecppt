"""Presenter for the Main tab"""

from qtpy.QtWidgets import QWidget

from .experiment_settings import DEFAULT_CROSSHAIR, DEFAULT_EXPERIMENT, DEFAULT_LATTICE, PLOT_TYPES


class HyspecPPTPresenter:
    """Main presenter"""

    def __init__(self, view: "[QWidget]", model: "[QWidget]"):
        """Constructor
        :view: hppt_view class type
        :model:hppt_model class type
        """
        self._view = view
        self._model = model
        #initialize widgets
        self.view.EW.initializeCombo(PLOT_TYPES)
        self.view.EW.set_values(DEFAULT_EXPERIMENT)
        self.view.CW.set_values(DEFAULT_CROSSHAIR)
        self.view.SCW.set_values(DEFAULT_LATTICE)
        #select calculation mode
        self.view.SelW.set_SC_toggle(True)
        #initialize model
        self.model.store_experiment_data(**DEFAULT_EXPERIMENT)
        self.model.store_crosshair_data(current_experiment_type="crystal", **DEFAULT_CROSSHAIR)
        self.model.store_single_crystal_data(DEFAULT_LATTICE)

        #connections
        self.view.EW.valid_signal.connect(self.update_experiment_values)
        self.view.SelW.sc_rb.toggled.connect(self.q_mode_SC)
        self.view.SelW.powder_rb.toggled.connect(self.q_mode_powder)
        self.view.SCW.valid_signal.connect(self.update_SC_values)
        self.view.CW.valid_signal.connect(self.update_cursor_values)

    @property
    def view(self):
        """Return the view for this presenter"""
        return self._view

    @property
    def model(self):
        """Return the model for this presenter"""
        return self._model

    def q_mode_powder(self) -> None:
        """switch to powder mode"""
        self.model.store_crosshair_data(current_experiment_type='powder')
        crosshair = self.model.get_crosshair()
        self.view.CW.set_values(crosshair)
        self.set_PlotWidget_values(cursor_position=crosshair)

    def q_mode_SC(self) -> None:
        """switch to crystal"""
        self.model.store_crosshair_data(current_experiment_type='crystal')
        crosshair = self.model.get_crosshair()
        self.view.CW.set_values(crosshair)
        self.set_PlotWidget_values(cursor_position=crosshair)

    def update_experiment_values(self, new_values: dict[str, float]) -> None:
        """Ei/S2/alpha_p/plot_type update"""
        self.model.store_experiment_data(**new_values)
        new_intensity = self.model.calculate_graph_data()
        self.set_PlotWidget_values(intensity = new_intensity)

    def update_cursor_values(self, new_values: dict[str, float]) -> None:
        """DeltaE/modQ update"""
        #TODO: check on DeltaE<-Ei
        self.model.store_crosshair_data(**new_values)
        self.set_PlotWidget_values(cursor_position=new_values)

    def update_SC_values(self, new_values: dict[str, float]) -> None:
        self.model.store_single_crystal_data(new_values)
        new_position = self.model.get_crosshair()
        self.view.CW.set_values(new_position)
        self.set_PlotWidget_values(cursor_position=new_position)

    def set_PlotWidget_values(self, intensity = "new_intensity", cursor_position = "new_position", label="new_label"):
        """Pass through intensity matrix into plot in view"""
        print('call plot:', intensity, cursor_position, label)
