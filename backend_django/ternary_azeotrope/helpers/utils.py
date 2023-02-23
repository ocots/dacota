import json

from django.contrib.sessions.models import Session
from django.db.models import Q

from ..models import BinaryRelation, Component


def compounds_of_session(session_key):
    return Component.objects.filter(
        Q(sessions__pk=session_key) | Q(sessions__isnull=True)
    ).order_by("name")


def relations_of_session(session_key):
    return BinaryRelation.objects.filter(
        Q(sessions__pk=session_key) | Q(sessions__isnull=True)
    ).order_by("component1")


def delete_item(item, session_key):
    """Remove an instance of either component or binary relation models from a session

    Args:
        item (Component | BinaryRelation): instance to remove
        session_key (str): session id from which the instance is removed
    """
    nb_session = item.sessions.count()
    if nb_session != 0:
        print(f"number of sessions that added {item} is {nb_session}")

        if nb_session == 1:
            print("deleting ", item)
            item.delete()
        else:
            item.sessions.remove(Session.objects.get(pk=session_key))


def clear_session_data(session_key, compounds=None, relations=None):
    """Remove all compounds and binary relations registered for a session
    this function takes either the key of the session and look up for the elements to remove or
    takes directly the elements in arguments

    Args:
        session_key (str): session id from which the data is removed
        compounds (List[Component] | None) components to clear if not none
        relation (List[BinaryRelation] | None) BinaryRelations to clear if not none
    """
    (compounds, relations) = compounds, relations

    if not compounds and not relations:
        compounds = Component.objects.filter(Q(sessions__pk=session_key))
        relations = BinaryRelation.objects.filter(Q(sessions__pk=session_key))

    for c in compounds:
        delete_item(c, session_key)

    for r in relations:
        delete_item(r, session_key)


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


def get_relations(session_id, component1, component2, component3):
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


def relations_missings_msg(r1, r2, r3, component1, component2, component3):
    msg = "The following binary relations are not defined : "

    missings = []
    if len(r1) == 0:
        missings.append(component1.name + " - " + component2.name)
    if len(r2) == 0:
        missings.append(component2.name + " - " + component3.name)
    if len(r3) == 0:
        missings.append(component1.name + " - " + component3.name)

    return msg + ", ".join(missings)


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
