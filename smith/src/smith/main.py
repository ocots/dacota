import ast
import json
import sys
from json import JSONEncoder

import numpy as np

import smith
from smith.ternary import univol


# https://pynative.com/python-serialize-numpy-ndarray-into-json/
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def main(argv):
    L = list(argv)
    c1 = ast.literal_eval(L[0])
    c2 = ast.literal_eval(L[1])
    c3 = ast.literal_eval(L[2])

    a = np.array(ast.literal_eval(L[3]))
    alpha = np.array(ast.literal_eval(L[4]))

    pressure = smith.ternary.pressure.antoine(c1, c2, c3)
    activity = smith.ternary.activity.nrtl(a, alpha)

    curves_list = univol.diagram(
        pressure, activity, options=univol.Options(Display="off")
    )

    print(json.dumps(curves_list, cls=NumpyArrayEncoder))


if __name__ == "__main__":
    main(sys.argv[1:])
