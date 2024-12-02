.. _hyspecpptclasses:

Model-View-Presenter
=====================



HyspecPPT Model
----------------

.. mermaid::

 classDiagram
    HyspecPPTModel <|-- SingleCrystalModel
    HyspecPPTModel <|-- PowderModel


    class HyspecPPTModel{
        <<Abstract>>
        +Double incident_energy_e
        +Double detector_tank_angle_s
        +Double polarization_direction_angle_p
        +Double delta_e
        +Double mod_q
        +Option graph_type
        +calculate_graph_data()
        +get_model_data()
        +store_data()

    }

    class SingleCrystalModel{
        +Double single_crystal_a
        +Double single_crystal_b
        +Double single_crystal_c
        +Double single_crystal_alpha
        +Double single_crystal_beta
        +Double single_crystal_gamma
        +String single_crystal_h
        +String single_crystal_k
        +String single_crystal_l
        +calculate_qmod()
        +get_single_crystal_data()
    }

    class PowderModel{
        <>
    }



HyspecPPT View
---------------

.. mermaid::

 classDiagram
    HyspecPPTView "1" -->"1" SingleCrystalParameters

    class HyspecPPTView{
        -Signal~str~:error_message_signal
        -Signal~str~:update

        +QLabel:ei_display
        +QLineEdit:ei_value
        +QLabel:s2_display
        +QLineEdit:s2_value
        +QLabel:p_display
        +QLineEdit:p_value
        +QLabel:pol_type_display
        +QRadioButton:pol_type_value
        +QLabel:delta_e_display
        +QLineEdit:delta_e_value
        +QLabel:qmod_display
        +QLineEdit:qmod_value
        +QLabel:graph_type_display
        +QComboBox:graph_type_value
        +SingleCrystalParameters:single_crystal_parameters
        +PlotFigure:plot
        +QButton:help_btn
        +send_error_message()
        -show_error_message()
        //+QStatusBar:status_bar
        +get_stored_data()
        +store_data_and_update_plot()
        +show_hide_cystal_parameters()
        +validate_delta_ei()
    }


    class SingleCrystalParameters{
        -Signal~str~:update
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
        +update_qmod()
        +send_parameters()
    }


HyspecPPT Presenter
--------------------

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
