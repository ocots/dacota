import uuid

from ..helpers.serializers import ComponentSerializer
from ..models import BinaryRelation, Component


class User:
    """Class User that defines data available to a client using the web app on a session.
    data includes what is already in the database plus the elements added by the user on their session
    """

    def __init__(
        self,
    ):
        """Constructor of the User class

        Args:
            selected (list[Component], optional): List of three component chosen by the user for diagram generation. Defaults to None.
        """
        self.components = list(Component.objects.all())
        # self.components = []
        self.binaryRelations = list(BinaryRelation.objects.all())
        self.components_selected = None

    def add_component(self, name: str, a: float, b: float, c: float):
        """add a component added by the user that is not already present in the database

        Args:
            name (str): name of the component
            a (float): value a of the component
            b (float): value b of the component
            c (float): value c of the component
        """

        c = Component(name=name, a=a, b=b, c=c)
        self.components.append(c)
        # Component.objects._remove_from_cache(c)
        # return c

    def add_binaryRelation(
        self,
        component1: Component,
        component2: Component,
        a12: float,
        a21: float,
        alpha: float,
    ):
        """add a binary relation added by the user that is not already present in the database

        Args:
            component1 (Component): first component of the relation
            component2 (Component): second component of the relation
            a12 (float): value a12 component of the relation
            a21 (float): value a21 component of the relation
            alpha (float): value alpha of the relation
        """

        self.binaryRelations.append(
            BinaryRelation(
                component1=component1,
                component2=component2,
                a12=a12,
                a21=a21,
                alpha=alpha,
            )
        )

    def edit_component(
        self, name: str, a: float = None, b: float = None, c: float = None
    ):
        for comp in self.components:
            if comp.name == name:
                if a:
                    comp.a = a

                if b:
                    comp.b = b

                if c:
                    comp.c = c
                return

    def edit_Binaryrelation(
        self,
        name_component1: str,
        name_component2: str,
        a12: float = None,
        a21: float = None,
        alpha: float = None,
    ):
        """Edit one or multiple attribute of a relation which the name of its two components is given

        Args:
            name_component1 (str): name of the first component of the relation
            name_component2 (str): name of the second component of the relation
            a12 (float | None): if a value is passed to a12 argument then the attribute a12 of the relation will be updated with the value passed, if not the a12 will remain the same
            a21 (float | None): if a value is passed to a21 argument then the attribute a21 of the relation will be updated with the value passed, if not the a21 will remain the same
            alpha (float | None): if a value is passed to alpaha argument then the attribute alpaha of the relation will be updated with the value passed, if not the alpaha will remain the same
        """
        for relation in self.binaryRelations:
            if (
                relation.component1.name == name_component1
                and relation.component2.name == name_component2
            ):
                if a12:
                    relation.a12 = a12

                if a21:
                    relation.a21 = a21

                if alpha:
                    relation.alpha = alpha

                return

    def delete_component(self, name: str):
        """Delete from user components' list a component of the name given

        Args:
            name (str): name of the component to delete
        """

        for comp in self.components:
            if comp.name == name:
                self.components.remove(comp)
                return

    def delete_binaryRelation(self, name1: str, name2: str):
        """Delete from user binary relations list a component of the name given

        Args:
            name1 (str): name of the first component of the relation to delete
            name2 (str): name of the second component of the relation to delete
        """

        for relation in self.binaryRelations:
            if (
                relation.component1.name == name1
                and relation.component2.name == name2
            ):
                self.binaryRelations.remove(relation)
                return

    def components_as_str(self):
        res = ""
        for c in self.components:
            res += str(c)
        return res

    def get_user_data_json(self):
        user_data = {
            "components": [
                ComponentSerializer(instance=c).data for c in self.components
            ],
            # "binary_relations": [r.__dict__ for r in self.binaryRelations],
            "components_selected": self.components_selected,
        }
        return user_data

    @staticmethod
    def get_user(user_data):
        user = User()
        serializer = ComponentSerializer()
        user.components = [
            serializer.create(validated_data=c)
            for c in user_data.get("components", [])
        ]
        # print("SERIALIZER", str(user.components))
        # user.binaryRelations = [
        #   BinaryRelation(**r) for r in user_data.get("binary_relations", [])
        # ]
        user.components_selected = user_data.get("components_selected")
        return user
