# Projet smith 2020, transcription depuis getExtremities.m le 03/02/20

import numpy as np
from nutopy import nle

from smith.errors import *
from smith.ternary import mod_F3
from smith.ternary.tools import *


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def solve(x0, pressure, activity):
    r"""

    The ``solve`` function computes the ternary azeotropic point (if exists) of a given mixture by finding the zeros of the function``fun``
    by the Newton-Raphson method and using the analytic Jacobian of the ``fun`` function.


    Parameters
    ----------

    x0 : array
         initial  point in the state space: :math:`x_0=(x_1^0, x_2^0, T^0)`, where :math:`x_i,  i=1,2` are the mole fractions of the first
         two compounds and :math:`T` is the boiling temperature of the mixture.

    pressure : dictionary
               contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
               Contains also the ambient pressure constant :math:`P^0`.

    activity : dictionary
               contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
               of the mixture. Contains  also the ideal gaz constant :math:`R`.


    Returns
    -------

    sol.x : array
             the state space coordinates of the azeotropic point or the last computed point if the admissible solution is not found

    sol.f : float
            the norm of the target function (?)

    sol.nfev : ?

    sol.njev : ?

    sol.status : integer
                 solution's flag : -1 if converges to a point outside of the composition triangle :math:`x_1+x_2+x_3=1`, +1 otherwise.

    sol.success : boolean
                  True if converges to the azeotrope, False otherwise

    sol.message : string
                  solution's message


    See Also
    --------

    smith.ternary.azeotrope.fun() for the ternary azeotrope equations
    smith.ternary.azeotrope.jac() for the jacobian of the function ``fun``
    smith.ternary.activity() for the activity coefficients parameters
    smith.ternary.pressure() for the vapor pressure constants

    """

    # Cast of input variables
    if not isinstance(x0, float):
        x0 = np.asarray(x0)

    msg_erreur = "Variable x0 must be a three dimensional array."
    if isinstance(x0, np.ndarray):
        if x0.size != 3:
            raise ArgumentDimensionError(msg_erreur)
    else:
        raise ArgumentTypeError(msg_erreur)
    sol = nle.solve(
        fun,
        x0,
        df=jac,
        args=(
            pressure,
            activity,
        ),
    )

    if sol.x[0] + sol.x[1] > 1 or sol.x[0] + sol.x[1] < 0:
        sol.status = -1
        sol.success = False
        sol.message = "Azeotrope not found"
        return sol
    else:
        return sol


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def fun(x, pressure, activity):
    r"""
    The ``fun`` function returns the function of the form :math:`f : \mathbf{R}^3 \rightarrow \mathbf{R}^3` which defines the left
    hand-side of the ternary azeotrope equations of a given mixture.


    Parameters
    ----------

    x : array
        a point in the state space: :math:`x=(x_1, x_2, T)`, where :math:`x_i,  i=1,2`  are the mole fractions of the first two
        compounds and :math:`T` is the boiling temperature of the mixture.

    pressure : dictionary
               contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
               Contains also the ambient pressure constant :math:`P^0`.

    activity : dictionary
               contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
               of the mixture. Contains  also the ideal gaz constant :math:`R`.


    Returns
    -------

    y : array
        the right-hand sides of the ternary azeotrope equations

        .. math::

            (1-K_i(x_1, x_2, T))x_i = 0, \quad   i=1,2,3


    where :math:`x_i,  i=1,2` are the mole fraction of the first two compounds, :math:`T`
    is the boiling temperature of the mixture, and


         .. math::
             K_i=\frac{\gamma_i(x_1, x_2, T) P^{sat}(T)}{P^0}


    are the distribution coefficients.


    Examples
    --------

    >>> import numpy as np
    >>> from .tools import *
    >>> from . import mod_F3

    See Also
    --------

    smith.ternary.pressure() for the vapor pressure constants
    smith.ternary.activity() for the activity coefficients parameters
    smith.ternary.azeotrope.jac() for the jacobian of the function ``fun``
    smith.ternary.azeotrope.solve() for the resolution of the ternary azeotrope equations


    """

    # Cast of input variables
    if not isinstance(x, float):
        x = np.asarray(x)

    msg_erreur = "Variable x must be a three dimensional array."
    if isinstance(x, np.ndarray):
        if x.size != 3:
            raise ArgumentDimensionError(msg_erreur)
    else:
        raise ArgumentTypeError(msg_erreur)

    (pars_p, pars_g, modelName_p, modelName_g) = set_pars_py_to_fortran(
        pressure, activity
    )

    fun_val = mod_F3.f3(
        x, modelName_p, pars_p, modelName_g, pars_g, pars_p.size, pars_g.size
    )

    return fun_val


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def jac(x, pressure, activity):
    r"""

    The ``jac`` function returns the Jacobian of the function ``fun`` computed by automatic differentiation using  the ``TAPENADE``  library.

    Parameters
    ----------

    x : array
        a point in the state space: :math:`x=(x_1, x_2, T)`, where :math:`x_i,  i=1,2` are the mole fractions of the first two compounds
        and :math:`T` is the boiling temperature of the mixture.

    pressure : dictionary
        contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
        Contains also the ambient pressure constant :math:`P^0`.

    activity : dictionary
        contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
        of the mixture. Contains  also the ideal gaz constant :math:`R`.



    Returns
    -------

    jac:  3x3 array
          the 3x3 Jacobian matrix of the function ``fun``


    See Also
    --------

    smith.ternary.pressure() for the vapor pressure constants
    smith.ternary.activity() for the activity coefficients parameters
    smith.ternary.azeotrope.fun() for the ternary azeotrope equations
    smith.ternary.azeotrope.solve() for the resolution of the ternary azeotrope equations
    """
    # Cast of input variables
    if not isinstance(x, float):
        x = np.asarray(x)

    msg_erreur = "Variable x must be a three dimensional array."
    if isinstance(x, np.ndarray):
        if x.size != 3:
            raise ArgumentDimensionError(msg_erreur)
    else:
        raise ArgumentTypeError(msg_erreur)

    (pars_p, pars_g, modelName_p, modelName_g) = set_pars_py_to_fortran(
        pressure, activity
    )

    jac_val = mod_F3.f3_jac(
        x, modelName_p, pars_p, modelName_g, pars_g, pars_p.size, pars_g.size
    )

    return jac_val
