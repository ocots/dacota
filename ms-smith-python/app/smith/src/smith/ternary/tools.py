import numpy as np


def set_pars_py_to_fortran(pressure, activity):
    # Models names
    name_p = pressure["name"]
    name_g = activity["name"]

    if name_g == "NRTL" and name_p == "antoine":
        # Constants
        R = activity["R"]

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

    elif name_g == "NRTL" and name_p == "dippr":
        # Constants
        R = activity["R"]

        # Adaptation of the parameters:
        A = [[x for x in y] for y in activity["A"]]

        # Model name:
        modelName_p = name_p
        modelName_g = name_g

        alpha = activity["alpha"]
        dipprA = pressure["1"]
        dipprB = pressure["2"]
        dipprC = pressure["3"]
        dipprD = pressure["4"]
        dipprE = pressure["5"]
        P0 = pressure["P0"]

        pars_p = np.concatenate(
            (dipprA, dipprB, dipprC, dipprD, dipprE, P0), axis=None
        )

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

    elif name_g == "UNIQUAC" and name_p == "antoine":
        # Constants
        z = activity["z"]
        R = activity["R"]

        # Adaptation of the parameters:
        A = [[x for x in y] for y in activity["A"]]

        # Model name:
        modelName_p = name_p
        modelName_g = name_g

        r = activity["r"]
        q = activity["q"]
        Qp = activity["Qp"]
        antoineA = pressure["1"]
        antoineB = pressure["2"]
        antoineC = pressure["3"]

        pars_p = np.concatenate((antoineA, antoineB, antoineC), axis=None)

        pars_g = np.concatenate(
            (
                np.asarray(A[0]),
                np.asarray(A[1]),
                np.asarray(A[2]),
                np.asarray(r),
                np.asarray(q),
                np.asarray(Qp),
                z,
                R,
            ),
            axis=None,
        )

    elif name_g == "UNIQUAC" and name_p == "dippr":
        # Constants
        z = activity["z"]
        R = activity["R"]

        # Adaptation of the parameters:
        A = [[x for x in y] for y in activity["A"]]

        # Model name:
        modelName_p = name_p
        modelName_g = name_g

        r = activity["r"]
        q = activity["q"]
        Qp = activity["Qp"]
        dipprA = pressure["1"]
        dipprB = pressure["2"]
        dipprC = pressure["3"]
        dipprD = pressure["4"]
        dipprE = pressure["5"]
        P0 = pressure["P0"]

        pars_p = np.concatenate(
            (dipprA, dipprB, dipprC, dipprD, dipprE, P0), axis=None
        )

        pars_g = np.concatenate(
            (
                np.asarray(A[0]),
                np.asarray(A[1]),
                np.asarray(A[2]),
                np.asarray(r),
                np.asarray(q),
                np.asarray(Qp),
                z,
                R,
            ),
            axis=None,
        )

    return (pars_p, pars_g, modelName_p, modelName_g)
