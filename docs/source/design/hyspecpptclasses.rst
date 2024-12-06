.. _hyspecpptclasses:

Model-View-Presenter
######################




HyspecPPT Model
+++++++++++++++

The HyspecPPTModel encapsulates the backend functionality. It maintains one object: sample (Sample) that has all the valid values. The object fields are updated
every time there are new valid values received from the user (front end).

.. mermaid::

 classDiagram
    HyspecPPTModel <|-- Sample
    Sample "1" -->"1" CrosshairParameters
    CrosshairParameters "1" -->"1" SingleCrystalParameters


    class HyspecPPTModel{
        +Sample sample
    }

    class Sample{
        +float incident_energy_e
        +float detector_tank_angle_s
        +float polarization_direction_angle_p
        +enum 'PlotType' plot_type
        +CrosshairParameters cr_parameters
        +calculate_graph_data(incident_energy_e:float, detector_tank_angle_s:float,polarization_direction_angle_p:float,plot_type:str)
        +store_data(incident_energy_e:float, detector_tank_angle_s:float,polarization_direction_angle_p:float,plot_type:str)
        -get_emin(delta_e, incident_energy_e)
    }


    class CrosshairParameters{
        +enum 'SampleType' current_sample_type
        +float delta_e
        +float mod_q
        +SingleCrystalParameters sc_parameters
        +calculate_crosshair(current_sample_type:str, delta_e:float, mod_q:float, sc_parameters:dict)
        +get_qmod()
        +store_data(current_sample_type:str, delta_e:float, mod_q:float, sc_parameters:dictr)
        +set_sample_type(sample_type:str)
        +update_sample_type_return_qmod(sample_type:str)
        +update_sc_return_qmod(sc_data: dict)
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
        +get_parameters()
        +set_parameters()
    }

Sample Settings
----------------

The parameters' default values for the Sample object are stored in a file, e.g sample_settings.py, next to the model file. They are imported
in the HyspecPPT Model file and used during the Sample object's initialization and data calculations. The options for sample and plot types are used in HyspecPPT Model and View files.
More specifically the parameters with their values are:

    * sample type options
        .. code-block:: bash

            class SampleType(Enum):
                POWDER = "Powder"
                SINGLECRYSTAL = "Single Crystal"
    * plot type options
        .. code-block:: bash

            class PlotType(Enum):
                ALPHA = "alpha_s"
                COSALPHA = "cos^2(alpha_s)"
                COSALPHAPLUS1 = "1+cos^2(alpha_s))/2"
    * default_sample_type = SampleType.POWDER
    * default_plot_type = PlotType.COS_2_ALPHA_S
    * incident_energy_e = 20
    * detector_tank_angle_s = 30
    * polarization_direction_angle_p = 0
    * delta_e = 0
    * mod_q = 0
    * lattice_a = 1
    * lattice_b = 1
    * lattice_c = 1
    * lattice_alpha = 90
    * lattice_beta = 90
    * lattice_gamma = 90
    * lattice_unit_h = 0
    * lattice_unit_k = 0
    * lattice_unit_l = 0
    * number_of_pixels = 200

Functions
-------------

The function signatures and description are included below.

**-- Sample**

* def calculate_graph_data(incident_energy_e:float, detector_tank_angle_s:float,polarization_direction_angle_p:float,plot_type:str) --> dict : The function receives data parameters, updates the sample object's field values and calculates and returns the plot data.

    Internally store_data() is called to store the parameters. The returned data dictionary needed for the plot has the following format:

     .. code-block:: bash

        {
            "q_min": [], //1-d array
            "q_max": [], //1-d array
            "energy_transfer" : [], //1-d array
            "q2d" :[[],], //2-d array
            "e2d" :[[],], //2-d array
            "scharpf_angle" :[[],], //2-d array
        }

* def store_data(incident_energy_e:float, detector_tank_angle_s:float,polarization_direction_angle_p:float,plot_type:str) --> None : The function receives data parameters and updates the sample object's field values.
* def get_emin(delta_e:float, incident_energy_e:float) --> float : The function returns the e_min value, based on delta_e and incident_energy_e. If delta_e < -incident_energy_e, then e_min =1.2* delta_e, else e_min = delta_e.

The get_emin is only used internally in the Sample Model.


**-- CrosshairParameters**

