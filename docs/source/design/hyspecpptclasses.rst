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
        +calculate_graph_data()
        +get_data()
        +store_data()
        -get_emin(delta_e, incident_energy_e)
        -get_qmod()
        -get_crosshair()
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

-- Sample

* def calculate_graph_data(Dict data) --> Dict : The function receives data parameters, updates the sample object's field values and calculates and returns the plot data. The incoming data have the following format: e.g.
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

    The data structure is similar to the ones used in get_data() and set_data() for consistency.
    Internally store_data() is called to store the parameters, and get_qmod() and get_crosshair are called to find qmod and crosshair values respectively.
    The data dictionary created for the plot have the  following format:

     .. code-block:: bash

        {
            "q_min": [], //1-d array
            "q_max": [], //1-d array
            "energy_transfer" : [], //1-d array
            "q2d" :[[],], //2-d array
            "e2d" :[[],], //2-d array
            "scharpf_angle" :[[],], //2-d array
            "crosshair": { "x": <>, "y":<>}
        }

* def get_data() --> Dict : The function returns all the sample's parameters in a dictionary format regardless the of the sample type e.g:

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

* def store_data(Dict data) --> None : The function receives data parameters and updates the sample object's field values. The dictionary format is similar to get_data return value e.g.:

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


* get_emin(delta_e, incident_energy_e) --> float : The function returns the e_min value, based on delta_e and incident_energy_e. If delta_e < -incident_energy_e, then e_min =1.2* delta_e, else e_min = delta_e.
* get_qmod() --> float :  The function returns qmod. It calculates the value from the sc_parameters (SingleCrystal mode). It returns the qmod field for Powder.
* get_crosshair() --> dict : The function returns the crosshair x and y float values from the sc_parameters (SingleCrystal mode). It returns delta_e and qmod as x and y respectively for Powder.
  The following format is returned:

     .. code-block:: bash

        {
            "x": <x>,
            "y": <y>
        }


The get_emin and get_qmod functions are only used internally in the Sample Model.

-- SingleCrystalParameters

* def get_parameters(dict sc_data) --> None : The function updates the SingleCrystalParameters with the sc_data, provided in the following format e.g:

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

* def set_parameters() --> Dict : The function returns a dictionary with the SingleCrystalParameters field values.

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
    SampleWidget "1" -->"1" SingleCrystalParameters

    class HyspecPPTView{
        +SampleWidget:sample
        +PlotFigure:plot
        +QButton:help_btn
        +update_plot()
    }

    class SampleWidget{
        +Signal'dict' changed
        +QLabel:ei_display
        +QLineEdit:ei_value
        +QLabel:s2_display
        +QLineEdit:s2_value
        +QLabel:p_display
        +QLineEdit:p_value
        +QLabel:sample_type_display
        +QRadioButton:sample_type_value
        +QLabel:delta_e_display
        +QLineEdit:delta_e_value
        +QLabel:qmod_display
        +QLineEdit:qmod_value
        +QLabel:plot_type_display
        +QComboBox:plot_type_value
        +SingleCrystalParameters:single_crystal_parameters
        +get_plot_options() //from the file - init
        +get_sample_type_options() //from the file - init
        +check_parameters_and_send_data() // on every text editingFinished, combobox currentIndexChanged and radio toggled
        +toggle_crystal_parameters()
        +validation_status()
    }

    class SingleCrystalParameters{
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
        +set_parameters(dict parameters)
        +check_parameters_and_sample() // triggered by every sc parameter text textEdited event
        +validation_status()
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
        +update_plot()
        +update_qmod()
    }

    class HyspecPPTModel{
        #from above
    }

    class HyspecPPTView{
        #from above
    }
