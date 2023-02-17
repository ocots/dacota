from .container_runner import start_container
from .microservice_caller import call_microservice

# This variable is used to determine if we calculate the diagram locally or not
# This variable has to eventually have to be placed in settings.py
LOCAL = 0


def calculate_diagram(c1, c2, c3, a, alpha):
    # Call start_container method to generate the curves
    if LOCAL:
        curve_list = start_container(c1, c2, c3, a, alpha)
    else:
        curve_list = call_microservice(c1, c2, c3, a, alpha)
    return curve_list
