# Projet smith 2020.

import numpy as np

import smith


def antoine(component_1, component_2):
    r"""
    The function ``antoine`` rearranges the constants :math:`a_i, b_i, c_i` of Antoine's equation

        .. math::

           \log_{10}P_i^{sat}=a_i-\frac{b_i}{T+c_i}, \quad i=1,2


    for the compounds of a binary mixture in a given order and defines the ambient pressure constant :math:`P^0`.

    Parameters
    ----------

    component_i : array
                          the vector :math:`(a_i, b_i, c_i)` of the the Antoine equation constants of i-th compound, i=1,2

    options : dictionary
              computational options. Default value: ``Non``


    Returns
    -------

        pressure.name : str
                       the name of the vapor pressure model (`antoine` by default),

        pressure.1 : array
                     the vector :math:`(a_1, a_2, 0)`

        pressure.2 : array
                     the vector :math:`(b_1, b_2, 0)`

        pressure.3 : array
                     the vector :math:`(c_1, c_2, 0)`

        pressure.P0 : float
                    the ambient pressure constant


    Warning
    -------
    1. The values of the Antoine equation constants :math:`a_i, b_i, c_i` must agree with the units for the ambient pressure
    :math:`P0` (mmHg, Pa, etc.) and the temperature :math:`T` (°C, K, etc.) . By default, it is assumed that the temperature
    in Antoine's equation is measured in °C and P0= ``760`` mmHg.

    2. This function uses a dummy third compound.


    See Also
    --------

    smith.binary.activity() for the activity coefficients parameters
    """

    component_1 = np.asarray(component_1)
    component_2 = np.asarray(component_2)
    component_3 = np.asarray([0.0, 0.0, 0.0])

    antoineA = [component_1[0], component_2[0], component_3[0]]
    antoineB = [component_1[1], component_2[1], component_3[1]]
    antoineC = [component_1[2], component_2[2], component_3[2]]

    pressure = {
        "name": "antoine",
        "1": np.asarray(antoineA),
        "2": np.asarray(antoineB),
        "3": np.asarray(antoineC),
    }

    return pressure
