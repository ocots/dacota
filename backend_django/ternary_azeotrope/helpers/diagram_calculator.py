from .microservice_caller import call_microservice


def calculate_diagram(c1, c2, c3, a, alpha):
    curve_list = call_microservice(c1, c2, c3, a, alpha)
    return curve_list
