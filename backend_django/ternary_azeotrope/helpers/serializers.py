from django.core import serializers as django_serializers
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from ..models import Component

# from .user import User


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ["name", "a", "b", "c"]

    def create(self, validated_data):
        print("VALIDATED_DATA", validated_data)
        component = Component(
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


"""class UserSerializer(serializers.Serializer):
    # components = serializers.ListField(child=ComponentSerializer())
    components = ComponentSerializer(many=True)

    def create(self, validated_data):
        # user = UserSerializer(validated_data, many=True)
        user = User()
        user.components = ComponentSerializer(many=True).create(
            validated_data["components"]
        )

        return user


def serialize(objects):
    return django_serializers.serialize(
        "json",
        objects,
        fields=("name", "a", "b", "c"),
        use_natural_primary_keys=True,
    )"""
