from ..models import BinaryRelation
from .container_runner import start_container
from .diagram_calculalor import calculate_diagram


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

    def __init__(
        self,
        component1,
        component2,
        component3,
        binary_relations1,
        binary_relations2,
        binary_relations3,
    ):
        self.component1 = component1
        self.component2 = component2
        self.component3 = component3
        self.binary_relations = [
            binary_relations1,
            binary_relations2,
            binary_relations3,
        ]

    def diagram(self):
        c1, c2, c3, a, alpha = self.getParameterForDiagram()
        # sc1, sc2, sc3, sa, salpha = self.formatParameters(c1, c2, c3, a, alpha)
        sc1, sc2, sc3, sa, salpha = self.formatParameters(c1, c2, c3, a, alpha)
        # Call start_container method to generate the curves
        curve_list = calculate_diagram(sc1, sc2, sc3, sa, salpha)
        return curve_list

    def getParameterForDiagram(self):
        c1 = [self.component1.a, self.component1.b, self.component1.c]
        c2 = [self.component2.a, self.component2.b, self.component2.c]
        c3 = [self.component3.a, self.component3.b, self.component3.c]
        a = [[0, None, None], [None, 0, None], [None, None, 0]]
        alpha = [[0, None, None], [None, 0, None], [None, None, 0]]

        a[0][1] = self.binary_relations[0].a12
        a[1][0] = self.binary_relations[0].a21
        alpha[0][1] = alpha[1][0] = self.binary_relations[0].alpha

        a[1][2] = self.binary_relations[1].a12
        a[2][1] = self.binary_relations[1].a21
        alpha[1][2] = alpha[2][1] = self.binary_relations[1].alpha

        a[0][2] = self.binary_relations[2].a12
        a[2][0] = self.binary_relations[2].a21
        alpha[0][2] = alpha[2][0] = self.binary_relations[2].alpha

        return c1, c2, c3, a, alpha

    def formatParameters(self, c1, c2, c3, a, alpha):
        c1Formatted = str(c1)
        c2Formatted = str(c2)
        c3Formatted = str(c3)
        aFormatted = str(a)
        alphaFormatted = str(alpha)

        return (
            c1Formatted,
            c2Formatted,
            c3Formatted,
            aFormatted,
            alphaFormatted,
        )

    def __str__(self):
        return (
            self.component1.name
            + " - "
            + self.component2.name
            + " - "
            + self.component3.name
        )
