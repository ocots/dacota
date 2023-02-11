from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    # return HttpResponse("Home page")
    return render(request, 'ternary_azeotrope/index.html')
    """, {
    'components': Components.objects.all()
    }"""
