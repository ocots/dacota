from django.http import HttpResponse
from django.shortcuts import render

from backend_django.ternary_azeotrope.models import Component

# Create your views here.


def index(request):
    # return HttpResponse("Home page")
    return render(request, 'ternary_azeotrope/index.html', {
        'components': Component.objects.all()
    })
