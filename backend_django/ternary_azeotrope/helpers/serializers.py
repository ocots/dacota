from django.core import serializers as django_serializers
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from ..models import BinaryRelation, Component

# from .user import User


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ["name", "a", "b", "c"]

    def create(self, validated_data):
        # print("VALIDATED_DATA", validated_data)
        """id = None
        if "id" not in validated_data.keys():
            id = validated_data["name"]
        else:
            id = validated_data["id"]"""

        component = Component(
            # id=id,
            name=validated_data["name"],
            a=validated_data["a"],
            b=validated_data["b"],
            c=validated_data["c"],
        )
        # component._state.adding = False
        return component

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.a = validated_data.get("a", instance.b)
        instance.b = validated_data.get("b", instance.b)
        instance.c = validated_data.get("c", instance.c)
        return instance


class BinaryRelationSerializer(serializers.ModelSerializer):
    component1 = ComponentSerializer()
    component2 = ComponentSerializer()

    class Meta:
        model = BinaryRelation
        fields = ["component1", "component2", "a12", "a21", "alpha"]

    def create(self, validated_data):
        # component1 = validated_data.pop("component1")
        # component2 = validated_data.pop("component2")

        return BinaryRelation(
            component1=self.component1.create(validated_data["component1"]),
            component2=self.component1.create(validated_data["component2"]),
            a12=validated_data["a12"],
            a21=validated_data["a21"],
            alpha=validated_data["alpha"],
        )


"""class UserSerializer(serializers.Serializer):
    # components = serializers.ListField(child=ComponentSerializer())
    components = ComponentSerializer(many=True)

    def create(self, validated_data):
        # user = UserSerializer(validated_data, many=True)
        user = User()
        user.components = ComponentSerializer(many=True).create(
            validated_data["components"]
        )

        return user"""


def serialize(objects):
    return django_serializers.serialize(
        "json",
        objects,
        fields=("name", "a", "b", "c"),
        use_natural_primary_keys=True,
    )
