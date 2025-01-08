"""Presenter for the Main tab"""

from .experiment_settings import DEFAULT_CROSSHAIR, DEFAULT_EXPERIMENT, DEFAULT_LATTICE, DEFAULT_MODE, PLOT_TYPES


class HyspecPPTPresenter:
    """Main presenter"""

    def __init__(self, view: any, model: any):
        """Constructor
        :view: hppt_view class type
        :model:hppt_model class type
        """
        self._view = view
        self._model = model

        # M-V-P connections through callbacks
        self.view.connect_fields_update(self.handle_field_values_update)
        self.view.connect_powder_mode_switch(self.handle_switch_to_powder)
        self.view.connect_sc_mode_switch(self.handle_switch_to_sc)

        self.view.SCW.set_values(DEFAULT_LATTICE)
        self.view.EW.initializeCombo(PLOT_TYPES)
        self.view.EW.set_values(DEFAULT_EXPERIMENT)
        self.view.CW.set_values(DEFAULT_CROSSHAIR)

        # model init
        # to be removed needs to happen in the model
        self.model.set_experiment_data(**DEFAULT_EXPERIMENT)
        print("DEFAULT_CROSSHAIR", DEFAULT_CROSSHAIR, DEFAULT_MODE)
        self.model.set_crosshair_data(**DEFAULT_CROSSHAIR, **DEFAULT_MODE)
        self.model.set_single_crystal_data(params=DEFAULT_LATTICE)

        self.view.SelW.selector_init()  # pass the default mode from experiment type

    @property
    def view(self):
        """Return the view for this presenter"""
        return self._view

    @property
    def model(self):
        """Return the model for this presenter"""
        return self._model

    def handle_field_values_update(self, field_values):
        """Save the values in the model"""
        section = field_values["name"]
        data = field_values["data"]
        if section == "crosshair":
            # get the current experiment type
            experiment_type_label = self.view.SelW.get_selected_mode_label()
            experiment_type = "powder"
            if experiment_type_label.startswith("Single"):
                experiment_type = "single_crystal"
            print("data", data, experiment_type)
            self.model.set_crosshair_data(
                current_experiment_type=experiment_type, DeltaE=float(data["DeltaE"]), modQ=float(data["modQ"])
            )
        elif section == "experiment":
            self.model.set_experiment_data(
                float(data["Ei"]), float(data["S2"]), float(data["alpha_p"]), data["plot_type"]
            )
        else:
            print("dsad", data)
            self.model.set_single_crystal_data(data)

    def handle_switch_to_powder(self):
        """Switch to Powder mode"""
        # update the fields' visibility
        self.view.field_visibility_in_Powder()
        # update the experiment type in the model
        experiment_type = "powder"
        self.model.set_crosshair_data(current_experiment_type=experiment_type)

        # get the valid values for crosshair saved fields
        # if the view contains an invalid value it is overwritten
        saved_values = self.model.get_crosshair_data()
        print("saved", saved_values)
        self.view.CW.set_values(saved_values)
        print("view updated with: ", saved_values)

    def handle_switch_to_sc(self):
        """Switch to Single Crystal mode"""
        # update the fields' visibility
        self.view.field_visibility_in_SC()
        # update the experiment type in the model
        experiment_type = "single_crystal"
        self.model.set_crosshair_data(current_experiment_type=experiment_type)

        # get the valid values for crosshair saved fields
        # if the view contains an invalid value it is overwritten
        saved_values = self.model.get_crosshair_data()
        print("sc saved", saved_values)
        self.view.CW.set_values(saved_values)
        print("view updated with: ", saved_values)

        # get the valid values for lattice saved fields
        # saved_values = self.model.get_single_crystal_data()
        # self.view.CW.set_values(saved_values)
