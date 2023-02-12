# Projet smith 2020.
# Doc fait par N. Shcherbakova juillet 2020

import numpy as np

import smith


def antoine(component_1, component_2, component_3):
    r"""
    The function ``antoine`` rearranges the constants :math:`a_i, b_i, c_i` of Antoine's equation

        .. math::

           \log_{10}P_i^{sat}=a_i-\frac{b_i}{T+c_i}


    for the compounds  of a given ternary mixture : math:`i=1,2,3` in a given order and defines the ambient pressure constant :math:`P^0`.


    Parameters
    ----------

    component_i : array
                          the vector :math:`(a_i, b_i, c_i)` of the the Antoine equation constants of i-th compound, i=1,2,3

    P0 : float
         the ambient pressure constant


    Returns
    -------

    pressure['name'] : str
        the name of the vapor pressure model (``antoine`` by default)

    pressure['1'] : array
        the vector :math:`(a_1, a_2, a_3)`

    pressure['2'] : array
        the vector :math:`(b_1, b_2, b_2)`

    pressure['3'] : array
        the vector :math:`(c_1, c_2, c_3)`

    pressure['P0'] : float
        the ambient pressure constant


    Warning
    -------

    The values of the Antoine equation constants :math:`a_i, b_i, c_i` must agree with the units for the ambient pressure
    :math:`P0` (mmHg, Pa, etc.) and the temperature :math:`T` (°C, K, etc.). By default, it is assumed that the temperature
    in Antoine's equation is measured in °C and P0 = ``760`` mmHg`.


    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters
    """

    #    if P0 is None:
    #        P0 = smith.tools.getP0()

    component_1 = np.asarray(component_1)
    component_2 = np.asarray(component_2)
    component_3 = np.asarray(component_3)

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


def dippr(component_1, component_2, component_3, P0):
    r"""
    The function ``dippr`` rearranges the constants :math:`a_i, b_i, c_i, d_i, e_i` of Dippr's equation

        .. math::

           \lnP_i^{sat}=a_i+\frac{b_i}{T}+c_i*lnT+d_i*T^e


    for the compounds  of a given ternary mixture : math:`i=1,2,3` in a given order and defines the ambient pressure constant :math:`P^0`.


    Parameters
    ----------

    component_i : array
                          the vector :math:`(a_i, b_i, c_i, d-i, e_i)` of the the Dippr equation constants of i-th compound, i=1,2,3

    P0 : float
         the ambient pressure constant


    Returns
    -------

    pressure['name'] : str
        the name of the vapor pressure model (``antoine`` by default)

    pressure['1'] : array
        the vector :math:`(a_1, a_2, a_3)`

    pressure['2'] : array
        the vector :math:`(b_1, b_2, b_2)`

    pressure['3'] : array
        the vector :math:`(c_1, c_2, c_3)`

    pressure['P0'] : float
        the ambient pressure constant


    Warning
    -------

    The values of the Antoine equation constants :math:`a_i, b_i, c_i` must agree with the units for the ambient pressure
    :math:`P0` (mmHg, Pa, etc.) and the temperature :math:`T` (°C, K, etc.). By default, it is assumed that the temperature
    in Antoine's equation is measured in °C and P0 = ``760`` mmHg`.


    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters
    """

    component_1 = np.asarray(component_1)
    component_2 = np.asarray(component_2)
    component_3 = np.asarray(component_3)

    dipprA = [component_1[0], component_2[0], component_3[0]]
    dipprB = [component_1[1], component_2[1], component_3[1]]
    dipprC = [component_1[2], component_2[2], component_3[2]]
    dipprD = [component_1[3], component_2[3], component_3[3]]
    dipprE = [component_1[4], component_2[4], component_3[4]]

    pressure = {
        "name": "dippr",
        "1": np.asarray(dipprA),
        "2": np.asarray(dipprB),
        "3": np.asarray(dipprC),
        "4": np.asarray(dipprD),
        "5": np.asarray(dipprE),
        "P0": P0,
    }

    return pressure
