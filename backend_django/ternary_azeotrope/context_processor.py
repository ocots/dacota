from .helpers.utils import *
from .models import BinaryRelation, Component
import json


def common_context(request):
    components = list(compounds_of_session(request.session.session_key))
    relations = list(relations_of_session(request.session.session_key))
    return {
        "components": components,
        "components_json": json.dumps([c.id for c in components]),
        "relations": relations,
        "relations_json": json.dumps(
            [(r.component1.id, r.component2.id) for r in relations]
        ),
        "component_keys": Component.fields(),
        "relation_keys": BinaryRelation.fields(),
    }
