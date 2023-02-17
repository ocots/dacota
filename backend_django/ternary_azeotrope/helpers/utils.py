from ..models import BinaryRelation


def get_binaryRelations_fromDB(component1, component2, component3):
    r1 = BinaryRelation.objects.get(
        component1=component1, component2=component2
    )
    r2 = BinaryRelation.objects.get(
        component1=component2, component2=component3
    )
    r3 = BinaryRelation.objects.get(
        component1=component1, component2=component3
    )

    return r1, r2, r3
