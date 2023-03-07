# Projet alcos 2017, transcription depuis getExtremities.m le 03/02/20

import numpy as np
import smith


def nrtl(a12, a21, alpha, R=None):
    r"""

    The function ``nrtl`` returns the set of constants of the activity coefficients of a given binary mixture.


    Parameters
    ----------

    A : 3x3 array
        the matrix of binary interaction coefficients

    alpha : 3x3 array
        the symmetric matrix of non-randomness parameters

    R : float
        ...


    Returns
    -------

    activity.name : str
        the name of the vapor pressure model (`antoine` by default)

    activity.A : 3x3 array
        the 3x3 matrix of binary interaction coefficients

    activity.alpha:  3x3 array
        the 3x3 symmetric matrix of non-randomness parameters

    activity.R : float
        the ideal gaz constant


    Warning
    -------

    1. The units of the element of matrices ``A_bar`` and ``alpha`` must agree with the units of the ideal gaz constant
    :math:`R`. By default, R = ``1.9872042586`` Cal/(K.mol).

    2. This function uses a dummy third compound with zero values of all constants. The only non-trivial values are
    :math:`a_{12},\;a_{21}, \; \alpha_{12}`.  They describe the interaction coefficients and the non-randomness parameter between the 1st en the 2nd compounds.


    See Also
    --------

    smith.ternary.pressure() for the vapor pressure constants
    """

    if R is None:
        R = smith.tools.getR()

    A = np.array([[0, a12, 0], [a21, 0, 0], [0, 0, 0]])
    Alpha = np.array([[0.0, alpha, 0.0], [alpha, 0.0, 0.0], [0.0, 0.0, 0.0]])

    activity = {"name": "NRTL", "A": A, "alpha": Alpha, "R": R}

    return activity
