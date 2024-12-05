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
    Sample "1" -->"1" SingleCrystalParameters


    class HyspecPPTModel{
        +Sample sample
    }

    class Sample{
        +enum 'SampleType' current_sample_type
        +float incident_energy_e
        +float detector_tank_angle_s
        +float polarization_direction_angle_p
        +float delta_e
        +float mod_q
        +enum 'PlotType' plot_type
        +SingleCrystalParameters sc_parameters
        +calculate_graph_data(incident_energy_e:float, detector_tank_angle_s:float,polarization_direction_angle_p:float,plot_type:str)
        +calculate_crosshair(current_sample_type:str, delta_e:float, mod_q:float, sc_parameters:dict)
        +get_data()
        +store_data()
        -get_emin(delta_e, incident_energy_e)
        +get_qmod() //when switching from Powder to Single Crystal ?
        //+update_qmod()
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

    Example usage: when switching from Powder to Single Crystal mode and backend all related parameters

* def get_data() --> dict : The function returns all the sample's parameters in a dictionary format regardless the of the sample type e.g:

    .. code-block:: bash

        {
            "current_sample_type": <sample_type>,
            "incident_energy_e": <e>,
            "detector_tank_angle_s" : <s2>,
            "polarization_direction_angle_p" :<ao>,
            "delta_e": <d_e>,
            "mod_q" : <m_q>,
            "plot_type" : <g_a>,
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

    The function can be called by the Presenter, in order to update the View with the memory-stored values.

* def store_data(data: dict) --> None : The function receives data parameters and updates the sample object's field values. The dictionary format is similar to get_data return value e.g.:

    .. code-block:: bash

        {
            "current_sample_type": "SingleCrystal",
            "incident_energy_e": <e>,
            "detector_tank_angle_s" : <s2>,
            "polarization_direction_angle_p" :<ao>,
            "delta_e": <d_e>,
            "mod_q" : <m_q>,
            "plot_type" : <g_a>,
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
            "incident_energy_e": <e>,
            "detector_tank_angle_s" : <s2>,
            "polarization_direction_angle_p" :<ao>,
            "delta_e": <d_e>,
            "mod_q" : <m_q>,
            "plot_type" : <g_a>,
            "sc_parameters" : {}
        }


* def get_emin(delta_e, incident_energy_e) --> float : The function returns the e_min value, based on delta_e and incident_energy_e. If delta_e < -incident_energy_e, then e_min =1.2* delta_e, else e_min = delta_e.
* def get_qmod() --> float :  The function returns qmod. It calculates the value from the sc_parameters (SingleCrystal mode). It returns the qmod field for Powder.


The get_emin is only used internally in the Sample Model.

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
        +QLabel:plot_type_display
        +QComboBox:plot_type_value
        +SingleCrystalParametersWidget:single_crystal_parameters
        +set_sample_options(sample_types:[str])
        +set_plot_options(plot_types:[str])
        +set_qmod(qmod:float)
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
* def sample_type_update() --> None :   The function wraps the Presenter call. Example usage: it is called on sample type radio toggled
* def parameters_update() --> None : The function wraps the Presenter call. Example usage: it is called at every parameter update event.
* def toggle_crystal_parameters(show:bool) --> None : The function hides/shows the SingleCrystalParametersWidget based on the show flag.
* def validation_status() --> Bool : The function checks all the CrosshairWidget's parameters' validation status. It returns True, if and only if all parameters are valid, else False.
* def get_parameters() --> dict : The function packs/returns all parameters in a dictionary format as follows:
     .. code-block:: bash

        {
            "current_sample_type": "Powder",
            "delta_e": <d_e>,
            "mod_q" : <m_q>,
            "plot_type" : <g_a>,
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
        +update_plot()
        +update_crosshair()
        +get_plot_options()
        +get_sample_type_options()
    }

    class HyspecPPTModel{
        #from above
    }

    class HyspecPPTView{
        #from above
    }

* parameters_update
* sample parameters_update
* sample sample type update
* sc parameters_update

* def check_parameters_and_send_data() --> dict : The function checks the status of all parameters, (validation_status) and if every parameter is valid it packs/returns the parameters in a dictionary. Example usage: on every text editingFinished, and combobox currentIndexChanged

    .. code-block:: bash

        {
            "current_sample_type": <sample_type>,
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

* def check_parameters_and_send_data() --> dict : The function checks the status of all parameters, (validation_status) and if every parameter is valid it packs/returns the parameters in a dictionary. Example usage: on every text editingFinished, and combobox currentIndexChanged
    .. code-block:: bash

        {
            "incident_energy_e": <e>,
            "detector_tank_angle_s" : <s2>,
            "polarization_direction_angle_p" :<ao>,
            "delta_e": <d_e>,
        }

The Presenter describes the 2 main workflows that require communication and coordination between the Model and View through the Presenter. Additionally, it includes 2 functions that retrieves the options  from the settings files for the View.
Any value processing and/or filtering to match the requirements and logic of the View and Model side should happen on the Presenter.

#. Get available plot types from the settings files: get_plot_options()

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter

            Note over View,Presenter: Application Start - HyspecPPTView Initialization
            View->>Presenter: Get all available plot type options - SampleWidget::get_plot_options()
            Note right of Presenter: get the PlotType Enum from sample_settings file
            Presenter->>View: Return the list of plot types (str)
            Note left of View: Display the plot types in the plot_type_value combo box

#. Get available sample type options from the settings files: get_sample_type_options()

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter

            Note over View,Presenter: Application Start - HyspecPPTView Initialization
            View->>Presenter: Get all available sample type options - SampleWidget::get_sample_type_options()
            Note right of Presenter: get the SampleType Enum from sample_settings file
            Presenter->>View: Return the list of sample types (str)
            Note left of View: Display the sample types in the plot_type_value radio buttons

#. This describes the sequence of events happening among M-V-P when Sample parameters (except from sample type) are updated in order to see a new plot : update_plot()

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter
            participant Model

            Note over View,Model: Plot Update due to any Sample parameter (except from sample type) update
            View->>Presenter: User updates a parameter at SampleWidget (except from sample type)
            Note right of Presenter: get the SampleType Enum from sample_settings file
            Presenter->>View: Return the list of sample types (str)
            Note left of View: Display the sample types in the plot_type_value radio buttons

#. This describes the sequence of events happening among M-V-P when Single Crystal parameters are updated in order to see a new plot : update_plot()

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter
            participant Model

            Note over View,Model: Plot Update due to any Single Crystal parameter
            View->>Presenter: User updates a parameter at SingleCrystalWidget
            Note right of Presenter: get the SampleType Enum from sample_settings file
            Presenter->>View: Return the list of sample types (str)
            Note left of View: Display the sample types in the plot_type_value radio buttons


#. This describes the sequence of events happening among M-V-P when only the sample type is updated in order to see a new plot : update_crosshair()  //qmod value field, and sc parameters values block

    .. mermaid::

        sequenceDiagram
            participant View
            participant Presenter
            participant Model

            Note over View,Model: Plot update due to sample type change
            View->>Presenter: User updates the sample_type_value at SampleWidget
            Note right of Presenter: get the SampleType Enum from sample_settings file
            Presenter->>View: Return the list of sample types (str)
            Note left of View: Display the sample types in the plot_type_value radio buttons



Powder: crosshair (x,y lines) are updated from deltaE and Qmod.
If only Qmod is updated, then the crosshair can be updated in the front end. The only thing needed at this point is to store the new Qmod in the model.
if only DeltaE is updated:
* check if the plot data need to redrawned
* redraw the crosshair
in the model split crosshair and plot data calculations
Single Crystal: parameters are responsible only for the mod Q

update_crosshair
update_plot
when switching from Powder to Single Crystal and back, the only thing affected is the (modQ) crosshair. Only mod Q is kept and updated between sample switches
