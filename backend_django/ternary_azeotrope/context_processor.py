from .helpers.utils import *
from .models import BinaryRelation, Component


def common_context(request):
    return {
        "components": compounds_of_session(request.session.session_key),
        "relations": relations_of_session(request.session.session_key),
        "component_keys": Component.fields(),
        "relation_keys": BinaryRelation.fields(),
    }
