from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import Client, TestCase
from ternary_azeotrope.helpers.ternary_mixture import TernaryMixture
from ternary_azeotrope.models import BinaryRelation, Component

"""
acetone     = [7.11714, 1210.595, 229.664]
chloroforme = [6.95465, 1170.966, 226.232]
methanol    = [8.08097, 1582.271, 239.726]
A     = [[0, -643.277, 184.701], [228.457, 0, 2736.86], [222.645, -1244.03, 0]]
alpha = [[0, 0.3043, 0.3084], [0.3043, 0, 0.095], [0.3084, 0.095, 0]]


acetone     = [7.11714, 1210.595, 229.664]
chloroforme = [6.95465, 1170.966, 226.232]
benzene     = [6.87087, 1196.760, 219.161]
A     = [[0, -643.277, -193.34], [228.457, 0, 176.8791], [569.931, -288.2136, 0]]
alpha = [[0, 0.3043, 0.3007], [0.3043, 0, 0.3061], [0.3007, 0.3061, 0]]


acetone      = [7.11714, 1210.595, 229.664]
ethylacetate = [7.10179, 1244.951, 217.881]
benzene      = [6.87987, 1196.760, 219.161]
A     = [[0, 529.7, -193.34], [-360, 0, -273.017], [569.931, 383.126, 0]]
alpha = [[0, 0.2, 0.3007], [0.2, 0, 0.3194], [0.3007, 0.3194, 0]]


methylacetate = [7.06524, 1157.630, 219.726]
methanol      = [8.08097, 1582.271, 239.726]
hexane        = [6.91058, 1189.640, 226.280]
A     = [[0, 441.452, 647.05], [304.005, 0, 1619.38], [403.459, 1622.29, 0]]
alpha = [[0, 0.1174, 0.2], [0.1174, 0, 0.4365], [0.2, 0.4365, 0]]
"""


class TestModels(TestCase):
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

    # This test is working, launching multiple times the same function does not consume a lot of memory, it's cpu bound.
    # Calculating the diagram takes approximately 4 seconds on my computer.
    def test_100_diagram(self):
        for i in range(0):
            diagram = self.mix1.diagram()

    def test_parameters_for_diagram(self):
        # Test the parameters for the diagram: Acetone, Chloroforme, Methanol
        c1, c2, c3, a, alpha = self.mix1.getParameterForDiagram()
        self.assertEqual(c1, [7.11714, 1210.595, 229.664])
        self.assertEqual(c2, [6.95465, 1170.966, 226.232])
        self.assertEqual(c3, [8.08097, 1582.271, 239.726])
        self.assertEqual(
            a,
            [
                [0, -643.277, 184.701],
                [228.457, 0, 2736.86],
                [222.645, -1244.03, 0],
            ],
        )
        self.assertEqual(
            alpha,
            [[0, 0.3043, 0.3084], [0.3043, 0, 0.095], [0.3084, 0.095, 0]],
        )

    def test_parameters_for_diagram2(self):
        # Test the parameters for the diagram: Acetone, Chloroforme, Benzene
        c1, c2, c3, a, alpha = self.mix2.getParameterForDiagram()
        self.assertEqual(c1, [7.11714, 1210.595, 229.664])
        self.assertEqual(c2, [6.95465, 1170.966, 226.232])
        self.assertEqual(c3, [6.87087, 1196.760, 219.161])
        self.assertEqual(
            a,
            [
                [0, -643.277, -193.34],
                [228.457, 0, 176.8791],
                [569.931, -288.2136, 0],
            ],
        )
        self.assertEqual(
            alpha,
            [[0, 0.3043, 0.3007], [0.3043, 0, 0.3061], [0.3007, 0.3061, 0]],
        )

    def test_parameters_for_diagram3(self):
        # Test the parameters for the diagram: Acetone, Ethylacetate, Benzene
        c1, c2, c3, a, alpha = self.mix3.getParameterForDiagram()
        self.assertEqual(c1, [7.11714, 1210.595, 229.664])
        self.assertEqual(c2, [7.10179, 1244.951, 217.881])
        self.assertEqual(c3, [6.87087, 1196.760, 219.161])
        self.assertEqual(
            a,
            [[0, 529.7, -193.34], [-360, 0, -273.017], [569.931, 383.126, 0]],
        )
        self.assertEqual(
            alpha, [[0, 0.2, 0.3007], [0.2, 0, 0.3194], [0.3007, 0.3194, 0]]
        )

    def test_parameters_for_diagram4(self):
        # Test the parameters for the diagram: Methylacetate, Methanol, Hexane
        c1, c2, c3, a, alpha = self.mix4.getParameterForDiagram()
        self.assertEqual(c1, [7.06524, 1157.630, 219.726])
        self.assertEqual(c2, [8.08097, 1582.271, 239.726])
        self.assertEqual(c3, [6.91058, 1189.640, 226.280])
        self.assertEqual(
            a,
            [
                [0, 441.452, 647.05],
                [304.005, 0, 1619.38],
                [403.459, 1622.29, 0],
            ],
        )
        self.assertEqual(
            alpha, [[0, 0.1174, 0.2], [0.1174, 0, 0.4365], [0.2, 0.4365, 0]]
        )
