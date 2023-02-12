from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from ternary_azeotrope.models import Component

# Create your views here.


def index(request, valid_inputs=True):
    # return HttpResponse("Home page")
    return render(
        request,
        "ternary_azeotrope/index.html",
        {
            "componenents": Component.objects.all(),
            "valid_components": valid_inputs,
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

            # line only for test, to comment after generating diagram view is done etc
            return HttpResponse(
                f"Chosen components : {component1},  {component2},  {component3}"
            )

        except ValueError:
            # return HttpResponseRedirect(reverse("index", args=(False,)))
            return index(request, False)
            # return HttpResponse(
            #    "user didn't select 3 components or components are not distinct"
            # )
