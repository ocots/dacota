import sys

sys.path.append(".helpers")

from logging import Logger

from django.contrib.sessions.models import Session
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from ternary_azeotrope.models import BinaryRelation, Component

from .helpers import utils
from .helpers.plotter import get_plot
from .helpers.serializers import ComponentSerializer
from .helpers.ternary_mixture import TernaryMixture
from .helpers.user import User

lg = Logger(name="Log")


def get_user(request):
    if not request.session.has_key("user_data"):
        user = User()
        request.session["user_data"] = user.get_user_data_json()
        return user
    else:
        return User.get_user(request.session["user_data"])


def get_user_data(request):
    return request.session.get("user_data")


def index(request, valid_inputs=True, diagram=None, message=None):
    curr_session = request.session.session_key
    # if not Session.objects.filter(session_key=curr_session).exists():
    #    Session.objects.create(session_key=curr_session)
    if not request.session.has_key("user_data"):
        request.session["user_data"] = {}

    context = {
        "valid_components": valid_inputs,
        "diagram": diagram,
        "message": message,
        # "components": get_user(request).components,
        "components": Component.objects.filter(
            Q(sessions__pk=request.session.session_key)
            | Q(sessions__isnull=True)
        ),
    }

    # print(Session.objects.get(pk=request.session.session_key).components.all())

    return render(
        request,
        "ternary_azeotrope/index.html",
        context,
    )
    # return render(request, "ternary_azeotrope/.html")


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

            r1, r2, r3 = utils.get_session_relations(
                request.session.session_key,
                component1,
                component2,
                component3,
            )

            if len(r1) == 0 or len(r2) == 0 or len(r3) == 0:
                msg = "The following binary relations are not defined : "

                if len(r1) == 0:
                    msg += (
                        component1.name.upper()
                        + " - "
                        + component2.name.upper()
                    )
                if len(r2) == 0:
                    msg += (
                        ", "
                        + component2.name.upper()
                        + " - "
                        + component3.name.upper()
                    )
                if len(r3) == 0:
                    msg += (
                        ", "
                        + component1.name.upper()
                        + " - "
                        + component3.name.upper()
                    )

                return index(request, message=msg)

            else:
                mixture = TernaryMixture(
                    component1, component2, component3, r1[0], r2[0], r3[0]
                )
                curves = mixture.diagram()
                diag = get_plot(curves, mixture)

                return index(request, diagram=diag)

        except ValueError:
            # return redirect("index", False, None
            return index(request, valid_inputs=False)


def add_component(request):
    """user = UserSerializer().create(
        validated_data=request.session[get_sessionId(request)]
    )"""
    print("ADD called")
    if request.method == "POST":
        name = request.POST["name"]
        a = request.POST["a"]
        b = request.POST["b"]
        c = request.POST["c"]

        new_compound = Component.objects.create(name=name, a=a, b=b, c=c)
        new_compound.sessions.add(
            Session.objects.get(pk=request.session.session_key)
        )

        # user = User.get_user(request.session.get("user_data", "{}"))
        # user.add_component(name, float(a), float(b), float(c))
        # request.session["user_data"] = user.get_user_data_json()

        # = UserSerializer(user).data

        return HttpResponseRedirect(reverse("index"))
        # return HttpResponseRedirect(reverse("test"))


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

    # test session attribute
    # c = Component(name="test", a=0, b=0, c=0)
    # c.save()
    # c.sessions.add(Session.objects.get(pk=request.session.session_key))
    print(Session.objects.get(pk=request.session.session_key).components)
    return HttpResponse(msg)
