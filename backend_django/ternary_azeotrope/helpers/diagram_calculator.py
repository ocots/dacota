from ternary_azeotrope.helpers.utils import formatParameters

from .container_runner import start_container
from .microservice_caller import call_microservice

# This variable is used to determine if we calculate the diagram locally or not
# This variable has to eventually be placed in settings.py
LOCAL = 0


def calculate_diagram(c1, c2, c3, a, alpha):
    # Call start_container method to generate the curves
    if LOCAL:
        sc1, sc2, sc3, sa, salpha = formatParameters(c1, c2, c3, a, alpha)
        curve_list = start_container(sc1, sc2, sc3, sa, salpha)
    else:
        curve_list = call_microservice(c1, c2, c3, a, alpha)
    return curve_list