* def calculate_crosshair(current_sample_type:str, delta_e:float, mod_q:float, sc_parameters:dict) --> dict : The function returns the crosshair values. For the SingleCrystal mode it calculates the eline and qline from the sc_parameters. For Powder, it returns delta_e and qmod as eline and qline respectively. The single crystal parameters dictionary have the following format

     .. code-block:: bash

        {
            "sc_parameters" :
            {
                "lattice_a":<a>,
                "lattice_b":<b>,
                "lattice_c":<c>,
                "lattice_alpha":<alpha>,
                "lattice_beta":<beta>,
                "lattice_gamma":<gamma>,
                "lattice_unit_h":<h>,
                "lattice_unit_k":<k>,
                "lattice_unit_l":<l>
            }
        }

    Internally store_data() is called to store the parameters, and get_qmod() is called to find qmod values respectively.
    The following format is returned:

     .. code-block:: bash

        {
            eline: list[float], // 2 values in the list
            qline:list[float] // 2 values in the list
        }

* def get_qmod() --> float :  The function returns qmod. It calculates the value from the sc_parameters (SingleCrystal mode). It returns the qmod field for Powder.
* def set_sample_type(sample_type:str) --> None :  The function sets the current_sample_type from the sample_type parameter
* def store_data(current_sample_type:str, delta_e:float, mod_q:float, sc_parameters:dict) --> None : The function receives data parameters and updates the CrosshairParameters and Single Crystal object's field values e.g.:

    .. code-block:: bash

        {
            "current_sample_type": "SingleCrystal",
            "delta_e": <d_e>,
            "mod_q" : <m_q>,
            "sc_parameters" :
            {
                "lattice_a":<a>,
                "lattice_b":<b>,
                "lattice_c":<c>,
                "lattice_alpha":<alpha>,
                "lattice_beta":<beta>,
                "lattice_gamma":<gamma>,
                "lattice_unit_h":<h>,
                "lattice_unit_k":<k>,
                "lattice_unit_l":<l>
            }
        }

    In case of Powder mode the sc_parameters are not populated/included in the data dictionary and the sc_parameters is ignored for model data update e.g.:

     .. code-block:: bash

        {
            "current_sample_type": "Powder",
            "delta_e": <d_e>,
            "mod_q" : <m_q>,
            "sc_parameters" : {}
        }

* def update_sample_type_return_qmod(sample_type:str) --> float :  The function updates the sample_type value and returns qmod (get_qmod)
* def update_sc_return_qmod(sc_data: dict) --> float :  The function updates the SingleCrystalParameters and returns qmod (get_qmod)

**-- SingleCrystalParameters**

* def set_parameters(sc_data: dict) --> None : The function updates the SingleCrystalParameters with the sc_data, provided in the following format e.g:

     .. code-block:: bash

        {
            "lattice_a":<a>,
            "lattice_b":<b>,
            "lattice_c":<c>,
            "lattice_alpha":<alpha>,
            "lattice_beta":<beta>,
            "lattice_gamma":<gamma>,
            "lattice_unit_h":<h>,
            "lattice_unit_k":<k>,
            "lattice_unit_l":<l>
        }

* def get_parameters() --> dict : The function returns a dictionary with the SingleCrystalParameters field values.

     .. code-block:: bash

        {
            "lattice_a":<a>,
            "lattice_b":<b>,
            "lattice_c":<c>,
            "lattice_alpha":<alpha>,
            "lattice_beta":<beta>,
            "lattice_gamma":<gamma>,
            "lattice_unit_h":<h>,
            "lattice_unit_k":<k>,
            "lattice_unit_l":<l>
        }

The data structure is the same in set_parameters() and get_parameters() for consistency.



HyspecPPT View
+++++++++++++++


