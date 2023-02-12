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
    C1 = ast.literal_eval(L[0])
    C2 = ast.literal_eval(L[1])
    C3 = ast.literal_eval(L[2])

    A = np.array(ast.literal_eval(L[3]))
    alpha = np.array(ast.literal_eval(L[4]))

    pressure = smith.ternary.pressure.antoine(C1, C2, C3)
    activity = smith.ternary.activity.nrtl(A, alpha)

    curves_list = univol.diagram(
        pressure, activity, options=univol.Options(Display="off")
    )

    print(json.dumps(curves_list, cls=NumpyArrayEncoder))


if __name__ == "__main__":
    main(sys.argv[1:])
