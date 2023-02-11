from ..models import BinaryRelation


class TernaryMixture:
    """
    TernaryMixture class : represents a ternary mixture of three components and their binary relations.

    Attributes:
        component1 (Componant): The first component in the mixture.
        component2 (Componant): The second component in the mixture.
        component3 (Componant): The third component in the mixture.
        binary_relation1 (BinaryRelation): The binary relation between component1 and component2.
        binary_relation2 (BinaryRelation): The binary relation between component2 and component3.
        binary_relation3 (BinaryRelation): The binary relation between component1 and component3.

    Methods:
        diagram(self) : Computes and returns the ternary diagram for the mixture.
    """

    def __init__(self, component1, component2, component3):
        self.component1 = component1
        self.component2 = component2
        self.component3 = component3
        self.binary_relations = [
            BinaryRelation.objects.get(
                component1=component1, component2=component2
            ),
            BinaryRelation.objects.get(
                component2=component2, component1=component3
            ),
            BinaryRelation.objects.get(
                component3=component3, component1=component1
            ),
        ]

    def diagram(self):
        # Your code to calculate the diagram based on the 3 components and their binary relation
        pass

    def __str__(self):
        return (
            self.component1.name
            + " - "
            + self.component2.name
            + " - "
            + self.component3.name
        )
