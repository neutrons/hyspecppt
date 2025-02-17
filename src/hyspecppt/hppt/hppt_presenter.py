"""Presenter for the Main tab"""

from .experiment_settings import PLOT_TYPES


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

        # populate fields
        self.view.sc_widget.set_values(self.model.get_single_crystal_data())
        self.view.experiment_widget.initializeCombo(PLOT_TYPES)
        self.view.experiment_widget.set_values(self.model.get_experiment_data())

        # set default selection mode from the model
        experiment_type = self.view.selection_widget.powder_label
        if self.model.cp.get_experiment_type().startswith("single"):
            experiment_type = self.view.selection_widget.sc_label
        self.view.selection_widget.selector_init(experiment_type)  # pass the default mode from experiment type

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
            experiment_type_label = self.view.selection_widget.get_selected_mode_label()
            experiment_type = "powder"
            if experiment_type_label.startswith("Single"):
                experiment_type = "single_crystal"
            # check whether we need to replot - new deltae
            replot = self.model.check_plot_update(float(data["DeltaE"]))
            # update crosshair
            self.model.set_crosshair_data(
                current_experiment_type=experiment_type, DeltaE=float(data["DeltaE"]), modQ=float(data["modQ"])
            )
            if replot:
                # update the heatmap
                plot_data = self.model.calculate_graph_data()
                self.view.plot_widget.update_plot(
                    q_min=plot_data["Q_low"],
                    q_max=plot_data["Q_hi"],
                    energy_transfer=plot_data["E"],
                    q2d=plot_data["Q2d"],
                    e2d=plot_data["E2d"],
                    scharpf_angle=plot_data["intensity"],
                    plot_label=plot_data["plot_type"],
                )
            # update the plot crosshair, if valid values are passed from the model; could be invalid q
            self.view.plot_widget.update_crosshair(eline=data["DeltaE"], qline=data["modQ"])

        elif section == "experiment":
            self.model.set_experiment_data(
                float(data["Ei"]), float(data["S2"]), float(data["alpha_p"]), data["plot_type"]
            )

            # update the heatmap, if valid values are passed
            plot_data = self.model.calculate_graph_data()
            self.view.plot_widget.update_plot(
                q_min=plot_data["Q_low"],
                q_max=plot_data["Q_hi"],
                energy_transfer=plot_data["E"],
                q2d=plot_data["Q2d"],
                e2d=plot_data["E2d"],
                scharpf_angle=plot_data["intensity"],
                plot_label=plot_data["plot_type"],
            )

        else:
            self.model.set_single_crystal_data(data)
            # update newly calculated qmod
            # get the valid values for crosshair saved fields
            # if the view contains an invalid value it is overwritten
            saved_values = self.model.get_crosshair_data()
            self.view.crosshair_widget.set_values(saved_values)
            # update the plot crosshair, if valid values are passed from the model; could be invalid q
            if self.view.crosshair_widget.validation_status_all_inputs():
                self.view.plot_widget.update_crosshair(eline=saved_values["DeltaE"], qline=saved_values["modQ"])

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
        self.view.crosshair_widget.set_values(saved_values)
        # update the plot crosshair
        self.view.plot_widget.update_crosshair(eline=saved_values["DeltaE"], qline=saved_values["modQ"])

        # update view values
        saved_values = self.model.get_experiment_data()
        self.view.experiment_widget.set_values(saved_values)

    def handle_switch_to_sc(self):
        """Switch to Single Crystal mode"""
        # update the fields' visibility
        self.view.field_visibility_in_SC()
        # update the experiment type in the model
        experiment_type = "single_crystal"
        self.model.set_crosshair_data(current_experiment_type=experiment_type)

        # get the valid values for crosshair saved fields
        # if the view contains an invalid value, except from calculated q, it is overwritten
        saved_values = self.model.get_crosshair_data()
        self.view.crosshair_widget.set_values(saved_values)
        # update the plot crosshair, if valid values are passed from the model; could be invalid q
        if self.view.crosshair_widget.validation_status_all_inputs():
            self.view.plot_widget.update_crosshair(eline=saved_values["DeltaE"], qline=saved_values["modQ"])

        # get the valid values for experiment saved fields
        # if the view contains an invalid value it is overwritten
        saved_values = self.model.get_experiment_data()
        self.view.experiment_widget.set_values(saved_values)

        # get the valid values for single crystal saved fields
        # if the view contains an invalid value it is overwritten
        saved_values = self.model.get_single_crystal_data()
        self.view.sc_widget.set_values(saved_values)
