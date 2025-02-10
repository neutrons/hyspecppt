.. _hyspecpptclasses:

Model-View-Presenter
######################

The software is organized in a Model-View-Presenter pattern.
The main (HyspecPPT) models, view and presenter classes and their components interactions are described here.


HyspecPPT Model
+++++++++++++++

The HyspecPPTModel encapsulates the backend functionality. The object fields are updated
every time there are new valid values received from the user (front end).

.. mermaid::

 classDiagram
    HyspecPPTModel "1" -->"1" CrosshairParameters
    CrosshairParameters "1" -->"1" SingleCrystalParameters

    class HyspecPPTModel{
        +float incident_energy_e
        +float detector_tank_angle_s
        +float polarization_direction_angle_p
        +enum 'PlotType' plot_type
        +CrosshairParameters cr_parameters
        +set_single_crystal_data(params: dict[str, float])
        +get_single_crystal_data()
        +set_crosshair_data(current_experiment_type: str, DeltaE: float = None, modQ: float = None)
        +get_crosshair_data()
        +set_experiment_data(Ei: float, S2: float, alpha_p: float, plot_type: str)
        +get_experiment_data()
        +check_plot_update(deltaE)
        +calculate_graph_data()
    }


    class CrosshairParameters{
        +float delta_e
        +float mod_q
        +SingleCrystalParameters sc_parameters
        +set_crosshair(current_experiment_type: str, DeltaE: float = None, modQ: float = None)
        +get_crosshair()
        +get_experiment_type()
    }

    class SingleCrystalParameters{
        +float lattice_a
        +float lattice_b
        +float lattice_c
        +float lattice_alpha
        +float lattice_beta
        +float lattice_gamma
        +float lattice_unit_h
        +float lattice_unit_k
        +float lattice_unit_l
        +set_parameters(params: dict[str, float])
        +get_parameters()
        +calculate_modQ()
    }

Experiment Settings
--------------------

The parameters' default values for the application are stored in a file, experiment_settings.py, next to the model file. They are imported
in the HyspecPPT Model file and used during the Experiment object's initialization and data calculations. The options for experiment and plot types are used in HyspecPPT Model and View files.
More specifically the parameters with their values are:

    * Experiment type options
        .. code-block:: bash

            class ExperimentType(Enum):
                POWDER = "Powder"
                SINGLECRYSTAL = "Single Crystal"
    * plot type options
        .. code-block:: bash

            class PlotType(Enum):
                ALPHA = "alpha_s"
                COSALPHA = "cos^2(alpha_s)"
                COSALPHAPLUS1 = "1+cos^2(alpha_s))/2"
    * DEFAULT_MODE:dict =
        * current_experiment_type="single_crystal"
    * DEFAULT_CROSSHAIR: dict =
        * delta_e = 0
        * mod_q = 0
    * DEFAULT_EXPERIMENT:dict =
        * plot_type = PlotType.COS_2_ALPHA_S
        * incident_energy_e = 20
        * detector_tank_angle_s = 30
        * polarization_direction_angle_p = 0
    * DEFAULT_LATTICE:dict =
        * a = 1
        * b = 1
        * c = 1
        * alpha = 90
        * beta = 90
        * gamma = 90
        * h = 0
        * k = 0
        * l = 0
    * MAX_MODQ = 15 -- maximum momentum transfer
    * N_POINTS = 200 -- number of points in the plot
    * TANK_HALF_WIDTH = 30.0 -- tank half-width
    * number_of_pixels = 200



HyspecPPT View
+++++++++++++++


