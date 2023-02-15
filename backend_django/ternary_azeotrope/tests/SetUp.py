from ..models import BinaryRelation, Component


def init(obj):
    obj.acetone = Component.objects.create(
        name="acetone",
        a=7.11714,
        b=1210.595,
        c=229.664,
    )
    obj.chloroforme = Component.objects.create(
        name="chloroforme",
        a=6.95465,
        b=1170.966,
        c=226.232,
    )
    obj.benzene = Component.objects.create(
        name="benzene",
        a=6.87087,
        b=1196.760,
        c=219.161,
    )

    obj.methanol = Component.objects.create(
        name="methanol",
        a=8.08097,
        b=1582.271,
        c=239.726,
    )

    obj.acetone_chloroforme = BinaryRelation.objects.create(
        component1=obj.acetone,
        component2=obj.chloroforme,
        a12=-643.277,
        a21=228.457,
        alpha=0.3043,
    )
    obj.acetone_benzene = BinaryRelation.objects.create(
        component1=obj.acetone,
        component2=obj.benzene,
        a12=-193.34,
        a21=569.931,
        alpha=0.3007,
    )
    obj.chloroforme_benzene = BinaryRelation.objects.create(
        component1=obj.chloroforme,
        component2=obj.benzene,
        a12=176.8791,
        a21=-288.2136,
        alpha=0.3061,
    )
