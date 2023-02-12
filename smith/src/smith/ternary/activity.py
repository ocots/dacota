# Projet SMITH 2020, transcription depuis getExtremities.m le 03/02/20

import numpy as np

import smith


def nrtl(A, alpha, R=None):
    r"""
    The function ``nrtl`` returns the set of constants of the activity coefficients of a given ternary mixture.


    Parameters
    ----------

    A : 3x3 array
        the matrix of binary interaction coefficients

    alpha : 3x3 array
            the symmetric matrix of non-randomness parameters

    R   : float
        ...

    Returns
    -------

    activity['name'] : str
        the name of the vapor pressure model (``antoine`` by default)

    activity['A'] : 3x3 array
        the matrix of binary interaction coefficients

    activity['alpha'] : 3x3 array
        the symmetric matrix of non-randomness parameters

    activity['R'] : float
        the ideal gaz constant


    Warning
    -------
    The units of the element of matrices ``A_bar`` and ``alpha`` must agree with the units of the ideal gaz constant :math:`R`.
    By default, R = ``1.9872042586`` Cal/(K.mol).

    See Also
    --------

    smith.ternary.pressure() for the vapor pressure constants
    """

    # Tests on input variables
    if R is None:
        R = smith.tools.getR()

    activity = {
        "name": "NRTL",
        "A": np.asarray(A),
        "alpha": np.asarray(alpha),
        "R": R,
    }

    return activity


def uniquac(A, r, q, Qp, z, R=None):
    r"""
    The function ``uniquac`` returns the set of constants of the activity coefficients of a given ternary mixture.


    Parameters
    ----------

    A : 3x3 array
        the matrix of binary interaction coefficients

    r :

    q :

    q_prim :

    z   : float
        ...

    Returns
    -------

    activity['name'] : str
        the name of the model (``uniquac`` by default)

    activity['A'] : 3x3 array
        the matrix of binary interaction coefficients

    activity['r'] : 3x3 array
        the vector ...

    activity['q'] : 3x3 array
        the vector ...

    activity['Qp'] : 3x3 array
        the vector ...

    activity['z'] : float
        the ideal gaz constant


    Warning
    -------
    The units of the element of matrices ``A`` must agree with the units of the ideal gaz constant :math:`R`.
    By default, R = ``1.9872042586`` Cal/(K.mol).

    See Also
    --------

    smith.ternary.pressure() for the vapor pressure constants
    """

    # Tests on input variables
    if R is None:
        R = smith.tools.getR()

    activity = {
        "name": "UNIQUAC",
        "A": np.asarray(A),
        "r": np.asarray(r),
        "q": np.asarray(q),
        "Qp": np.asarray(Qp),
        "z": z,
        "R": R,
    }
    return activity
