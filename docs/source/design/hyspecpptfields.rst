.. _hyspecpptfields:

===============================
Fields and Validation for Plot
===============================

The main functionality of the tool is to display a plot, based on the filled in parameters, automatically; no plot button exists

Overall, users can:
   * plot from Powder
   * plot from Single Crystal
   * click on "Help" button that opens up a readthedocs user documentation

Fields
--------

Below are the fields of SingleCrystal and Powder Models

.. list-table:: Common Fields
  :header-rows: 1

  * - Field
    - Type
    - Value Origin
    - Additional validation
    - Mandatory
  * - Polarization Type
    - String
    - predefined choices:["Powder", "Single Crystal"]
    -
    - yes
  * - Ei (Incident Energy) - meV
    - Double
    -
    - 1 < Ei < 100
    - yes
  * - S2 (HYSPEC Detector Tank Angle)
    - String
    -
    - 30<=P<=90
    - yes
  * - P (Polarization Direction Angle)
    - Double
    -
    - -90<=P<=90
    - yes
  * - Delta E
    - Double
    -
    - Ei - DeltaE ≥ -Ei
    - no
  * - mod Q (\|Q\|)
    - Double
    -
    -
    - no
  * - Plot Type
    - String
    - predefined choices:["cos^2(alpha)", "(1+cos^2alpha)/2"]
    -
    - yes


Below are the additional fields of SingleCrystal Model


.. list-table:: Single Crystal Model Additional Fields
  :header-rows: 1

  * - Field
    - Type
    - Default
    - Additional validation
    - Mandatory
  * - a
    - Double
    -
    - 1 < a < 100
    - yes
  * - b
    - Double
    -
    - 1 < b < 100
    - yes
  * - c
    - Double
    -
    - 1 < c < 100
    - yes
  * - alpha
    - Double
    -
    - 45 < alpha < 135
    - yes
  * - beta
    - Double
    -
    - 45 < beta < 135
    - yes
  * - gamma
    - Double
    -
    - 45 < gamma < 135
    - yes
  * - H
    - Double
    -
    -
    - yes
  * - K
    - Double
    -
    -
    - yes
  * - L
    - Double
    -
    -
    - yes



Inter-Field Validations
------------------------

Polarization Type:
  * If Polarization Type set to "Single Crystal", all parameters of Single Crystal block are required. The valid default/model-stored values are set at the appropriate fields.
  * If Polarization Type set to "Powder", all parameters of Single Crystal block are hidden and not required. The valid default/model-stored values are set at the appropriate fields.

modQ (\|Q\|):
  * If Polarization Type set to "Single Crystal", it is a read-only field. The value is returned from the backend after all Single crystal parameters are filled in.
  * If Polarization Type set to "Powder", user can fill the value in.

Delta E - Ei:
  * If and only if  Ei - DeltaE ≥ -Ei, the Delta E value is valid. Else the DeltaE is set to -Ei and the related parameters are recalculated, too


Validation
----------

Regarding validation, if all fields are valid, then the front end triggers the backend to send the current parameters and receive the new data and plot the graph.


Front end side validation can include:
   * required fields
   * field types
   * threshold limits: Ei, P, deltaE and crystal parameters; qt validators can be used


Backend side validation can include:
  * qmod calculation
  * graph data calculations
  * update DeltaE and related parameters
