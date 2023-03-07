import json
from json import JSONEncoder

import numpy as np
import smith
from smith.ternary import azeotrope, univol


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def ternaryDiagram(parameters):
    c1 = parameters["c1"]
    c2 = parameters["c2"]
    c3 = parameters["c3"]
    a = np.array(parameters["a"])
    alpha = np.array(parameters["alpha"])

    pressure = smith.ternary.pressure.antoine(
        c1, c2, c3
    )  # P0 étant un paramètre optionnel à pressure
    activity = smith.ternary.activity.nrtl(
        a, alpha
    )  # R étant un paramètre optionnel à activity

    curves_list = univol.diagram(
        pressure, activity, options=univol.Options(Display="off")
    )

    # This code is returns add a dictionnary that contains the position of the last element and not -1
    # for i, curve in enumerate(curves_list):
    #     if len(curve["x1"]) == len(curve["x2"]):
    #         last_position = len(curve["x1"]) - 1
    #     else:
    #         last_position = -1
    #     curve["azeo"] = {"0": False, str(last_position): False}

    #     last = np.array([curve["x1"][-1], curve["x2"][-1], curve["T"][-1]])
    #     fun_last = azeotrope.fun(last, pressure, activity)
    #     if np.allclose(fun_last, np.zeros(3)):
    #         curve["azeo"][str(last_position)] = True

    #     first = np.array([curve["x1"][0], curve["x2"][0], curve["T"][0]])
    #     fun_first = azeotrope.fun(first, pressure, activity)
    #     if np.allclose(fun_first, np.zeros(3)):
    #         curve["azeo"]["0"] = True

    # This code is returns add a dictionnary that contains the position of the last element and not -1
    for i, curve in enumerate(curves_list):
        curve["azeo"] = {"0": False, "-1": False}

        last = np.array([curve["x1"][-1], curve["x2"][-1], curve["T"][-1]])
        fun_last = azeotrope.fun(last, pressure, activity)
        if np.allclose(fun_last, np.zeros(3)):
            curve["azeo"]["-1"] = True

        first = np.array([curve["x1"][0], curve["x2"][0], curve["T"][0]])
        fun_first = azeotrope.fun(first, pressure, activity)
        if np.allclose(fun_first, np.zeros(3)):
            curve["azeo"]["0"] = True

    curves_json = json.loads(json.dumps(curves_list, cls=NumpyArrayEncoder))

    return curves_json
