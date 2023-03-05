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

from .helpers.ternary_mixture import TernaryMixture
from .helpers.utils import *


def get_context(request):
    if "context" in request.session:
        data = request.session.get("context", {})
        to_keep = ["c1_selected", "c2_selected", "c3_selected"]
        selected = {}
        for k in to_keep:
            if k in data:
                selected[k] = data[k]
        request.session["context"] = selected
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
    """Function to launch the calculation to generate the diagram

    Args:
        request (_type_): the request

    Raises:
        ValueError: where the mixture compounds selected are not distinct

    Returns:
        the diagram of the compound selected in the page
    """
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

                request.session["context"] = {
                    "message": alert_msg,
                    "type": "danger",
                }

            else:
                mixture = TernaryMixture(
                    component1, component2, component3, r1[0], r2[0], r3[0]
                )
                curves = mixture.diagram()
                curves = json.dumps(curves)

                request.session["context"] = {
                    "curves": curves,
                }

        except ValueError:
            request.session["context"] = {
                "message": "The mixture compounds should be distinct !",
                "type": "danger",
            }

        request.session["context"].update(
            {
                "c1": str(component1),
                "c2": str(component2),
                "c3": str(component3),
                "c1_selected": component1.id,
                "c2_selected": component2.id,
                "c3_selected": component3.id,
            }
        )

        return redirect("index")


def add_component(request):
    """ "Function to add a new compound

    Args:
        request (_type_): the request

    Returns:
        redirect to the updated page with the new compound in the table of compounds
    """
    if request.method == "POST":
        name = request.POST["name"]
        a = request.POST["a"]
        b = request.POST["b"]
        c = request.POST["c"]

        curr_session = Session.objects.get(pk=request.session.session_key)

        if Component.objects.filter(name=name, a=a, b=b, c=c).exists():
            c = Component.objects.get(name=name, a=a, b=b, c=c)
            if not c.sessions.contains(curr_session):
                c.sessions.add(curr_session)
                c.save()
                msg = f"Compound {c} added successfuly."
                request.session["context"] = {
                    "message": msg,
                    "type": "success",
                }
            else:
                # component already available for the session
                msg = f"{c} already exists !"
                request.session["context"] = {
                    "message": msg,
                    "type": "warning",
                }
        else:
            new_compound = Component.objects.create(name=name, a=a, b=b, c=c)
            new_compound.sessions.add(curr_session)

            msg = f"Compound {new_compound} added successfuly."
            request.session["context"] = {"message": msg, "type": "success"}

        return HttpResponseRedirect(reverse("index"))


def add_relation(request):
    """Function to add a new relation between two compounds

    Args:
        request (_type_): the request

    Returns:
        redirect to the updated page with the new relation in the table of relations
    """
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
                    request.session["context"] = {
                        "message": msg,
                        "type": "info",
                    }
                else:
                    # relation already available for the session, a message to the user will be added later
                    msg = f"Binary relation {relation} with the same parameters already exists !"
                    request.session["context"] = {
                        "message": msg,
                        "type": "warning",
                    }
            else:
                # unique constraint
                msg = f"Binary relation {relation} already exists. You can edit their parameters."
                request.session["context"] = {
                    "message": msg,
                    "type": "danger",
                }
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
            request.session["context"] = {"message": msg, "type": "success"}
        return redirect("index")


def edit_relation(request):
    """Function to edit the parameters of a relation in the table

    Args:
        request (_type_): the request

    Returns:
        redirect to the principal page with a updated table
    """
    if request.method == "POST":
        json_data = request.body.decode("utf-8")
        data = json.loads(json_data)
        id = data.pop("id")
        relation = BinaryRelation.objects.get(pk=id)
        if "component1" in data:
            data.pop("component1")
        if "component2" in data:
            data.pop("component2")

        edit_element(request.session.session_key, relation, data)

        return redirect("index")


def edit_component(request):
    """Function to edit the parameters of a compound in the table

    Args:
        request (_type_): the request

    Returns:
        redirect to the principal page with a updated table

    """
    if request.method == "POST":
        json_data = request.body.decode("utf-8")
        data = json.loads(json_data)
        id = data.pop("id")
        component = Component.objects.get(pk=id)
        edit_element(request.session.session_key, component, data)

        return redirect("index")


def delete_relation(request, relation_id: str):
    """Function to delete a relation from the table by the icon in Actions


    Args:
        request (_type_): the request
        relation_id (str):  the id of the relation to remove
    Returns:
        redirect to the principal page with a updated table
    """
    if request.method == "GET":
        relation = BinaryRelation.objects.get(pk=int(relation_id))
        delete_item(relation, request.session.session_key)

        return redirect("index")


def delete_compound(request, compound_id: str):
    """Function to delete a compound from the table by the icon in Actions

    Args:
        request (_type_): the request
        compound_id (str): the id of the compound to remove
    Returns:
        redirect to the principal page with a updated table
    """
    if request.method == "GET":
        component = Component.objects.get(pk=int(compound_id))
        delete_item(component, request.session.session_key)

        return redirect("index")
