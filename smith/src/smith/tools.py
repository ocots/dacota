import numpy as np


def finite_diff(fun, x, *args, **kwargs):
    v_eps = np.finfo(float).eps
    if isinstance(x, float):
        t = np.sqrt(v_eps) * np.sqrt(np.max(1.0, np.abs(x)))
        j = (fun(x + t, *args, **kwargs) - fun(x, *args, **kwargs)) / t
    else:
        n = x.size
        j = np.zeros((n, n))
        f = fun(x, *args, **kwargs)
        for i in range(0, n):
            t = np.sqrt(v_eps) * np.sqrt(np.maximum(1.0, np.abs(x[i])))
            xi = x[i]
            x[i] = xi + t
            j[:, i] = (fun(x, *args, **kwargs) - f) / t
            x[i] = xi

    return j


def getR():
    return 1.9872042586  # [Cal/(K.mol)]
