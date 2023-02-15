from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("run", views.run, name="run"),
    path(
        "add/<str:name>/<str:a>/<str:b>/<str:c>",
        views.add_component,
        name="add",
    ),
    path("list", views.list, name="list"),
    path("test_session", views.test, name="test"),
]
