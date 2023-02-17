import json
import sys
import uuid

sys.path.append(".helpers")

from logging import Logger

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from ternary_azeotrope.models import Component

from .helpers import utils
from .helpers.plotter import get_plot
from .helpers.serializers import ComponentSerializer
from .helpers.ternary_mixture import TernaryMixture
from .helpers.user import User

lg = Logger(name="Log")


def get_user(request):
    if not request.session.has_key("user_data"):
        user = User()
        print(user.components[0].id)
        sys.edit(0)
        # print(user.components)
        request.session["user_data"] = user.get_user_data_json()
        # print(user.get_user_data_json())
        return user
    else:
        return User.get_user(request.session["user_data"])


def get_user_data(request):
    # if not request.session.has_key("user_data"):
    #    request.session["user_data"] = User().get_user_data_json()

    return request.session.get("user_data")


def index(request, valid_inputs=True, diagram=None):
    context = {
        "valid_components": valid_inputs,
        "diagram": diagram,
        "components": get_user(request).components,
    }

    # print(get_user(request).components)

    # context["components"] = get_user(request).components

    return render(
        request,
        "ternary_azeotrope/index.html",
        context,
    )
    # return render(request, "ternary_azeotrope/.html")


def run(request):
    print(Component.objects)
    if request.method == "POST":
        print(request.POST)
        try:
            id1 = int(request.POST["component1"])
            id2 = int(request.POST["component2"])
            id3 = int(request.POST["component3"])
            component1 = Component.objects.get(pk=id1)
            component2 = Component.objects.get(pk=id2)
            component3 = Component.objects.get(pk=id3)

            # print(component2)

            if (
                component1 == component2
                or component1 == component3
                or component2 == component3
            ):
                raise ValueError

            try:
                r1, r2, r3 = utils.get_binaryRelations_fromDB(
                    component1, component2, component3
                )
            except:
                raise ValueError

            mixture = TernaryMixture(
                component1, component2, component3, r1, r2, r3
            )
            curves = mixture.diagram()
            diag = get_plot(curves, mixture)

            return index(request, diagram=diag)

        except ValueError:
            # return redirect("index", False, None)
            return index(request, valid_inputs=False)


def add_component(request, name: str, a: str, b: str, c: str):
    """user = UserSerializer().create(
        validated_data=request.session[get_sessionId(request)]
    )"""

    # print(user.components)
    user = User.get_user(request.session.get("user_data", "{}"))
    user.add_component(name, float(a), float(b), float(c))
    request.session["user_data"] = user.get_user_data_json()

    """temp = request.session["user_data"]["components"].append(
        {"name": name, "a": a, "b": b, "c": c}
    )
    request.session["user_data"]["components"] = temp"""
    # = UserSerializer(user).data

    # return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("test"))


def list(request):
    d = request.session.get("user_data")
    return HttpResponse(str(d))


def test(request):
    msg = ""
    if not request.session.has_key("user_data"):
        new_user = User()
        # user_data = UserSerializer(new_user).data
        request.session["user_data"] = new_user.get_user_data_json()

        msg = (
            "NEW SESSION \n"
            + "user data :"
            + str(request.session["user_data"])
            + "\n user components : "
            + str(new_user.components)
        )

    else:
        d = request.session.get("user_data", "{}")
        curr_user = User.get_user(d)
        # print(curr_user.components)
        msg = (
            "EXISTING SESSION - user data :"
            + str(d)
            + "\n user components list : "
            + str(curr_user.components)
        )

    return HttpResponse(msg)
