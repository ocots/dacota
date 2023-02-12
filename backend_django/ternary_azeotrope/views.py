from django.http import HttpResponse
from django.shortcuts import render

from ternary_azeotrope.models import Component

# Create your views here.


def index(request):
    # return HttpResponse("Home page")
    return render(request, 'ternary_azeotrope/index.html', {
        "componenents": Component.objects.all()
    })
