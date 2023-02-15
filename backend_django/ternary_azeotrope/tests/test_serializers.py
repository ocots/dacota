from django.test import TestCase

from ..helpers.serializers import *
from .SetUp import init


class SerialiserTest(TestCase):
    def setUp(self) -> None:
        # init(self)
        self.acetone_data = {"name": "Acetone", "a": 4.5, "b": 0, "c": 1.8}
        self.acetone = Component(name="Acetone", a=4.5, b=0, c=1.8)
        self.benzene = Component(
            name="benzene",
            a=6.87087,
            b=1196.76,
            c=219.161,
        )

        self.components_data = {
            "components": [
                {"name": "Acetone", "a": 4.5, "b": 0, "c": 1.8},
                {
                    "name": "benzene",
                    "a": 6.87087,
                    "b": 1196.76,
                    "c": 219.161,
                },
            ]
        }
        """{
            "name": "methanol",
            "a": 8.08097,
            "b": 1582.271,
            "c": 239.726,
        },"""

        self.user = User()
        self.user.components = [self.acetone, self.benzene]

    def test(self):
        # Component serialisation and deserialisation test

        # testing from json to object
        cs = ComponentSerializer()
        comp = cs.create(validated_data=self.acetone_data)
        self.assertEqual(type(comp), Component)
        self.assertEqual(str(comp), str(self.acetone))

        # testing from object to json
        self.assertEqual(
            ComponentSerializer(self.acetone).data, self.acetone_data
        )

        # testing list serialization
        # print(serialize(self.user.components))

        # test from user object to json
        user_s = UserSerializer(self.user)
        self.assertEqual(user_s.data, self.components_data)
        # print(user_s.data)

        # test from json to user object
        user_from_json = UserSerializer().create(
            validated_data=self.components_data
        )
        # print(self.components_data)
        self.assertEqual(user_from_json.components_selected, None)
        self.assertEqual(user_from_json.binaryRelations, [])

        # print("components of user from json", user_from_json.components)
        # print("components of user ", self.user.components)
        self.assertEqual(
            str(user_from_json.components), str(self.user.components)
        )
