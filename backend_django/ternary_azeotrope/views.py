import sys

sys.path.append(".helpers")

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from ternary_azeotrope.models import Component

from .helpers import utils
from .helpers.plotter import get_plot
from .helpers.ternary_mixture import TernaryMixture
from .helpers.user import User

user = User()


# Create your views here.
def index(
    request,
    valid_inputs=True,
    diagram=None,
):
    if "user_data" not in request.session:
        new_user = User()
        request.session["user_data"] = new_user.__dict__
    else:
        print(request.session["user_data"])

    return render(
        request,
        "ternary_azeotrope/index.html",
        {
            "components": Component.objects.all(),
            "valid_components": valid_inputs,
            "diagram": diagram,
        },
    )
    # return render(request, "ternary_azeotrope/.html")


def run(request):
    if request.method == "POST":
        print(request.session)
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
            return index(request, valid_inputs=False)


def add_component(request, name: str, a: str, b: str, c: str):
    user.add_component(name, float(a), float(b), float(c))
    print(user.components)
    return HttpResponse(user.components_as_str())
    # return HttpResponse(request, "Added")
