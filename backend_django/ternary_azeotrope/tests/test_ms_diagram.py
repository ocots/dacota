from django.test import TestCase
from ternary_azeotrope.helpers.container_runner import start_container
from ternary_azeotrope.helpers.microservice_caller import call_microservice
from ternary_azeotrope.helpers.utils import load_json


class TestMS(TestCase):
    def setUp(self):
        self.c1 = [7.11714, 1210.595, 229.664]
        self.c2 = [6.95465, 1170.966, 226.232]
        self.c3 = [8.08097, 1582.271, 239.726]
        self.a = [
            [0, -643.277, 184.701],
            [228.457, 0, 2736.86],
            [222.645, -1244.03, 0],
        ]
        self.alpha = [
            [0, 0.3043, 0.3084],
            [0.3043, 0, 0.095],
            [0.3084, 0.095, 0],
        ]

    def test_post_ternary_diagram_with_invalid_parameters(self):
        component = [1, 2]
        diagramMS = call_microservice(
            component, self.c2, self.c3, self.a, self.alpha
        )
        assert diagramMS == {"detail": "Invalid parameters"}

    def test_post_ternary_diagram(self):
        # Load the expected result from the file graph.json defined in the folder where manage.py is located, use the load_json function defined in the utils.py file
        expected_result = load_json("graph.json")
        diagramMS = call_microservice(
            self.c1, self.c2, self.c3, self.a, self.alpha
        )
        assert diagramMS == expected_result

    def test_compare_local_and_ms_diagram(self):
        """diagramLocal = start_container(
            self.c1, self.c2, self.c3, self.a, self.alpha
        )

        diagramMS = call_microservice(
            self.c1, self.c2, self.c3, self.a, self.alpha
        )

        assert diagramLocal == diagramMS"""
