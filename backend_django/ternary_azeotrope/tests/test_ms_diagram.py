import requests
from django.test import TestCase
from ternary_azeotrope.helpers.ternary_mixture import TernaryMixture
from ternary_azeotrope.helpers.utils import load_json
from ternary_azeotrope.models import BinaryRelation, Component

from backend_django.settings import AUTH_TOKEN, MS_ENDPOINT


class TestMS(TestCase):
    def setUp(self):
        self.acetone = Component.objects.create(
            name="acetone",
            a=7.11714,
            b=1210.595,
            c=229.664,
        )
        self.chloroforme = Component.objects.create(
            name="chloroforme",
            a=6.95465,
            b=1170.966,
            c=226.232,
        )
        self.benzene = Component.objects.create(
            name="benzene",
            a=6.87087,
            b=1196.760,
            c=219.161,
        )
        self.acetone_chloroforme = BinaryRelation.objects.create(
            component1=self.acetone,
            component2=self.chloroforme,
            a12=-643.277,
            a21=228.457,
            alpha=0.3043,
        )
        self.acetone_benzene = BinaryRelation.objects.create(
            component1=self.acetone,
            component2=self.benzene,
            a12=-193.34,
            a21=569.931,
            alpha=0.3007,
        )
        self.chloroforme_benzene = BinaryRelation.objects.create(
            component1=self.chloroforme,
            component2=self.benzene,
            a12=176.8791,
            a21=-288.2136,
            alpha=0.3061,
        )
        self.methanol = Component.objects.create(
            name="methanol",
            a=8.08097,
            b=1582.271,
            c=239.726,
        )
        self.acetone_methanol = BinaryRelation.objects.create(
            component1=self.acetone,
            component2=self.methanol,
            a12=184.701,
            a21=222.645,
            alpha=0.3084,
        )
        self.chloroforme_methanol = BinaryRelation.objects.create(
            component1=self.chloroforme,
            component2=self.methanol,
            a12=2736.86,
            a21=-1244.03,
            alpha=0.095,
        )
        self.ethylacetate = Component.objects.create(
            name="ethylacetate",
            a=7.10179,
            b=1244.951,
            c=217.881,
        )
        self.acetone_ethylacetate = BinaryRelation.objects.create(
            component1=self.acetone,
            component2=self.ethylacetate,
            a12=529.7,
            a21=-360,
            alpha=0.2,
        )
        self.ethylacetate_benzene = BinaryRelation.objects.create(
            component1=self.ethylacetate,
            component2=self.benzene,
            a12=-273.017,
            a21=383.126,
            alpha=0.3194,
        )
        self.methylacetate = Component.objects.create(
            name="methylacetate",
            a=7.06524,
            b=1157.630,
            c=219.726,
        )
        self.hexane = Component.objects.create(
            name="hexane",
            a=6.91058,
            b=1189.640,
            c=226.280,
        )
        self.methylacetate_methanol = BinaryRelation.objects.create(
            component1=self.methylacetate,
            component2=self.methanol,
            a12=441.452,
            a21=304.005,
            alpha=0.1174,
        )
        self.methanol_hexane = BinaryRelation.objects.create(
            component1=self.methanol,
            component2=self.hexane,
            a12=1619.38,
            a21=1622.29,
            alpha=0.4365,
        )
        self.methylacetate_hexane = BinaryRelation.objects.create(
            component1=self.methylacetate,
            component2=self.hexane,
            a12=647.05,
            a21=403.459,
            alpha=0.2,
        )

        self.mix1 = TernaryMixture(
            self.acetone,
            self.chloroforme,
            self.methanol,
            self.acetone_chloroforme,
            self.chloroforme_methanol,
            self.acetone_methanol,
        )

        self.mix2 = TernaryMixture(
            self.acetone,
            self.chloroforme,
            self.benzene,
            self.acetone_chloroforme,
            self.chloroforme_benzene,
            self.acetone_benzene,
        )

        self.mix3 = TernaryMixture(
            self.acetone,
            self.ethylacetate,
            self.benzene,
            self.acetone_ethylacetate,
            self.ethylacetate_benzene,
            self.acetone_benzene,
        )

        self.mix4 = TernaryMixture(
            self.methylacetate,
            self.methanol,
            self.hexane,
            self.methylacetate_methanol,
            self.methanol_hexane,
            self.methylacetate_hexane,
        )

    def test_get_home(self):
        # The endpoint is the IP address of the server where the microservice is running
        endpoint = MS_ENDPOINT
        # The port is the port where the microservice is listening
        port = 80
        # The path is the path of the endpoint
        path = ""
        # The url is the combination of the endpoint, the port and the path
        url = "http://" + endpoint + ":" + str(port) + path

        response = requests.get(url)
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"

    def test_post_home(self):
        # The endpoint is the IP address of the server where the microservice is running
        endpoint = MS_ENDPOINT
        # The port is the port where the microservice is listening
        port = 80
        # The path is the path of the endpoint
        path = "/"
        # The url is the combination of the endpoint, the port and the path
        url = "http://" + endpoint + ":" + str(port) + path

        response = requests.post(url)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert response.json() == {"Hello": "World"}

    def test_post_parameters_echo(self):
        data = {
            "c1": [7.11714, 1210.595, 229.664],
            "c2": [6.95465, 1170.966, 226.232],
            "c3": [8.08097, 1582.271, 239.726],
            "a": [
                [0, -643.277, 184.701],
                [228.457, 0, 2736.86],
                [222.645, -1244.03, 0],
            ],
            "alpha": [
                [0, 0.3043, 0.3084],
                [0.3043, 0, 0.095],
                [0.3084, 0.095, 0],
            ],
        }
        # The endpoint is the IP address of the server where the microservice is running
        endpoint = MS_ENDPOINT
        # The port is the port where the microservice is listening
        port = 80
        # The path is the path of the endpoint
        path = "/parameters-echo"
        # The url is the combination of the endpoint, the port and the path
        url = "http://" + endpoint + ":" + str(port) + path

        response = requests.post(url, json=data)
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid endpoint"}

    def test_post_ternary_diagram_with_missing_parameters(self):
        data = {
            "c1": [7.11714, 1210.595, 229.664],
            "c2": [6.95465, 1170.966, 226.232],
            "c3": [8.08097, 1582.271, 239.726],
            "a": [
                [0, -643.277, 184.701],
                [228.457, 0, 2736.86],
                [222.645, -1244.03, 0],
            ],
        }
        # The endpoint is the IP address of the server where the microservice is running
        endpoint = MS_ENDPOINT
        # The port is the port where the microservice is listening
        port = 80
        # The path is the path of the endpoint
        path = "/ternary-diagram"
        # The url is the combination of the endpoint, the port and the path
        url = "http://" + endpoint + ":" + str(port) + path
        response = requests.post(
            url,
            json=data,
            headers={"Authorization": f"Ayman {AUTH_TOKEN}"},
        )
        assert response.status_code == 400
        assert response.headers["content-type"] == "application/json"
        assert response.json() == {"detail": "Missing one or more parameters"}

    def test_post_ternary_diagram_with_invalid_parameters(self):
        data = {
            "c1": [7.11714, 1210.595],
            "c2": [6.95465, 1170.966, 226.232],
            "c3": [8.08097, 1582.271, 239.726],
            "a": [
                [0, -643.277, 184.701],
                [228.457, 0, 2736.86],
                [222.645, -1244.03, 0],
            ],
            "alpha": [
                [0, 0.3043, 0.3084],
                [0.3043, 0, 0.095],
                [0.3084, 0.095, 0],
            ],
        }
        # The endpoint is the IP address of the server where the microservice is running
        endpoint = MS_ENDPOINT
        # The port is the port where the microservice is listening
        port = 80
        # The path is the path of the endpoint
        path = "/ternary-diagram"
        # The url is the combination of the endpoint, the port and the path
        url = "http://" + endpoint + ":" + str(port) + path

        response = requests.post(
            url,
            json=data,
            headers={"Authorization": f"Ayman {AUTH_TOKEN}"},
        )
        assert response.status_code == 400
        assert response.headers["content-type"] == "application/json"
        assert response.json() == {"detail": "Invalid parameters"}

    def test_post_ternary_diagram_with_invalid_parameters2(self):
        data = {
            "c1": [7.11714, 1210.595, 0],
            "c2": [6.95465, -1170.966, 226.232],
            "c3": [8.08097, 1582.271, 239.726],
            "a": [
                [0, -643.277, 184.701],
                [228.457, 0, "2736.86"],
                [222.645, -1244.03, 0],
            ],
            "alpha": [
                [0, 0.3043, 0.3084],
                [0.3043, 0, 0.095],
                [0.3084, 0.095, 0],
            ],
        }
        # The endpoint is the IP address of the server where the microservice is running
        endpoint = MS_ENDPOINT
        # The port is the port where the microservice is listening
        port = 80
        # The path is the path of the endpoint
        path = "/ternary-diagram"
        # The url is the combination of the endpoint, the port and the path
        url = "http://" + endpoint + ":" + str(port) + path

        response = requests.post(
            url,
            json=data,
            headers={"Authorization": f"Ayman {AUTH_TOKEN}"},
        )
        assert response.status_code == 400
        assert response.headers["content-type"] == "application/json"
        assert response.json() == {"detail": "Invalid parameters"}

    def test_post_ternary_diagram_with_no_token(self):
        data = {
            "c1": [7.11714, 1210.595, 229.664],
            "c2": [6.95465, 1170.966, 226.232],
            "c3": [8.08097, 1582.271, 239.726],
            "a": [
                [0, -643.277, 184.701],
                [228.457, 0, 2736.86],
                [222.645, -1244.03, 0],
            ],
            "alpha": [
                [0, 0.3043, 0.3084],
                [0.3043, 0, 0.095],
                [0.3084, 0.095, 0],
            ],
        }
        # The endpoint is the IP address of the server where the microservice is running
        endpoint = MS_ENDPOINT
        # The port is the port where the microservice is listening
        port = 80
        # The path is the path of the endpoint
        path = "/ternary-diagram"
        # The url is the combination of the endpoint, the port and the path
        url = "http://" + endpoint + ":" + str(port) + path

        response = requests.post(url, json=data)
        assert response.status_code == 401
        assert response.headers["content-type"] == "application/json"

    def test_post_ternary_diagram(self):
        data = {
            "c1": [7.11714, 1210.595, 229.664],
            "c2": [6.95465, 1170.966, 226.232],
            "c3": [8.08097, 1582.271, 239.726],
            "a": [
                [0, -643.277, 184.701],
                [228.457, 0, 2736.86],
                [222.645, -1244.03, 0],
            ],
            "alpha": [
                [0, 0.3043, 0.3084],
                [0.3043, 0, 0.095],
                [0.3084, 0.095, 0],
            ],
        }
        # Load the expected result from the file graph.json defined in the folder where manage.py is located, use the load_json function defined in the utils.py file
        expected_result = load_json("graph.json")

        # The endpoint is the IP address of the server where the microservice is running
        endpoint = MS_ENDPOINT
        # The port is the port where the microservice is listening
        port = 80
        # The path is the path of the endpoint
        path = "/ternary-diagram"
        # The url is the combination of the endpoint, the port and the path
        url = "http://" + endpoint + ":" + str(port) + path
        response = requests.post(
            url,
            json=data,
            headers={"Authorization": f"Ayman {AUTH_TOKEN}"},
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert response.json() == expected_result
