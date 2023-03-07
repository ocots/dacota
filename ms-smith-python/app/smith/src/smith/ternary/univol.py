# Projet smith 2020, transcription depuis getExtremities.m le 03/02/20

import numpy as np
from nutopy import nle, path
from scipy import optimize
from smith import options
from smith.errors import *
from smith.ternary import curve_interface, extrem
from smith.ternary.tools import *

# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
#
# DIAGRAM
#
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def diagram(pressure, activity, options=None):
    r"""

    The ``diagram`` function returns the complete diagram of univolatility curves for a given mixture


    Parameters
    ----------


    pressure : dictionary
               contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
               Contains also the ambient pressure constant :math:`P^0`.

    activity : dictionary
               contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
               of the mixture. Contans  also the ideal gaz constant :math:`R`.

    options : dictionary
              computational options, default value: ``Non``


    Returns
    -------

    y : list
        the output of all computed univolatility curves


    Examples
    --------
    >>> import numpy as np
    >>> from .tools import *
    >>> from smith import univol


    Example 1:

    >>> def test_diagram(parameters_mixture):
    ...     (parametres, modelName) = set_pars_py_to_fortran(parameters_mixture)
    ...     curves_list = univol.diagram(parametres)


    >>> curves_list = univol.curve(parameters_mixture)
    >>> print(curves_list)


    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters

    smith.ternary.pressure() for the vapor pressure constants

    smith.ternary.univol.extremities() for the complete list of starting (extremity) points for the set of existing univolatility curves
    between i-th and j-th compounds on the given edge of the composition triangle

    smith.ternary.univol.curve() for the computation of a univolatility curve  of index ij starting from the given extremity point
    """

    # Tests on input variables
    if options is None:
        options = Options()

    # 1. get all the extremities
    extremities_list = []

    Temp_min = 0.0
    Temp_max = 1000.0

    edges = [1, 2, 3]
    indices = [[1, 2], [1, 3], [2, 3]]
    (n, m) = np.shape(indices)

    for edge in edges:
        for i in range(0, n):
            indice_i = indices[i][0]
            indice_j = indices[i][1]
            extrems = extremities(
                pressure,
                activity,
                indice_i,
                indice_j,
                edge,
                Temp_min,
                Temp_max,
                options=options,
            )

            if len(extrems) != 0:
                (le, ce) = np.shape(extrems)

                for j in range(0, le):
                    extrem = extrems[j]
                    alpha = extrem[0]
                    tempe = extrem[1]

                    if edge == 1:
                        x1 = 0.0
                        x2 = alpha
                    elif edge == 2:
                        x2 = 0.0
                        x3 = alpha
                        x1 = 1.0 - x3
                    else:
                        x1 = alpha
                        x2 = 1.0 - x1

                    extremity_dict = {
                        "x1": x1,
                        "x2": x2,
                        "T": tempe,
                        "indice_i": indice_i,
                        "indice_j": indice_j,
                        "edge": edge,
                    }
                    extremities_list.append(extremity_dict)

    # 2. Compute all the curves
    curves_list = []

    for extremity_dict in extremities_list:
        x1_init = extremity_dict["x1"]
        x2_init = extremity_dict["x2"]
        temperature_init = extremity_dict["T"]
        indice_i = extremity_dict["indice_i"]
        indice_j = extremity_dict["indice_j"]

        (x1, x2, T) = curve(
            pressure,
            activity,
            x1_init,
            x2_init,
            temperature_init,
            indice_i,
            indice_j,
            options=options,
        )

        edge = extremity_dict["edge"]

        curve_dict = {
            "x1": x1,
            "x2": x2,
            "T": T,
            "i": indice_i,
            "j": indice_j,
            "edge": edge,
        }

        curves_list.append(curve_dict)

        # Set the final point composition
        x1f = x1[-1]
        x2f = x2[-1]
        x3f = 1.0 - x1f - x2f

        if (x1f <= x2f) and (x1f <= x3f):
            edgef = 1  # x1 = 0
        elif (x2f <= x1f) and (x2f <= x3f):
            edgef = 2  # x2 = 0
        else:
            edgef = 3  # x3 = 0

        # Save the final point state coordinates, the indexes of the univolatility compounds and final point edge.

        ef = {
            "x1": x1f,
            "x2": x2f,
            "T": T[-1],
            "indice_i": indice_i,
            "indice_j": indice_j,
            "edge": edgef,
        }

        Tolerance = options.get("TolXMax")
        Wmin = options.get("MaxTolX")

        # Browse the list of extremities and verify if the current final point is in the list, in this case cancel this point from
        # the list in order to avoid the double integration of the same curve
        for ec in extremities_list:
            Wc = error(ef, ec)

            if Wc < Wmin:
                Wmin = Wc
                e = ec

        if Wmin < Tolerance:
            extremities_list.remove(e)
        else:
            raise Error("Problem !")

    return curves_list


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def error(e1, e2, options=None):
    # Tests on input variables
    if options is None:
        options = Options()

    # Test if two extremity points are the same (within the tolerance set in options)
    if (
        (e1["indice_i"] != e2["indice_i"])
        or (e1["indice_j"] != e2["indice_j"])
        or (e1["edge"] != e2["edge"])
    ):
        return options.get("MaxTolX")
    else:
        return np.sqrt(
            (e1["x1"] - e2["x1"]) ** 2
            + (e1["x2"] - e2["x2"]) ** 2
            + (e1["T"] - e2["T"]) ** 2
        )


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
#
# EXTREMITIES
#
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def extremities(
    pressure, activity, indi, indj, edge, Temp_min, Temp_max, options=None
):
    r"""

    The ``extremities`` function returns the complete list of the end-points (extremities) for the set of existing univolatility curves between
    i-th and j-th compounds on the given edge of the composition triangle for the temperatures  :math:`T\in[T_{min}, T_{max}]`.



    Parameters
    ----------

    pressure : dictionary
               contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
               Contains also the ambient pressure constant :math:`P^0`.

    activity : dictionary
               contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
               of the mixture. Contains  also the ideal gaz constant :math:`R`.

    indi : int
           the index of i-th compound

    indj : int
           the index of i-th compound

    edge : int
           the index of the edge of the triangle : 1 for the edge  :math:`x_1=0` ( binary mixture of 2th and 3rd compounds), 2 for the edge
           :math:`x_2=0` (binary mixture of 1st and 3rd compounds), 3 for the edge :math:`x_3=0` (binary mixture of 1st and 2nd compounds)

    Temp_min : float
               the left extremity of the temperature interval

    Temp_max : float
               the right extremity of the temperature interval

    options : dictionary
              computational options, set ``Non`` by default for this function


    Returns
    -------

    y : array
        ???


    Examples
    --------

    >>> import numpy as np
    >>> from .tools import *
    >>> from smith import univol


    Example 1:

    >>> def test_extremities():
    ...     Temp_min    = 0
    ...     Temp_max    = 100
    ...     edge        = 1
    ...     indi    = 1
    ...     indj    = 3
    ...     (parametres, modelName) = set_pars_py_to_fortran(parameters_mixture)
    ...     extremities = univol.extremities(parametres, indice_i, indice_j, edge, Temp_min, Temp_max))
    ...     return extremities

    >>> extremities = univol.extremities(parameters_mixture, indi, indj, edge, Temp_min, Temp_max)
    >>> print(extremities)


    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters

    smith.ternary.pressure() for the vapor pressure constants

    smith.ternary.univol.extremity() for the set of univolatility points between i-th and j-th compounds on the given edge of the composition triangle

    smith.ternary.univol.curve() for the computation of a univolatility curve  of index ij starting from the given extremity point

    smith.ternary.univol.diagram() for the computation of the complete set of all existing  univolatility curves of a given mixture


    """

    # Tests on input variables
    if options is None:
        options = Options()

    verbose = options.get("Display")

    # ...
    extremities = []

    # ...
    #    parameters = parameters_mixture
    (pars_p, pars_g, modelName_p, modelName_g) = set_pars_py_to_fortran(
        pressure, activity
    )

    # ...
    alpha_init = 0.0

    # here alpha is one of the concentration: x1, x2 or x3, depending on the edge
    phi = lambda T, alpha: extrem.phi(
        T,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        alpha,
        pars_p.size,
        pars_g.size,
    )
    psi = lambda T, alpha: extrem.psi(
        T,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        alpha,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )
    ext = lambda x: extrem.extremity(
        x,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )  # y = (alpha, T)

    # here the Jacobian of the function
    jac_phi = lambda T, alpha: extrem.phi_jac(
        T,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        alpha,
        pars_p.size,
        pars_g.size,
    )
    #    jac_psi = lambda T, alpha : extrem.psi_jac(T, modelName, pars, edge, alpha, indi, indj, pars.size)
    jac_ext = lambda x: extrem.extremity_jac(
        x,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )  # y = (alpha, T)

    # get T(alpha=0) such that phi(T(0), 0) = 0
    temp_init = optimize.brentq(
        lambda T: phi(T, alpha_init),
        Temp_min,
        Temp_max,
        disp=True,
        xtol=options.get("TolXMin"),
    )

    # if RuntimeError is True:
    #    raise Error('No initial temperature found.')

    # get psi(T(0), 0)
    psi_val_prec = psi(temp_init, alpha_init)

    # Intializations
    alpha_final = 1.0
    Nstep = options.get("Nsteps")
    alpha_span = np.linspace(alpha_init, alpha_final, Nstep)
    temp = temp_init

    # nle.solve options
    opt = nle.Options(
        SolverMethod="hybrj", Display=verbose, TolX=options.get("TolXMin")
    )

    for i in range(1, Nstep):
        #
        alpha = alpha_span[i]

        # Solve  phi=0 at current point
        sol = nle.solve(phi, temp, df=jac_phi, args=(alpha,), options=opt)
        temp = sol.x

        if not sol.success:
            print("Pb during homotopy!")

        # Test if the function psi() change the sign
        psi_val = psi(temp, alpha)

        # print('alpha = ', alpha)
        # print('temp  = ', temp)
        # print('psi   = ', psi_val)
        # print('---')

        if (
            psi_val * psi_val_prec < 0
        ):  # Detect the intersection of the curves phi=0 and  psi=0 in the state space
            # print('sign has changed')

            # Find the exact intersection point of the curves phi=0 and psi=0 in the state space
            sol = nle.solve(
                ext, np.array([alpha, temp]), df=jac_ext, options=opt
            )
            extremity = sol.x

            if not sol.success:
                print("Pb during computation of the crossing point!")

            extremities.append(list(extremity))

        # Update the psi value
        psi_val_prec = psi_val

    if verbose == "on":
        print("Extremities of the univolatility curves: ", extremities)

    return extremities


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def phi(T, pressure, activity, edge, alpha):
    r"""
    The ``phi`` function returns the value of the function :math:`\phi:\mathbf{R}^2 \rightarrow \mathbf{R}` of the form


    .. math::

        \phi(\alpha, T)=0

    where :math:`\alpha\in [0,1]` is the length parameter of the edge (one of the non-zero mole fractions), and  :math:`T` is
    the boiling temperature of the mixture. This equation represents the thermodynamic equilibrium condition written in the form


    .. math::

       \Phi(x_1, x_2, T)=\sum_{i=1}^3 K_i(x_1, x_2, T)x_i - 1,

    and restricted to the given edge of the composition triangle. Here :math:`K_i(x_1, x_2, T)` denotes the distribution coefficient
    of i-th compound, the distributions coefficient of the missing compound on given binary edge is computed at infinite dilution.


    Parameters
    ----------

    T : float
        The temperature of the mixture

    pressure: dictionary
              Contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
              Contains also the ambient pressure constant :math:`P^0`.

    activity: dictionary
              contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
              of the mixture. Contains  also the ideal gaz constant :math:`R`.

    edge : int
           the index of the edge of the triangle : 1 for the edge  :math:`x_1=0` ( binary mixture of 2th and 3rd compounds), 2 for the edge
           :math:`x_2=0` (binary mixture of 1st and 3rd compounds), 3 for the edge :math:`x_3=0` (binary mixture of 1st and 2nd compounds)

    alpha : float
            the mole fraction of the compound used to parameterize the edge

    Returns
    -------

    y : ?


    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters

    smith.ternary.pressure() for the vapor pressure constants

    smith.ternary.univol.psi() for the ``psi`` function (univolatility condition)
    """

    (pars_p, pars_g, modelName_p, modelName_g) = set_pars_py_to_fortran(
        pressure, activity
    )

    return extrem.phi(
        T,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        alpha,
        pars_p.size,
        pars_g.size,
    )


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def psi(T, pressure, activity, edge, alpha, indi, indj):
    r"""
    The ``psi`` function returns the value of the function :math:`\psi_{i, j}:\mathbf{R}^2 \rightarrow \mathbf{R}` of the form


    .. math::

        \psi_{ij}(\alpha, T)=0

    where :math:`\alpha\in [0,1]` is the length parameter of the given edge (one of the non-zero mole fractions), and  :math:`T` is the
    temperature of the mixture. This equation represents the univolatility condition between i-th and j-the compounds


    .. math::
        \Psi_{ij}(x_1, x_2, T)=K_i(x_1, x_2, T)-K_j(x_1, x_2, T),


    restricted to the given edge of the composition triangle. Here :math:`K_i(x_1, x_2, T)` denotes the distribution coefficient of i-th
    compound, the distributions coefficient of the missing compound on given binary edge is computed at infinite dilution.


    Parameters
    ----------

    T : float
        the temperature of the mixture

    pressure : dictionary
               contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
               Contains also the ambient pressure constant :math:`P^0`.

    activity : dictionary
               contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
               of the mixture. Contains  also the ideal gaz constant :math:`R`.

    edge : int
           the index of the edge of the triangle : 1 for the edge  :math:`x_1=0` ( binary mixture of 2th and 3rd compounds), 2 for the edge
           :math:`x_2=0` (binary mixture of 1st and 3rd compounds), 3 for the edge :math:`x_3=0` (binary mixture of 1st and 2nd compounds)

    alpha : float
            the mole fraction of the compound used parameterize the edge

    indi : int
           the index of i-th compound

    indj : int
           the index of j-th compound


    Returns
    -------

    y : ?



    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters

    smith.ternary.pressure() for the vapor pressure constants

    smith.ternary.univol.phi() for the ``phi`` function (thermodynamic equilibrium condition)
    """

    (pars_p, pars_g, modelName_p, modelName_g) = set_pars_py_to_fortran(
        pressure, activity
    )

    return extrem.psi(
        T,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        alpha,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def extremity(x, pressure, activity, edge, indi, indj):
    r"""

    The ``extremity`` function returns the function of the form :math:`f : \mathbf{R}^2 \rightarrow \mathbf{R}^2` which defines the
    univolatility point between i-th and j-th compounds over the given edge of the composition  triangle :

    .. math::

        \Phi(\alpha, T)=0,    \Psi_{i,j}(\alpha, T)=0


    Parameters
    ----------

    x : array
        a point in the state space: :math:`x=(x_1, x_2, T)`

    pressure : dictionary
               contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
               Contains also the ambient pressure constant :math:`P^0`.

    activity : dictionary
               contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
               of the mixture. Contains  also the ideal gaz constant :math:`R`.

    edge : int
           ihe index of the edge of the triangle : 1 for the edge  :math:`x_1=0` ( binary mixture of 2th and 3rd compounds), 2 for the edge
        :math:`x_2=0` (binary mixture of 1st and 3rd compounds), 3 for the edge :math:`x_3=0` (binary mixture of 1st and 2nd compounds)

    indi : int
           the index of i-th compound

    indj : int
           the index of j-th compound


    Returns
    -------

    y : ?


    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters

    smith.ternary.pressure() for the vapor pressure constants

    smith.ternary.univol.phi() for the ``phi`` function (thermodynamic equilibrium condition)

    smith.ternary.univol.psi() for the ``psi`` function (univolatility condition)

    smith.ternary.univol.extremities() for the complete list of starting (extremity) points for the set of existing univolatility curves between i-th and j-th
    compounds on the given edge of the composition triangle

    smith.ternary.univol.curve() for the computation of a univolatility curve  of index ij starting from the given extremity point

    smith.ternary.univol.diagram() for the computation of the complete set of all existing  univolatility curves of a given mixture
    """

    # Cast of input variables
    if not isinstance(x, float):
        x = np.asarray(x)

    msg_erreur = "Variable x must be a two dimensional array."
    if isinstance(x, np.ndarray):
        if x.size != 2:
            raise ArgumentDimensionError(msg_erreur)
    else:
        raise ArgumentTypeError(msg_erreur)

    (pars_p, pars_g, modelName_p, modelName_g) = set_pars_py_to_fortran(
        pressure, activity
    )

    return extrem.extremity(
        x,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def phi_jac(T, pressure, activity, edge, alpha):
    r"""

    The ``phi_jac`` function returns the gradient of the function ``phi`` computed by automatic differentiation using the  ``TAPENADE`` library


    Parameters
    ----------

    T : float
        the temperature of the mixture

    pressure : dictionary
               contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
               Contains also the ambient     pressure constant :math:`P^0`.

    activity : dictionary
               contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
               of the mixture. Contains  also the ideal gaz constant :math:`R`.

    edge : int
           the index of the edge of the triangle : 1 for the edge  :math:`x_1=0` ( binary mixture of 2th and 3rd compounds), 2 for the edge
           :math:`x_2=0` (binary mixture of 1st and 3rd compounds), 3 for the edge :math:`x_3=0` (binary mixture of 1st and 2nd compounds)

    alpha : float
            the mole fraction of the compound used to parameterize the given edge



    Returns
    -------

    ??


    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters

    smith.ternary.pressure() for the vapor pressure constants

    smith.ternary.univol.phi() for the ``phi`` function (thermodynamic equilibrium condition)
    """

    (pars_p, pars_g, modelName_p, modelName_g) = set_pars_py_to_fortran(
        pressure, activity
    )

    return extrem.phi_jac(
        T,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        alpha,
        pars_p.size,
        pars_g.size,
    )


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def psi_jac(T, pressure, activity, edge, alpha, indi, indj):
    r"""


    The ``psi_jac`` function returns the gradient of the function ``psi`` computed by automatic differentiation using the ``TAPENADE`` library


    Parameters
    ----------

    T : float
        the temperature of the mixture

    pressure : dictionary
               contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
               Contains also the ambient pressure constant :math:`P^0`.

    activity : dictionary
               contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
               of the mixture. Contains  also the ideal gaz constant :math:`R`.

    edge : int
           the index of the edge of the triangle : 1 for the edge  :math:`x_1=0` ( binary mixture of 2th and 3rd compounds), 2 for the edge
           :math:`x_2=0` (binary mixture of 1st and 3rd compounds), 3 for the edge :math:`x_3=0` (binary mixture of 1st and 2nd compounds)

    alpha : float
            the mole fraction of the compound used to parameterize the given edge

    indi : int
           the index of i-th compound

    indj : int
           the index of j-th compound


    Returns
    -------

    ???

    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters

    smith.ternary.pressure() for the vapor pressure constants

    smith.ternary.univol.psi() for the ``psi`` function (univolatility condition)
    """

    (pars_p, pars_g, modelName_p, modelName_g) = set_pars_py_to_fortran(
        pressure, activity
    )

    return extrem.psi_jac(
        T,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        alpha,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def extremity_jac(x, pressure, activity, edge, indi, indj):
    r"""

    The ``extremity_jac`` function returns the Jacobian  of the function ``extremity`` computed by automatic differentiation using the ``TAPENADE`` library.


    Parameters
    ----------

    x : array
        a point in the state space : :math:`x=(x_1, x_2, T)`

    pressure : dictionary
               contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
               Contains also the ambient pressure constant :math:`P^0`.

    activity : dictionary
               contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
               of the mixture. Contains  also the ideal gaz constant :math:`R`.

    edge : int
           the index of the edge of the triangle : 1 for the edge  :math:`x_1=0` ( binary mixture of 2th and 3rd compounds), 2 for the edge
           :math:`x_2=0` (binary mixture of 1st and 3rd compounds), 3 for the edge :math:`x_3=0` (binary mixture of 1st and 2nd compounds)

    indi : int
           the index of i-th compound

    indj : int
           the index of j-th compound


    Returns
    -------

    y : ?


    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters

    smith.ternary.pressure() for the vapor pressure constants

    smith.ternary.univol.phi() for the ``phi`` function (thermodynamic equilibrium condition)

    smith.ternary.univol.psi() for the ``psi`` function (univolatility condition)

    smith.ternary.univol.extremities() for the complete list of starting (extremity) points for the set of existing univolatility curves between i-th and j-th
    compounds on the given edge of the composition triangle

    smith.ternary.univol.curve() for the computation of a univolatility curve  of index ij starting from the given extremity point

    smith.ternary.univol.diagram() for the computation of the complete set of all existing  univolatility curves of a given mixture

    """

    # Cast of input variables
    if not isinstance(x, float):
        x = np.asarray(x)

    msg_erreur = "Variable x must be a two dimensional array."
    if isinstance(x, np.ndarray):
        if x.size != 2:
            raise ArgumentDimensionError(msg_erreur)
    else:
        raise ArgumentTypeError(msg_erreur)

    (pars_p, pars_g, modelName_p, modelName_g) = set_pars_py_to_fortran(
        pressure, activity
    )

    return extrem.extremity_jac(
        x,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        edge,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
#
# CURVE
#
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# computation of a univolatility curve
def curve(
    pressure,
    activity,
    x1_init,
    x2_init,
    temperature_init,
    indi,
    indj,
    options=None,
):
    r"""

    The function ``curve`` calculates the univolatility curve starting from the extremity point :math:`(x_1^{init}, x_2^{init}, T^{init})`
    verifying the univolatility condition between i-th and j-th compound.


    Parameters
    ----------

    pressure : dictionary
               contains the name of the model and the corresponding set of vapor-pressure constants for the saturating pressure computations.
               Contains also the ambient   pressure constant :math:`P^0`.

    activity : dictionary
               contains the name of the model and the corresponding set of constants defining the set of activity coefficients :math:`\gamma_i`
               of the mixture. Contains  also the ideal gaz constant :math:`R`.

    x1_init, x2_init, temperature_init : float
                                          the state coordinates of the extremity point

    indi : int
           the index of i-th compound

    indj : int
           the index of j-th compound

    options : dictionary
              computational options, default value: ``Non``


    Returns
    -------

    y : list
        the output date of the curve in the 3D state space


    Examples
    --------
    >>> import numpy as np
    >>> from .tools import *
    >>> from smith import univol


    Example 1:

    >>> def test_curve():
    ...     Temp_min    = 0
    ...     Temp_max    = 100
    ...     edge        = 1
    ...     indi    = 1
    ...     indj    = 3
    ...     (parametres, modelName) = set_pars_py_to_fortran(parameters_mixture)
    ...     extremities = univol.curve(parametres, indi, indj, edge, Temp_min, Temp_max))
    ...
    ...     extremity   = extremities[0]
    ...     x1_init     = 0.0
    ...     x2_init     = extremity[0]
    ...     temperature_init = extremity[1]
    ...
    ...     (x1, x2, T) = univol.curve(parametres, x1_init, x2_init, temperature_init, indi, indj)

    >>> (x1, x2, T) = univol.curve(parameters_mixture, x1_init, x2_init, temperature_init, indi, indj)
    >>> print(x1, x2, T)


    See Also
    --------

    smith.ternary.activity() for the activity coefficients parameters

    smith.ternary.pressure() for the vapor pressure constants

    smith.ternary.univol.extremities() for the complete list of starting (extremity) points for the set of existing univolatility curves between i-th and j-th

    compounds on the given edge of the composition triangle smith.ternary.univol.curve() for the computation of a univolatility curve
    of index ij starting from the given extremity point

    smith.ternary.univol.diagram() for the computation of the complete set of all existing  univolatility curves of a given mixture

    """

    # Tests on input variables
    if options is None:
        options = Options()

    verbose = options.get("Display")

    # -------------------------------------------------------------------------------
    # 1. we place the initial point (in terms of concentrations) on the triangle

    (x1_init, x2_init) = proj(x1_init, x2_init)

    # -------------------------------------------------------------------------------
    # 2. we start the homotopy and check we are entering the triangle

    # parameters
    (pars_p, pars_g, modelName_p, modelName_g) = set_pars_py_to_fortran(
        pressure, activity
    )

    # homotopic function
    fcurve = lambda x, beta: curve_interface.fcurve(
        x,
        beta,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )

    # jacobian function
    jac_fcurve = lambda x, beta: curve_interface.fcurve_jac(
        x,
        beta,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )

    # options
    opt = path.Options(Display=verbose, MaxSteps=5, MaxIterCorrection=0)  #

    # initial and final homotopic parameter with initial solution to fcurve = 0
    # we assume that fcurve(x_init, beta_init) = 0

    x0 = np.array([x2_init, temperature_init])
    b0 = x1_init

    # betaf = beta_min or beta_max, depending for which we enter in the triangle
    # with beta_min = -1, beta_max = 1
    beta_min = -1.0
    beta_max = 1.0
    bf = beta_max

    # homotopy on 1 step.
    sol = path.solve(
        fcurve,
        x0,
        b0,
        bf,
        options=opt,
        callback=is_out_triangle,
        df=jac_fcurve,
    )

    if sol.status < -10:
        bf = beta_min

    # -------------------------------------------------------------------------------
    # 3. homotopy in the right direction

    # options
    opt = path.Options(
        Display=verbose,
        TolOdeAbs=1e-10,
        TolOdeRel=1e-10,
        MaxStepSizeHomPar=1e-2,
        MaxIterCorrection=0,
    )

    # homotopy
    sol = path.solve(
        fcurve,
        x0,
        b0,
        bf,
        options=opt,
        callback=is_out_triangle,
        df=jac_fcurve,
    )

    if sol.status >= -10:
        print(sol)
        raise Error(
            "Problem during homotopy. The curve should cross the triangle."
        )

    # curve without final point
    x1 = sol.parsout[:-1]
    x2 = sol.xout[:-1, 0]
    T = sol.xout[:-1, 1]

    # second to last point
    x1_0 = sol.parsout[-2]
    x2_0 = sol.xout[-2, 0]
    T_0 = sol.xout[-2, 1]

    x1_f = sol.parsout[-1]

    # -------------------------------------------------------------------------------
    # 4. we find the last point of the curve on the triangle

    opt = path.Options(
        Display=verbose,
        TolOdeAbs=1e-10,
        TolOdeRel=1e-10,
        MaxStepSizeHomPar=1e-2,
    )

    if sol.status == -11:
        edge = 1
    elif sol.status == -12:
        edge = 2
    elif sol.status == -13:
        edge = 3
    else:
        raise Error("Problem during homotopy.")

    # function to cancel
    x0 = np.array([x2_0, T_0])
    b0 = x1_0
    fcross = lambda b: fcross_all_params(
        b, x0, b0, fcurve, jac_fcurve, opt, is_out_triangle, edge
    )

    # finding the root of fcross
    bf = optimize.brentq(
        fcross, x1_0, x1_f, disp=False, xtol=options.get("TolXMin")
    )

    # homotopy to get the final point
    sol = path.solve(
        fcurve,
        x0,
        b0,
        bf,
        options=opt,
        callback=is_out_triangle,
        df=jac_fcurve,
    )

    # get the last point and put it on the triangle
    x1_f = sol.parsout[-1]
    x2_f = sol.xout[-1, 0]
    T_f = sol.xout[-1, 1]

    (x1_f, x2_f) = proj(x1_f, x2_f)

    # add last point to the list
    x1 = np.append(x1, [x1_f])
    x2 = np.append(x2, [x2_f])
    T = np.append(T, [T_f])

    if verbose == "on":
        print("Computed curve in the state space : ", x1, x2, T)

    return (x1, x2, T)


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# orthogonal projection of the point on the triangle
def proj(x1, x2):
    r"""

    The ``proj`` function places the orthogonal projections of an extremity point on the sides of the composition triangle


    Parameters
    ----------

    x1, x2 : float
             composition of the extremity point


    Returns
    -------

    y : list
        the pair of Cartesian coordinates of the extremity points on the sides if the composition  triangle


    Examples
    --------
    >>> from smith import univol


    Example :

    >>> x1 =  0.5
    >>> x2 = -0.01
    >>> (x1, x2) = univol.proj(x1, x2)
    >>> print(x1, x2, T)

    See Also
    --------
    smith.ternary.univol.extremities() returns the complete list of the end-points (extremities) of all univolatility curves of a given mixture
    smith.ternary.univol.curve() for the computation of a univolatility curve  of index ij starting from the given extremity point
    smith.ternary.univol.diagram() for the computation of the complete set of all existing  univolatility curves of a given mixture
    """

    x3 = 1.0 - x1 - x2

    if (x1 <= x2) and (x1 <= x3):
        edge = 1  # x1 = 0
    elif (x2 <= x1) and (x2 <= x3):
        edge = 2  # x2 = 0
    else:
        edge = 3  # x3 = 0

    if edge == 1:
        x1 = 0.0
    elif edge == 2:
        x2 = 0.0
    else:
        a = (1.0 - x1 - x2) / 2.0
        x1 = x1 + a
        x2 = x2 + a

    return (x1, x2)


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# callback to test if the curve goes out the triangle
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


@static_vars(x1_last=1.0, x2_last=1.0, x3_last=1.0, first=True)
def is_out_triangle(infos):
    """r

    The function ``is_out_triangle`` tests whether the given point of the state space it inside or outside of the composition triangle


    Parameters
    ----------

    infos : ?
          ???


    Returns
    -------

    flag : int
           returns 0 if the point is inside the triangle, -11 if :math:`x_1<0`, -12 if  :math:`x_2<0`, and -13 if :math:`x_3<0`.
    """

    x1 = infos.pars[0]
    x2 = infos.x[0]
    x3 = 1.0 - x1 - x2

    flag = 0

    if is_out_triangle.first:
        is_out_triangle.first = False

    else:  # we check if we cross the triangle
        if x1 < 0:
            if is_out_triangle.x1_last >= 0:
                is_out_triangle.first = True
                flag = -11
        if x2 < 0:
            if is_out_triangle.x2_last >= 0:
                is_out_triangle.first = True
                flag = -12
        if x3 < 0:
            if is_out_triangle.x3_last >= 0:
                is_out_triangle.first = True
                flag = -13

    is_out_triangle.x1_last = x1
    is_out_triangle.x2_last = x2
    is_out_triangle.x3_last = x3

    return flag


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# fun to seek exact crossing with the triangle
def fcross_all_params(bf, x0, b0, fcurve, jacfcurve, opt, cb, edge):
    r"""

    The function ``fcross_all_params`` returns the exact crossing point between the univolatility curve and the border of the composition triangle


    Parameters
    ----------

    bf : float
         the final value of the homotopy parameter (?)

    x0 : array
         the starting point of the univolatility curve in the complete state space :math:`(x_1, x_2, T)`

    b0 : float
         the initial value of the homotopy parameter (?)

    fcurve: ?

    jacfcurve : ?
         the Jacobian of the ``fcurve`` function

    opt : ?

    cb: ?

    edge : int
           the index of the edge of the triangle : 1 for the edge  :math:`x_1=0` ( binary mixture of 2th and 3rd compounds), 2 for the edge
           :math:`x_2=0` (binary mixture of 1st and 3rd compounds), 3 for the edge :math:`x_3=0` (binary mixture of 1st and 2nd compounds)


    Returns
    -------
    """

    sol = path.solve(
        fcurve, x0, b0, bf, options=opt, callback=cb, df=jacfcurve
    )

    # final point
    x1 = sol.parsout[-1]
    x2 = sol.xout[-1, 0]
    x3 = 1.0 - x1 - x2

    if edge == 1:
        return x1
    elif edge == 2:
        return x2
    else:
        return x3


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def fcurve(x, beta, modelName_p, pars_p, modelName_g, pars_g, indi, indj):
    # Cast of input variables
    if not isinstance(x, float):
        x = np.asarray(x)

    msg_erreur = "Variable x must be a two dimensional array."
    if isinstance(x, np.ndarray):
        if x.size != 2:
            raise ArgumentDimensionError(msg_erreur)
    else:
        raise ArgumentTypeError(msg_erreur)

    return curve_interface.fcurve(
        x,
        beta,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def jac_fcurve(x, beta, modelName_p, pars_p, modelName_g, pars_g, indi, indj):
    r"""

    The function ``jac_fcurve`` returns the Jacobian of the ``fcurve`` function computed by automatic differentiation with ``TAPENADE``
    library.


    Parameters
    ----------

    x: array
       a point in the state space : :math:`x=(x_1, x_2, T)`.

    beta: float ?
          the value of te homotopic parameter(?)

    modelName: string
    """

    # Cast of input variables
    if not isinstance(x, float):
        x = np.asarray(x)

    msg_erreur = "Variable x must be a two dimensional array."
    if isinstance(x, np.ndarray):
        if x.size != 2:
            raise ArgumentDimensionError(msg_erreur)
    else:
        raise ArgumentTypeError(msg_erreur)

    return curve_interface.fcurve_jac(
        x,
        beta,
        modelName_p,
        pars_p,
        modelName_g,
        pars_g,
        indi,
        indj,
        pars_p.size,
        pars_g.size,
    )


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
#
# OPTIONS
#
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
class Options(options.Options):
    r"""

    Options for :meth:`smith.ternary.univol.extremities`.


    Attributes
    ----------

    Display : str
              display iterations and results or not. Takes values {'on', 'off'}, default value: ``on``

    Nsteps :  int
              maximum number of iterations to solve zeros of  the function ``fun``. Default value: ``100``

    TolXMax : float
              relative tolerance between iterates. Default value: ``1e-6``

    TolXMin :  float
               relative tolerance between iterates. Default value: ``1e-12``

    MaxTolX :  float
               relative tolerance between iterates. Default value : ``1e10``

    R :  float
         the ideal gaz constant. Default value: ``R = 1.9872042586`` Cal/(K.mol)

    P0 : float
         ambient pressure. Default value: ``P0=760`` mmHg



    Examples
    --------

    >>> from nutopy import nle



    Constructor usage

    >>> options = univol.Options()

    >>> options = univol.Options(Display='off', TolX=1e-8)

    >>> options = univol.Options({'Display' : 'off', 'TolX' : 1e-8})



    Update

    >>> options.update(Display='on')



    Get

    >>> solver = options.get('Display')


    References
    ----------

    [1] M. J. D. Powell, A Hybrid Method for Nonlinear Equations.
        Numerical Methods for Nonlinear Algebraic Equations,
        P. Rabinowitz, editor. Gordon and Breach, 1970.
    """

    def __init__(self, *args, **kwargs):
        """
        Doc de __init__


        Parameters
        ----------
        args : tuple
            Anonymous arguments
        kwargs : dictionary
            Named arguments
        """

        self.name = "nle.solve"

        # On donne les valeurs par defaut de options
        self.options = dict(
            Display="off",
            Nsteps=100,
            TolXMax=1e-6,
            TolXMin=1e-8,
            MaxTolX=1e10,
            R=1.9872042586,  # [Cal/(K.mol)]
            P0=760,
        )  # [(mmHg)]

        self.update(*args, **kwargs)
