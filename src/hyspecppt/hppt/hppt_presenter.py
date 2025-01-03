"""Presenter for the Main tab"""

from .experiment_settings import DEFAULT_CROSSHAIR, DEFAULT_EXPERIMENT, DEFAULT_LATTICE, PLOT_TYPES


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

        self.view.SCW.set_values(DEFAULT_LATTICE)
        self.view.EW.initializeCombo(PLOT_TYPES)
        self.view.EW.set_values(DEFAULT_EXPERIMENT)
        self.view.CW.set_values(DEFAULT_CROSSHAIR)

        # to be removed
        self.get_Experiment_values()
        self.get_SingleCrystal_values()
        self.get_Selector_values()
        self.get_Crosshair_values()

    @property
    def view(self):
        """Return the view for this presenter"""
        return self._view

    @property
    def model(self):
        """Return the model for this presenter"""
        return self._model

    def get_Experiment_values(self) -> dict:
        """Get Ei, Pangle, S2, Type values from Experiment

        return: dict of Experiment key value pairs
        """
        EW_dict = {}
        EW_dict["Ei"] = self.view.EW.Ei_edit.text()
        EW_dict["Pangle"] = self.view.EW.Pangle_edit.text()
        EW_dict["S2"] = self.view.EW.S2_edit.text()
        EW_dict["Type"] = self.view.EW.Type_combobox.currentText()
        return EW_dict

    def get_Selector_values(self):
        """Check if Single Crystal radio button is checked

        return: True - Single Crystal radio button is toggled
                False - Single Crystal radio button is not toggled. Powder radio button is toggled
        """
        return self.view.SelW.sc_rb.isChecked()

    def get_SingleCrystal_values(self):
        """Get Single Crystal mode specific values from SingleCrystalWidget

        return: dict of Single Crystal key value pairs
        """
        SC_dict = {}
        SC_dict["a"] = self.view.SCW.a_edit.text()
        SC_dict["b"] = self.view.SCW.b_edit.text()
        SC_dict["c"] = self.view.SCW.c_edit.text()

        SC_dict["alpha"] = self.view.SCW.alpha_edit.text()
        SC_dict["beta"] = self.view.SCW.beta_edit.text()
        SC_dict["gamma"] = self.view.SCW.gamma_edit.text()

        SC_dict["h"] = self.view.SCW.h_edit.text()
        SC_dict["k"] = self.view.SCW.k_edit.text()
        SC_dict["l"] = self.view.SCW.l_edit.text()
        return SC_dict

    def get_Crosshair_values(self):
        """Get Crosshair mode specific values from CrosshairWidget

        return: dict of Crosshair key value pairs
        """
        CH_dict = {}
        CH_dict["DeltaE"] = self.view.CW.DeltaE_edit.text()
        CH_dict["modQ"] = self.view.CW.modQ_edit.text()
        return CH_dict

    def set_PlotWidget_values(self):
        """Pass through intensity matrix into plot in view"""
        pass

    def handle_field_values_update(self, field_values):
        """Save the values in the model"""
        section = field_values["name"]
        data = field_values["data"]
        if section == "crosshair":
            self.model.save_crosshair_data(data)
        elif section == "experiment":
            self.model.save_experiment_data(
                float(data["Ei"]), float(data["S2"]), float(data["alpha_p"]), data["plot_type"]
            )
        else:
            self.model.save_sc_data(data)

    def handle_switch_to_powder(self):
        """Switch to Powder mode"""
        # update the fields' visibility
        self.view.field_visibility_in_Powder()

        # get the valid values for all saved fields
        # if the view contains an invalid value it is overwritten
        saved_values = self.model.get_experiment_data()
        self.view.EW.set_values(saved_values)
        print("view updated with: ", saved_values)
