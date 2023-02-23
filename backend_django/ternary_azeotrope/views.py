import ast
import json
import sys
from urllib.parse import urlencode

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


def get_context(request):
    if "context" in request.session:
        data = request.session.get("context", {})
        request.session.pop("context")
        return data
    return {}


def index(request):
    # check if the request comes from a new client
    if not request.session.has_key("created_in"):
        # create a new session instance
        request.session["created_in"] = datetime.now().strftime(
            "%d/%m/%Y, %H:%M:%S"
        )
        request.session.set_expiry(settings.SESSION_EXPIRY_DURATION)

        # remove expired session
        call_command(command_name="clean_expired_sessions")

    extra_context = get_context(request)
    return render(request, "ternary_azeotrope/index.html", extra_context)


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

                request.session["context"] = {"alert_message": alert_msg}

            else:
                mixture = TernaryMixture(
                    component1, component2, component3, r1[0], r2[0], r3[0]
                )
                curves = mixture.diagram()
                curves = json.dumps(curves)
                # diag = get_plot(curves, mixture)

                request.session["context"] = {"curves": curves}

        except ValueError:
            request.session["context"] = {
                "alert_message": "The mixture compounds should be distinct !"
            }

        return redirect("index")


def add_component(request):
    if request.method == "POST":
        name = request.POST["name"]
        a = request.POST["a"]
        b = request.POST["b"]
        c = request.POST["c"]

        curr_session = Session.objects.get(pk=request.session.session_key)
        msg = None

        if Component.objects.filter(name=name, a=a, b=b, c=c).exists():
            c = Component.objects.get(name=name, a=a, b=b, c=c)
            if not c.sessions.contains(curr_session):
                c.sessions.add(curr_session)
                c.save()
                msg = f"Compound {c} added successfuly."
            else:
                # component already available for the session
                msg = f"{c} already exists !"
        else:
            new_compound = Component.objects.create(name=name, a=a, b=b, c=c)
            new_compound.sessions.add(curr_session)

            msg = f"Compound {new_compound} added successfuly."

        request.session["context"] = {"info_message": msg}
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

        msg = None

        if BinaryRelation.objects.filter(
            component1=component1,
            component2=component2,
        ).exists():
            relation = BinaryRelation.objects.get(
                component1=component1,
                component2=component2,
            )

            if (
                relation.a12 == a12
                and relation.a21 == a21
                and relation.alpha == alpha
            ):
                if not relation.sessions.contains(curr_session):
                    relation.sessions.add(curr_session)
                    relation.save()
                    msg = f"Binary relation {relation} added successfuly."
                else:
                    # relation already available for the session, a message to the user will be added later
                    msg = f"Binary relation {relation} with the same parameters already exists !"
            else:
                # unique constraint
                msg = f"New binary relation {relation} cannot be added. please edit their parameters instead."
        else:
            relation = BinaryRelation.objects.create(
                component1=component1,
                component2=component2,
                a12=a12,
                a21=a21,
                alpha=alpha,
            )
            relation.sessions.add(curr_session)
            msg = f"Binary relation {relation} added successfuly."

        request.session["context"] = {"info_message": msg}
        return redirect("index")
