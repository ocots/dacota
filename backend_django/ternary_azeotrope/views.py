import sys

sys.path.append(".helpers")

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from ternary_azeotrope.models import Component

from .helpers.plotter import get_plot
from .helpers.ternary_mixture import TernaryMixture


# Create your views here.
def index(request, valid_inputs=True, diagram=None):
    print(Component.objects.all())
    return render(
        request,
        "ternary_azeotrope/index.html",
        {
            "components": Component.objects.all(),
            "valid_components": valid_inputs,
            "diagram": diagram,
        },
    )


def run(request):
    if request.method == "POST":
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

            mixture = TernaryMixture(component1, component2, component3)
            curves = mixture.diagram()
            diag = get_plot(curves, mixture)

            return index(request, diagram=diag)

        except ValueError:
            return index(request, valid_inputs=False)
