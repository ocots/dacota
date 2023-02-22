import ast
import json
import sys

sys.path.append(".helpers")

from datetime import datetime

from django.contrib.sessions.models import Session
from django.core.management import call_command
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from ternary_azeotrope.models import BinaryRelation, Component

from backend_django import settings

from .helpers.plotter import get_plot
from .helpers.ternary_mixture import TernaryMixture
from .helpers.utils import *

day = 60 * 60 * 24


def index(request, valid_inputs=True, diagram=None, message=None):
    if not request.session.has_key("created_in"):
        # create a new session instance
        request.session["created_in"] = datetime.now().strftime(
            "%d/%m/%Y, %H:%M:%S"
        )
        # request.session.set_expiry(settings.SESSION_EXPIRY_DURATION)
        request.session.set_expiry(settings.SESSION_EXPIRY_DURATION)

        # remove expired session
        call_command(command_name="clean_expired_sessions")

    context = {
        "valid_components": valid_inputs,
        "diagram": diagram,
        "message": message,
        "components": compounds_of_session(request.session.session_key),
        "relations": relations_of_session(request.session.session_key),
        "component_keys": Component.fields(),
        "relation_keys": BinaryRelation.fields(),
    }

    return render(
        request,
        "ternary_azeotrope/index.html",
        context,
    )


def run(request):
    if request.method == "POST":
        try:
            id1 = request.POST["component1"]
            id2 = request.POST["component2"]
            id3 = request.POST["component3"]

            component1 = Component.objects.get(pk=id1)
            component2 = Component.objects.get(pk=id2)
            component3 = Component.objects.get(pk=id3)

            if (
                component1 == component2
                or component1 == component3
                or component2 == component3
            ):
                raise ValueError

            r1, r2, r3 = get_relations(
                request.session.session_key,
                component1,
                component2,
                component3,
            )

            if len(r1) == 0 or len(r2) == 0 or len(r3) == 0:
                alert_msg = relations_missings_msg(
                    r1, r2, r3, component1, component2, component3
                )
                return index(request, message=alert_msg)

            else:
                mixture = TernaryMixture(
                    component1, component2, component3, r1[0], r2[0], r3[0]
                )
                curves = mixture.diagram()
                diag = get_plot(curves, mixture)

                return index(request, diagram=diag)

        except ValueError:
            return index(request, valid_inputs=False)


def add_component(request):
    if request.method == "POST":
        name = request.POST["name"]
        a = request.POST["a"]
        b = request.POST["b"]
        c = request.POST["c"]

        new_compound = Component.objects.create(name=name, a=a, b=b, c=c)
        new_compound.sessions.add(
            Session.objects.get(pk=request.session.session_key)
        )

        return HttpResponseRedirect(reverse("index"))


def add_relation(request):
    if request.method == "POST":
        component1_id = request.POST.get("component1")
        component2_id = request.POST.get("component2")
        a12 = float(request.POST.get("a12"))
        a21 = float(request.POST.get("a21"))
        alpha = float(request.POST.get("alpha"))

        curr_session = Session.objects.get_or_create(
            session_key=request.session.session_key
        )[0]

        component1 = Component.objects.get(pk=component1_id)
        component2 = Component.objects.get(pk=component2_id)

        relation = BinaryRelation.objects.create(
            component1=component1,
            component2=component2,
            a12=a12,
            a21=a21,
            alpha=alpha,
        )
        relation.sessions.add(curr_session)

        return redirect("index")
