# Create tests for the models.py file

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import Client, TestCase
from ternary_azeotrope.models import BinaryRelation, Component

"""
acetone     = [7.11714, 1210.595, 229.664]
chloroforme = [6.95465, 1170.966, 226.232]
benzene     = [6.87087, 1196.760, 219.161]
A     = [[0, -643.277, -193.34], [228.457, 0, 176.8791], [569.931, -288.2136, 0]]
alpha = [[0, 0.3043, 0.3007], [0.3043, 0, 0.3061], [0.3007, 0.3061, 0]]


acetone     = [7.11714, 1210.595, 229.664]
chloroforme = [6.95465, 1170.966, 226.232]
methanol    = [8.08097, 1582.271, 239.726]
A     = [[0, -643.277, 184.701], [228.457, 0, 2736.86], [222.645, -1244.03, 0]]
alpha = [[0, 0.3043, 0.3084], [0.3043, 0, 0.095], [0.3084, 0.095, 0]]


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
        self.benzene_ethylacetate = BinaryRelation.objects.create(
            component1=self.benzene,
            component2=self.ethylacetate,
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
        self.methylacetate_methanol = BinaryRelation.objects.create(
            component1=self.methylacetate,
            component2=self.methanol,
            a12=441.452,
            a21=304.005,
            alpha=0.1174,
        )
        self.hexane = Component.objects.create(
            name="hexane",
            a=6.91058,
            b=1189.640,
            c=226.280,
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

    def test_component(self):
        self.assertEqual(self.acetone.name, "acetone")
        self.assertEqual(self.acetone.a, 7.11714)
        self.assertEqual(self.acetone.b, 1210.595)
        self.assertEqual(self.acetone.c, 229.664)

    def test_binary_relation(self):
        self.assertEqual(self.acetone_chloroforme.component1.name, "acetone")
        self.assertEqual(
            self.acetone_chloroforme.component2.name, "chloroforme"
        )
        self.assertEqual(self.acetone_chloroforme.a12, -643.277)
        self.assertEqual(self.acetone_chloroforme.a21, 228.457)
        self.assertEqual(self.acetone_chloroforme.alpha, 0.3043)

    def test_binary_relation_constraint_unique(self):
        with self.assertRaises(IntegrityError):
            BinaryRelation.objects.create(
                component1=self.acetone,
                component2=self.chloroforme,
                a12=-643.277,
                a21=228.457,
                alpha=0.3043,
            )

    def test_binary_relation_possible_with_inversed_components(self):
        BinaryRelation.objects.create(
            component1=self.chloroforme,
            component2=self.acetone,
            a12=-643.277,
            a21=228.457,
            alpha=0.3043,
        )

    def test_binary_relation_with_same_component(self):
        binary_relation = BinaryRelation(
            component1=self.acetone,
            component2=self.acetone,
            a12=-643.277,
            a21=228.457,
            alpha=0.3043,
        )
        with self.assertRaises(ValidationError):
            binary_relation.full_clean()
            binary_relation.save()

    def test_binary_relation_with_same_component2(self):
        binary_relation = BinaryRelation(
            component1=self.acetone,
            component2=self.acetone,
            a12=-643.277,
            a21=228.457,
            alpha=0.3043,
        )
        self.assertRaises(ValidationError, binary_relation.clean)

    def test_component_str(self):
        self.assertEqual(
            str(self.acetone), "acetone (a=7.11714, b=1210.595, c=229.664)"
        )

    def test_binary_relation_str(self):
        self.assertEqual(
            str(self.acetone_chloroforme),
            "acetone - chloroforme",
        )

    def test_delete_component(self):
        self.assertIn(self.acetone, Component.objects.all())
        self.acetone.delete()
        self.assertNotIn(self.acetone, Component.objects.all())

    def test_delete_binary_relation(self):
        self.assertIn(self.acetone_chloroforme, BinaryRelation.objects.all())
        self.acetone_chloroforme.delete()
        self.assertEqual(
            BinaryRelation.objects.filter(component1=self.acetone)
            .filter(component2=self.chloroforme)
            .count(),
            0,
        )
        self.assertNotIn(
            self.acetone_chloroforme, BinaryRelation.objects.all()
        )
        self.assertIn(self.acetone, Component.objects.all())
        self.assertIn(self.chloroforme, Component.objects.all())

    def test_delete_component_with_binary_relation(self):
        self.assertIn(self.acetone, Component.objects.all())
        self.assertIn(self.acetone_chloroforme, BinaryRelation.objects.all())
        self.acetone.delete()
        self.assertEqual(
            BinaryRelation.objects.filter(component1=self.acetone).count(), 0
        )
        self.assertEqual(
            BinaryRelation.objects.filter(component2=self.acetone).count(), 0
        )
        self.assertNotIn(self.acetone, Component.objects.all())
        self.assertNotIn(
            self.acetone_chloroforme, BinaryRelation.objects.all()
        )

    def test_is_component_case_sensitive(self):
        self.assertEqual(Component.objects.filter(name="Acetone").count(), 0)

    def test_create_binary_relation_possible_with_different_case_component(
        self,
    ):
        Acetone = Component.objects.create(
            name="Acetone", a=98.11714, b=1.595, c=2.664
        )
        # Check that no exception is raised
        BinaryRelation.objects.create(
            component1=self.acetone,
            component2=Acetone,
            a12=-643.277,
            a21=228.457,
            alpha=0.3043,
        )
        BinaryRelation.objects.create(
            component1=Acetone,
            component2=self.chloroforme,
            a12=-643.277,
            a21=228.457,
            alpha=0.3043,
        )

    def test_binary_relation_possible_with_component_with_same_name_but_different_values(
        self,
    ):
        acetone = Component.objects.create(
            name="acetone", a=98.11714, b=1.595, c=2.664
        )
        # Check that no exception is raised
        BinaryRelation.objects.create(
            component1=self.acetone,
            component2=acetone,
            a12=-643.277,
            a21=228.457,
            alpha=0.3043,
        )
