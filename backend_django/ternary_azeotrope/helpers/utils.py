import json

from django.db.models import Q

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


def get_session_relations(session_id, component1, component2, component3):
    all_r1 = BinaryRelation.objects.filter(
        component1=component1, component2=component2
    )
    r1 = all_r1.filter(Q(sessions__isnull=True) | Q(sessions__pk=session_id))

    all_r2 = BinaryRelation.objects.filter(
        component1=component2, component2=component3
    )
    r2 = all_r2.filter(Q(sessions__isnull=True) | Q(sessions__pk=session_id))

    all_r3 = BinaryRelation.objects.filter(
        component1=component1, component2=component3
    )
    r3 = all_r3.filter(Q(sessions__isnull=True) | Q(sessions__pk=session_id))

    return r1, r2, r3


def load_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def formatParameters(c1, c2, c3, a, alpha):
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
