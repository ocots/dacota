from django.http import HttpResponse
from django.shortcuts import render
from ternary_azeotrope.models import Component

# Create your views here.


def index(request):
    # return HttpResponse("Home page")
    return render(
        request,
        "ternary_azeotrope/index.html",
        {"componenents": Component.objects.all()},
    )


def run(request):
    if request.method == "POST":
        component1 = Component.objects.get(pk=request.POST["component1"])
        component2 = Component.objects.get(pk=request.POST["component2"])
        component3 = Component.objects.get(pk=request.POST["component3"])

        # line only for test, to comment after generating diagram view is done etc
        return HttpResponse(
            f"Chosen components : {component1},  {component2},  {component3}"
        )