.. mermaid::

 classDiagram
    HyspecPPTView "1" -->"1" SampleWidget
    SampleWidget "1" -->"1" CrosshairWidget
    CrosshairWidget "1" -->"1" SingleCrystalParametersWidget

    class HyspecPPTView{
        +SampleWidget:sample
        +PlotFigure:plot
        +QButton:help_btn
        +update_plot(q_min: list[float],q_max: list[float],energy_transfer: list[float], q2d: list[list[float]],e2d: list[list[float]], scharpf_angle: list[list[float]])
        +update_crosshair(eline: list[float], qline:list[float])

    }

    class SampleWidget{
        +QLabel:ei_display
        +QLineEdit:ei_value
        +QLabel:s2_display
        +QLineEdit:s2_value
        +QLabel:p_display
        +QLineEdit:p_value
        +QLabel:plot_type_display
        +QComboBox:plot_type_value
        +CrosshairWidget:crosshair_parameters
        +validation_status()
        +parameters_update()
        +get_parameters()

    }

    class CrosshairWidget{
        +QLabel:sample_type_display
        +QRadioButton:sample_type_value
        +QLabel:delta_e_display
        +QLineEdit:delta_e_value
        +QLabel:qmod_display
        +QLineEdit:qmod_value
        +SingleCrystalParametersWidget:single_crystal_parameters
        +set_sample_options(sample_types:[str])
        +set_plot_options(plot_types:[str])
        +set_qmod(qmod:float)
        +set_qmod_readonly(readonly:bool)
        +toggle_crystal_parameters(show:bool)
        +validation_status()
        +sample_type_update()
        +parameters_update()
        +get_parameters()

    }

    class SingleCrystalParametersWidget{
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


Functions
-------------

The function signatures and description are included below.

**-- HyspecPPTView**

* def update_plot(q_min: list[float],q_max: list[float],energy_transfer: list[float], q2d: list[list[float]],e2d: list[list[float]], scharpf_angle: list[list[float]]) --> None : The function updates the plot with the given parameters.
* def update_crosshair(eline: list[float], qline:list[float]) --> None : The function updates the crosshair lines at the plot with the given parameters.

**-- CrosshairWidget**

* def set_sample_options(sample_types:[str]) --> None : The function sets the Sample options (Single Crystal and Powder) to be used as radio button options during the widget's initialization.
* def set_plot_options(plot_types:[str]) --> None : The function sets the plot type options, e.g. alpha_s, to be used as combobox options during the widget's initialization.
* def set_qmod(qmod:float) --> None: The function sets the mod_q value from qmod parameter.
* def set_qmod_readonly(readonly:bool) --> None : The function sets/unsets the qmod text readonly property based on the readonly flag.
* def sample_type_update() --> None :   The function wraps the Presenter call. Example usage: it is called on sample type radio toggled
* def parameters_update() --> None : The function wraps the Presenter call. Example usage: it is called at every parameter update event.
* def toggle_crystal_parameters(show:bool) --> None : The function hides/shows the SingleCrystalParametersWidget based on the show flag.
* def validation_status() --> Bool : The function checks all the CrosshairWidget's parameters' validation status. It returns True, if and only if all parameters are valid, else False.
* def get_parameters() --> dict : The function packs/returns all parameters in a dictionary format as follows:
     .. code-block:: bash

        {
            "current_sample_type": "Powder",
            "delta_e": <d_e>,
            "mod_q" : <m_q>
        }

**-- SampleWidget**

* def parameters_update() --> None : The function wraps the Presenter call. Example usage: it is called at every parameter update event.
* def validation_status() --> Bool : The function checks all the SampleWidget's parameters' validation status. It returns True, if and only if all parameters are valid, else False.
* def get_parameters() --> dict : The function packs/returns all parameters in a dictionary format as follows:
     .. code-block:: bash

        {
            "incident_energy_e": <e>,
            "detector_tank_angle_s" : <s2>,
            "polarization_direction_angle_p" :<ao>,
            "plot_type" : <g_a>
        }

**-- SingleCrystalParametersWidget**

* def get_parameters() --> dict : The function packs/returns all parameters in a dictionary format as follows:
    .. code-block:: bash

        {
            "lattice_a":<a>,
            "lattice_b":<b>,
            "lattice_c":<c>,
            "lattice_alpha":<alpha>,
            "lattice_beta":<beta>,
            "lattice_gamma":<gamma>,
            "lattice_unit_h":<h>,
            "lattice_unit_k":<k>,
            "lattice_unit_l":<l>
        }

* def set_parameters(parameters: dict) --> None : The functions sets all SingleCrystalParametersWidget's parameters from the dictionary with the following format:
    .. code-block:: bash

        {
            "lattice_a":<a>,
            "lattice_b":<b>,
            "lattice_c":<c>,
            "lattice_alpha":<alpha>,
            "lattice_beta":<beta>,
            "lattice_gamma":<gamma>,
            "lattice_unit_h":<h>,
            "lattice_unit_k":<k>,
            "lattice_unit_l":<l>
        }

    The functions get_parameters() and set_parameters() have the same dictionary format.
* def parameters_update() --> None : The function wraps the Presenter call. Example usage: it is called at every parameter update event.
* def validation_status() --> Bool : The function checks all the parameters' validation status. It returns True, if and only if all parameters are valid, else False.

HyspecPPT Presenter
++++++++++++++++++++++

.. mermaid::

 classDiagram
    HyspecPPTPresenter "1" -->"1" HyspecPPTModel
    HyspecPPTPresenter "1" -->"1" HyspecPPTView

    class HyspecPPTPresenter{
        -HyspecPPTModel:model
        -HyspecPPTView:view
        +sample_parameters_update()
        +crosshair_parameters_update()
        +sample_type_update()
        +sc_parameters_update()
        +get_plot_options()
        +get_sample_type_options()
    }

    class HyspecPPTModel{
        #from above
    }

    class HyspecPPTView{
        #from above
    }

The Presenter describes the main workflows that require communication and coordination between the Model and View through the Presenter. Additionally, it includes 2 functions that retrieves the options  from the settings files for the View.
Any value processing and/or filtering to match the requirements and logic of the View and Model side should happen on the Presenter.

#. Display the available plot types from the settings files: set_plot_options() at the View

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter

            Note over View,Presenter: Application Start - HyspecPPTView Initialization
            View->>Presenter: Get all available plot type options - SampleWidget::get_plot_options()
            Note right of Presenter: get the PlotType Enum from sample_settings file
            Presenter->>View: Return the list of plot types (str)
            Note left of View: Set and display the plot types in the plot_type_value combo box

#. Display the available sample type options from the settings files: set_sample_type_options() at the View

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter

            Note over View,Presenter: Application Start
            View->>Presenter: Get all available sample type options - SampleWidget::get_sample_type_options()
            Note right of Presenter: get the SampleType Enum from sample_settings file
            Presenter->>View: Return the list of sample types (str)
            Note left of View: Set and display the sample types in the sample_type_value radio buttons

#. This describes the sequence of events happening among M-V-P when Sample parameters are updated in order to see a new plot : sample_parameters_update()

    * Valid Status:

        .. mermaid::

            sequenceDiagram
                participant View
                participant Presenter
                participant Model

                Note over View,Model: Plot draw due to any SampleWidget parameter update
                View->>Presenter: User updates a parameter at SampleWidget: ei_value, s2_value, p_value or plot_type_value
                Note right of Presenter: Check the validation status of all SampleWidget parameters (SampleWidget.validation_status)
                Presenter->>View: Gather the SampleWidget parameters (SampleWidget.get_parameters)
                Presenter->>Model: Send the parameters to calculate plot (Sample.calculate_graph_data)
                Note right of Model: Store the ei, s2 p and plot_type in Sample (Sample.store_data internally) and calculate plot data
                Model->>Presenter: Return graph data dictionary
                Presenter->>View: Return graph data (HyspecPPTView.update_plot)
                Note left of View: Draw the plot

    * Invalid Status:

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter
            participant Model

            Note over View,Model: Crosshair update due to any SampleWidget parameter update
            View->>Presenter: User updates a parameter at SampleWidget: ei_value, s2_value, p_value or plot_type_value
            Note right of Presenter: Check the validation status of all SampleWidget parameters (SampleWidget.validation_status)
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
                Note right of Model: Store the current_sample_type, delta_e, mod_q, sc_parameters in Sample (CrosshairParameters.store_data internally) SingleCrystalParameters (SingleCrystalParameters.store_data internally and calculate crosshair
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

#. This describes the sequence of events happening among M-V-P when Crosshair parameter sample_type_value is updated in order to draw crosshair on the plot : sample_type_update().
The presenter checks the value of sample_type_value and splits the workflow as follows

    * Valid Status:

        * sample_type_value is set to Powder

            .. mermaid::

                sequenceDiagram
                    participant View
                    participant Presenter
                    participant Model

                    Note over View,Model: Crosshair draw due to CrosshairWidget sample_type_value update
                    View->>Presenter: User updates sample_type_value to Powder
                    Presenter->>View: Hide the SingleCrystalParametersWidget block (CrosshairWidget.toggle_crystal_parameters) and enable the qmod_value for edit (CrosshairWidget.set_qmod_readonly)
                    Presenter->>View: Gather the CrosshairWidget  parameters (CrosshairWidget.get_parameters)
                    Presenter->>Model: Send the sample type to be saved in the model

        * sample_type_value is set to Single Crystal

            .. mermaid::

                sequenceDiagram
                    participant View
                    participant Presenter
                    participant Model

                    Note over View,Model: Crosshair draw due to CrosshairWidget sample_type_value update
                    View->>Presenter: User updates sample_type_value to Single Crystal
                    Presenter->>View: Show the SingleCrystalParametersWidget block (CrosshairWidget.toggle_crystal_parameters) and disable the qmod_value for edit (CrosshairWidget.set_qmod_readonly)
                    Presenter->>Model: Send the sample type to calculate qmod (CrosshairParameters.update_sample_type_return_qmod)
                    Model->>Presenter: Return qmod and stored CrosshairParameters
                    Presenter->>View: Return qmod (CrosshairWidget.set_qmod), CrosshairParameters.set_parameters()
                    Note left of View: Display the qmod_value
                    Note left of View: Display the CrosshairParameters values
                    Note left of View: crosshair_parameters_update is triggered


    On sample type change, qmod is recalculated based on the CrosshairParameters and SingleCrystalParameters. Thus, if the user's qmod value was invalid, it will be ignored.


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