.. mermaid::

 classDiagram
    HyspecPPTView "1" -->"1" ExperimentWidget
    ExperimentWidget "1" -->"1" CrosshairWidget
    CrosshairWidget "1" -->"1" SingleCrystalWidget

    class HyspecPPTView{
        +ExperimentWidget:experiment_widget
        +SingleCrystalWidget:sc_widget
        +CrosshairWidget:crosshair_widget
        +SelectorWidget:selection_widget
        +PlotWidget:plot_widget

    }

    class ExperimentWidget{
        +QLabel:ei_display
        +QLineEdit:ei_value
        +QLabel:S2_display
        +QLineEdit:S2_value
        +QLabel:p_display
        +QLineEdit:p_value
        +QLabel:plot_type_display
        +QComboBox:plot_type_value
        +validation_status()
        +parameters_update()
        +get_parameters()
        +set_parameters(incident_energy_e: float, detector_tank_angle_s:float, polarization_direction_angle_p:float, plot_type:str)

    }

    class CrosshairWidget{
        +QLabel:Eexperiment_type_display
        +QRadioButton:experiment_type_value
        +QLabel:delta_e_display
        +QLineEdit:delta_e_value
        +QLabel:qmod_display
        +QLineEdit:qmod_value
        +set_experiment_options(experiment_types:[str])
        +set_plot_options(plot_types:[str])
        +set_qmod(qmod:float)
        +set_qmod_readonly(readonly:bool)
        +toggle_crystal_parameters(show:bool)
        +validation_status()
        +experiment_type_update()
        +parameters_update()
        +get_parameters()
        +set_parameters(current_experiment_type: str, delta_e:float, delta_e:floatr
    }

    class SingleCrystalWidget{
        +QLabel:a_display
        +QLineEdit:a_value
        +QLabel:b_display
        +QLineEdit:b_value
        +QLabel:c_display
        +QLineEdit:c_value
        +QLabel:alpha_display
        +QLineEdit:alpha_value
        +QLabel:beta_display
        +QLineEdit:beta_value
        +QLabel:gamma_display
        +QLineEdit:gamma_value
        +QLabel:h_display
        +QLineEdit:h_value
        +QLabel:k_display
        +QLineEdit:k_value
        +QLabel:l_display
        +QLineEdit:l_value
        +get_parameters()
        +set_parameters(parameters:dict)
        +validation_status()
        +parameters_update()

    }



HyspecPPT Presenter
++++++++++++++++++++++

.. mermaid::

 classDiagram
    HyspecPPTPresenter "1" -->"1" HyspecPPTModel
    HyspecPPTPresenter "1" -->"1" HyspecPPTView

    class HyspecPPTPresenter{
        -HyspecPPTModel:model
        -HyspecPPTView:view
        +experiment_parameters_update()
        +crosshair_parameters_update()
        +experiment_type_update()
        +sc_parameters_update()
        +get_plot_options()
        +get_experiment_type_options()
    }

    class HyspecPPTModel{
        #from above
    }

    class HyspecPPTView{
        #from above
    }

The Presenter describes the main workflows that require communication and coordination between the Model and View through the Presenter. Additionally, it includes 2 functions that retrieves the options  from the settings files for the View.
Any value processing and/or filtering to match the requirements and logic of the View and Model side should happen on the Presenter.


#. Application Start - HyspecPPTView Initialization. All default values are retrieved from the settings file.

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter

            Note over View,Presenter:  - HyspecPPTView Initialization
            Note right of Presenter: get Experiment parameters from experiment_settings file
            Presenter->>View: Set Experiment parameters (ExperimentWidget.set_parameters)
            Note left of View: Display Experiment parameters values
            Note left of View: experiment_parameters_update is triggered
            Note right of Presenter: get Crosshair parameters from experiment_settings file
            Presenter->>View: Set Crosshair parameters (CrosshairWidget.set_parameters)
            Note left of View: Display Crosshair parameters values
            Note right of Presenter: get SingleCrystal parameters from experiment_settings file
            Presenter->>View: Set SingleCrystal parameters (SingleCrystalWidget.set_parameters)
            Note left of View: Display SingleCrystal parameters values
            Note left of View: crosshair_parameters_update is triggered



#. Display the available plot types from the settings files: set_plot_options() at the View

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter

            Note over View,Presenter: Application Start - HyspecPPTView Initialization
            View->>Presenter: Get all available plot type options - ExperimentWidget::get_plot_options()
            Note right of Presenter: get the PlotType Enum from experiment_settings file
            Presenter->>View: Return the list of plot types (str)
            Note left of View: Set and display the plot types in the plot_type_value combo box

#. Display the available experiment type options from the settings files: set_experiment_type_options() at the View

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter

            Note over View,Presenter: Application Start
            View->>Presenter: Get all available experiment type options - ExperimentWidget::get_experiment_type_options()
            Note right of Presenter: get the ExperimentType Enum from experiment_settings file
            Presenter->>View: Return the list of experiment types (str)
            Note left of View: Set and display the experiment types in the experiment_type_value radio buttons

#. This describes the sequence of events happening among M-V-P when Experiment parameters are updated in order to see a new plot : experiment_parameters_update()

    * Valid Status:

        .. mermaid::

            sequenceDiagram
                participant View
                participant Presenter
                participant Model

                Note over View,Model: Plot draw due to any ExperimentWidget parameter update
                View->>Presenter: User updates a parameter at ExperimentWidget: ei_value, s2_value, p_value or plot_type_value
                Note right of Presenter: Check the validation status of all ExperimentWidget parameters (ExperimentWidget.validation_status)
                Presenter->>View: Gather the ExperimentWidget parameters (ExperimentWidget.get_parameters)
                Presenter->>Model: Send the parameters to calculate plot (Experiment.calculate_graph_data)
                Note right of Model: Store the ei, s2 p and plot_type in Experiment (Experiment.store_data internally) and calculate plot data
                Model->>Presenter: Return graph data dictionary
                Presenter->>View: Return graph data (HyspecPPTView.update_plot)
                Note left of View: Draw the plot

    * Invalid Status:

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter
            participant Model

            Note over View,Model: Plot draw due to any ExperimentWidget parameter update
            View->>Presenter: User updates a parameter at ExperimentWidget: ei_value, s2_value, p_value or plot_type_value
            Note right of Presenter: Check the validation status of all ExperimentWidget parameters (ExperimentWidget.validation_status)
            Note right of Presenter: Invalid Status: Nothing

#. This describes the sequence of events happening among M-V-P when Crosshair parameters delta_e_value and qmod_value are updated in order to draw crosshair on the plot : crosshair_parameters_update()

    * Valid Status:

        .. mermaid::

            sequenceDiagram
                participant View
                participant Presenter
                participant Model

                Note over View,Model: Crosshair draw due to CrosshairWidget delta_e_value or qmod_value update
                View->>Presenter: User (or programmatically) updates a parameter at CrosshairWidget: delta_e_value or qmod_value
                Note right of Presenter: Check the validation status of all CrosshairWidget parameters (CrosshairWidget.validation_status)
                Presenter->>View: Gather the CrosshairWidget parameters (CrosshairWidget.get_parameters)
                Presenter->>Model: Send the parameters to calculate crosshair (CrosshairParameters.calculate_crosshair)
                Note right of Model: Store the current_experiment_type, delta_e, mod_q, sc_parameters in CrosshairParameters (CrosshairParameters.store_data internally) SingleCrystalParameters (SingleCrystalParameters.store_data internally and calculate crosshair
                Model->>Presenter: Return crosshair
                Presenter->>View: Return crosshair qline and eline (HyspecPPTView.update_crosshair)
                Note left of View: Display the crosshair on the plot

    * Invalid Status:
        .. mermaid::

            sequenceDiagram
                participant View
                participant Presenter
                participant Model

                Note over View,Model: Crosshair draw due to CrosshairWidget delta_e_value or qmod_value update
                View->>Presenter: User (or programmatically) updates a parameter at CrosshairWidget: delta_e_value or qmod_value
                Note right of Presenter: Check the validation status of all CrosshairWidget parameters (CrosshairWidget.validation_status)
                Note right of Presenter: Invalid Status: Nothing

#. This describes the sequence of events happening among M-V-P when Crosshair parameter experiment_type_value is updated in order to draw crosshair on the plot : experiment_type_update(). The presenter checks the value of experiment_type_value and splits the workflow as follows

    * Valid Status:

        * experiment_type_value is set to Powder

            .. mermaid::

                sequenceDiagram
                    participant View
                    participant Presenter
                    participant Model

                    Note over View,Model: Crosshair draw due to CrosshairWidget experiment_type_value update
                    View->>Presenter: User updates experiment_type_value to Powder
                    Presenter->>View: Gather the CrosshairWidget  parameters (CrosshairWidget.get_parameters)
                    Presenter->>Model: Send the experiment type to be saved in the model
                    Presenter->>View: Hide the SingleCrystalParametersWidget block (CrosshairWidget.toggle_crystal_parameters) and enable the qmod_value for edit (CrosshairWidget.set_qmod_readonly)

        * experiment_type_value is set to Single Crystal

            .. mermaid::

                sequenceDiagram
                    participant View
                    participant Presenter
                    participant Model

                    Note over View,Model: Crosshair draw due to CrosshairWidget experiment_type_value update
                    View->>Presenter: User updates experiment_type_value to Single Crystal
                    Presenter->>Model: Send the experiment type to calculate qmod (CrosshairParameters.update_experiment_type_return_qmod_data)
                    Model->>Presenter: Return qmod and stored CrosshairParameters
                    Presenter->>View: Show the SingleCrystalParametersWidget block (CrosshairWidget.toggle_crystal_parameters) and disable the qmod_value for edit (CrosshairWidget.set_qmod_readonly)
                    Presenter->>View: Return qmod (CrosshairWidget.set_qmod), SingleCrystalParametersWidget.set_parameters()
                    Note left of View: Display the qmod_value
                    Note left of View: Display the SingleCrystalParameters values
                    Note left of View: crosshair_parameters_update is triggered


    On experiment type change, qmod is recalculated based on SingleCrystalParameters for Single Crystal mode. Thus, if the user's qmod value was invalid, it will be ignored.


#. This describes the sequence of events happening among M-V-P when Single Crystal parameters are updated in order to draw crosshair : sc_parameters_update()

    * Valid Status:

        .. mermaid::

            sequenceDiagram
                participant View
                participant Presenter
                participant Model

                Note over View,Model: Crosshair update due to any SingleCrystalParametersWidget parameter update
                View->>Presenter: User updates any parameter at SingleCrystalParametersWidget
                Note right of Presenter: Check the validation status of all SingleCrystalParametersWidget parameters (SingleCrystalParametersWidget.validation_status)
                Presenter->>View: Gather the SingleCrystalParametersWidget parameters (SingleCrystalParametersWidget.get_parameters)
                Presenter->>Model: Send the parameters
                Note right of Model: Update Single CrystalParameters and calculate the qmod value (update_sc_return_qmod)
                Model->>Presenter: Return qmod
                Presenter->>View: Return qmod (CrosshairWidget.set_qmod)
                Note left of View: Display the qmod_value
                Note left of View: crosshair_parameters_update is triggered


    * Invalid Status:

        .. mermaid::

            sequenceDiagram
                participant View
                participant Presenter
                participant Model
                Note over View,Model: Crosshair update due to any SingleCrystalParametersWidget parameter update
                View->>Presenter: User updates any parameter at SingleCrystalParametersWidget
                Note right of Presenter: Check the validation status of all SingleCrystalParametersWidget parameters (SingleCrystalParametersWidget.validation_status)
                Note right of Presenter: Invalid Status: Nothing
