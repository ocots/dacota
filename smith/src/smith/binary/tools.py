import numpy as np


def set_pars_py_to_fortran(pressure, activity):
    # Constants
    R = activity["R"]

    # Models names
    name_p = pressure["name"]
    name_g = activity["name"]

    if name_g == "NRTL" and name_p == "antoine":
        # Adaptation of the parameters:
        A = [[x for x in y] for y in activity["A"]]

        # Model name:
        modelName_p = name_p
        modelName_g = name_g

        alpha = activity["alpha"]
        antoineA = pressure["1"]
        antoineB = pressure["2"]
        antoineC = pressure["3"]

        pars_p = np.concatenate((antoineA, antoineB, antoineC), axis=None)

        pars_g = np.concatenate(
            (
                np.asarray(A[0]),
                np.asarray(A[1]),
                np.asarray(A[2]),
                np.asarray(alpha[0]),
                np.asarray(alpha[1]),
                np.asarray(alpha[2]),
                R,
            ),
            axis=None,
        )

    return (pars_p, pars_g, modelName_p, modelName_g)
