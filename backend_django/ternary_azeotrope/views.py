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
from .helpers.serializers import UserSerializer
from .helpers.ternary_mixture import TernaryMixture
from .helpers.user import User

lg = Logger(name="Log")


def get_sessionId(request):
    # return str(request.session._get_or_create_session_key())
    # id = str(request.session[""])
    # print(id)
    return "user_data"


def get_user(request):
    session_id = get_sessionId(request)
    if session_id in request.session:
        return UserSerializer().create(
            validated_data=request.session[session_id]
        )
    else:
        new_user = User()
        print("new user created")
        return new_user


def get_user_data(request):
    data = UserSerializer(get_user(request)).data
    # print("DATA : ", data)
    return data


def index(request, valid_inputs=True, diagram=None, first=True):
    # print(str(request.session.session_key)))
    # if first:
    #   request.session.cookie_name = str(uuid.uuid4())
    session_id = get_sessionId(request)
    context = {
        "valid_components": valid_inputs,
        "diagram": diagram,
        # "components": Component.objects.all(),
    }

    if session_id not in request.session:
        request.session[session_id] = get_user_data(request)
        # request.session.save()
        # context["components"] = (Component.objects.all(),)

    test = request.session[session_id]
    print(test)

    # else:
    # del request.session[str(request.session.session_key)]
    context["components"] = get_user(request).components
    # context["components"] = Component.objects.all()
    # print("user components : ", request.session[str(request.session.session_key)]["components"])"""

    return render(
        request,
        "ternary_azeotrope/index.html",
        context,
    )
    # return render(request, "ternary_azeotrope/.html")


def run(request):
    if request.method == "POST":
        # print(request.session)
        try:
            id1 = int(request.POST["component1"])
            id2 = int(request.POST["component2"])
            id3 = int(request.POST["component3"])
            component1 = Component.objects.get(pk=id1)
            component2 = Component.objects.get(pk=id2)
            component3 = Component.objects.get(pk=id3)

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
    user = UserSerializer().create(
        validated_data=request.session[get_sessionId(request)]
    )
    # print(user.components)
    user.add_component(name, float(a), float(b), float(c))
    # request.session[str(request.session.session_key)]["component"].append(Compo)
    # = UserSerializer(user).data
    # request.session.save()
    # print(user.components)

    return HttpResponseRedirect(reverse("index"))
    # return HttpResponse(request, "Added")


def list(request):
    return HttpResponse(str(get_user_data(request)))


def test(request):
    if not request.session.has_key("user_data"):
        new_user = User()
        user_data = UserSerializer(new_user).data
        request.session["user_data"] = user_data

        return HttpResponse("NEW SESSION" + str(request.session["user_data"]))
    else:
        return HttpResponse(
            "EXISTING SESSION" + str(request.session["user_data"])
        )
