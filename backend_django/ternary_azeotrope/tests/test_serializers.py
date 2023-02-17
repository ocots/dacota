from collections import OrderedDict

from django.test import TestCase

from ..helpers.serializers import *
from .SetUp import init


class SerialiserTest(TestCase):
    def setUp(self) -> None:
        init(self)
        self.acetone_data = {
            "id": 10,
            "name": "Acetone",
            "a": 4.5,
            "b": 0,
            "c": 1.8,
        }
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

        # self.user = User()
        # self.user.components = [self.acetone, self.benzene]

    def test(self):
        # Component serialisation and deserialisation test

        # testing from json to object
        # cs = ComponentSerializer()
        # comp = cs.create(validated_data=self.acetone_data)
        # self.assertEqual(type(comp), Component)
        # self.assertEqual(str(comp), str(self.acetone))

        # testing from object to json
        # self.assertEqual(
        #    ComponentSerializer(self.acetone).data, self.acetone_data
        # )

        # test binary relation serializer
        print(BinaryRelationSerializer(self.acetone_chloroforme).data)

        relation_dict = {
            "id": 1,
            "component1": OrderedDict(
                [
                    ("id", 1),
                    ("name", "acetone"),
                    ("a", 7.11714),
                    ("b", 1210.595),
                    ("c", 229.664),
                ]
            ),
            "component2": OrderedDict(
                [
                    ("id", 2),
                    ("name", "chloroforme"),
                    ("a", 6.95465),
                    ("b", 1170.966),
                    ("c", 226.232),
                ]
            ),
            "a12": -643.277,
            "a21": 228.457,
            "alpha": 0.3043,
        }
        relation_obj = BinaryRelationSerializer().create(relation_dict)
        print(relation_obj)

        # testing list serialization
        # print(serialize(self.user.components))
        """
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

        print(self.user.get_user_data_json())

        data = {
            "components": [
                {"id": None, "name": "Acetone", "a": 4.5, "b": 0, "c": 1.8},
                {
                    "id": None,
                    "name": "benzene",
                    "a": 6.87087,
                    "b": 1196.76,
                    "c": 219.161,
                },
            ],
            "binary_relations": [],
            "components_selected": None,
        }

        user = User.get_user(data)
        user.add_component("methanol", 0, 0, 0)
        print(user.get_user_data_json())
        # print(user.components)"""
