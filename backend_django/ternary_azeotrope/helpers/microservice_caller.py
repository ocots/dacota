# This is the endpoint of the microservice, it is the IP address of the server where the microservice is running
import json
import os

import requests

from backend_django.settings import AUTH_TOKEN, MS_ENDPOINT


def call_microservice(c1, c2, c3, a, alpha):
    # Call the microservice to generate the curves, the data is sent as a json object with the following structure:
    # {
    #     "c1": [a, b, c],
    #     "c2": [a, b, c],
    #     "c3": [a, b, c],
    #     "a": [[0, a12, a13], [a21, 0, a23], [a31, a32, 0]],
    #     "alpha": [[0, alpha12, alpha13], [alpha21, 0, alpha23], [alpha31, alpha32, 0]]
    # }
    # We use the requetes module to send a post request to the microservice
    # The request also contains the authorization token that is defined as an environment variable in .env file

    # The data is sent as a json object
    data = {
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "a": a,
        "alpha": alpha,
    }
    # The endpoint is the IP address of the server where the microservice is running
    endpoint = MS_ENDPOINT
    # The port is the port where the microservice is listening
    port = 80
    # The path is the path of the endpoint
    path = "/ternary-diagram"
    # The url is the combination of the endpoint, the port and the path
    url = "http://" + endpoint + ":" + str(port) + path
    # The token is the authorization token that is defined as an environment variable in .env file
    token = "Bearer " + AUTH_TOKEN
    # The headers are the authorization token and the content type
    headers = {"Authorization": token, "Content-Type": "application/json"}
    # The response is the response of the microservice
    response = requests.post(url, json=data, headers=headers)
    # The response is a json object that contains the curves
    curve_list = response.json()
    return curve_list
